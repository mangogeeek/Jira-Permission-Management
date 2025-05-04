import requests
import logging
import configparser
from time import sleep

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

# Function to read configuration from config.ini
def read_config(file_path):
    config = configparser.ConfigParser()
    try:
        config.read(file_path)
    except Exception as e:
        logging.error(f"❌ Error reading configuration file: {e}")
        exit()
    return config

# Load configuration from config.ini
config = read_config("config.ini")

# Assign configuration values
JIRA_BASE_URL = config.get("Jira", "JIRA_BASE_URL")
EMAIL = config.get("Jira", "EMAIL")
API_TOKEN = config.get("Jira", "API_TOKEN")

# Validate configuration
if not all([JIRA_BASE_URL, EMAIL, API_TOKEN]):
    logging.error("❌ Missing required configuration in config.ini.")
    exit()

# Load project names and permission scheme name from project_permissions_config.ini
project_config = read_config("assign_jira_permission_scheme_v2.ini")

# Assign project names and permission scheme name
PROJECT_NAMES = [name.strip() for name in project_config.get("Projects", "project_names").split(",")]
PERMISSION_SCHEME_NAME = project_config.get("Projects", "permission_scheme_name")

# Validate project names and permission scheme name
if not PROJECT_NAMES or not PERMISSION_SCHEME_NAME:
    logging.error("❌ Missing project names or permission scheme name in project_permissions_config.ini.")
    exit()

# Headers for authentication
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Function to get project ID from project name
def get_project_id(project_name):
    url = f"{JIRA_BASE_URL}/rest/api/3/project"
    response = requests.get(url, headers=HEADERS, auth=(EMAIL, API_TOKEN))
    
    if response.status_code == 200:
        projects = response.json()
        for project in projects:
            if project["name"] == project_name:
                return project["id"]
        logging.error(f"❌ Project '{project_name}' not found.")
    else:
        logging.error(f"❌ Failed to fetch projects. Status: {response.status_code}, Response: {response.text}")
    return None

# Function to get permission scheme ID from name
def get_permission_scheme_id(permission_scheme_name):
    url = f"{JIRA_BASE_URL}/rest/api/3/permissionscheme"
    response = requests.get(url, headers=HEADERS, auth=(EMAIL, API_TOKEN))
    
    if response.status_code == 200:
        schemes = response.json().get("permissionSchemes", [])
        for scheme in schemes:
            if scheme["name"] == permission_scheme_name:
                return scheme["id"]
        logging.error(f"❌ Permission scheme '{permission_scheme_name}' not found.")
    else:
        logging.error(f"❌ Failed to fetch permission schemes. Status: {response.status_code}, Response: {response.text}")
    return None

# Function to update permission scheme for a project
def update_permission_scheme(project_id, permission_scheme_id, project_name, permission_scheme_name):
    url = f"{JIRA_BASE_URL}/rest/api/3/project/{project_id}/permissionscheme"
    payload = {"id": permission_scheme_id}
    
    response = requests.put(url, json=payload, headers=HEADERS, auth=(EMAIL, API_TOKEN))
    
    if response.status_code == 200:
        logging.info(f"✅ Updated project '{project_name}' with permission scheme '{permission_scheme_name}' successfully!")
    else:
        logging.error(f"❌ Failed to update project '{project_name}'. Status: {response.status_code}, Response: {response.text}")

# Get the correct Permission Scheme ID
PERMISSION_SCHEME_ID = get_permission_scheme_id(PERMISSION_SCHEME_NAME)
if not PERMISSION_SCHEME_ID:
    logging.error("❌ Cannot proceed without a valid permission scheme ID.")
    exit()

# Loop through each project and update the permission scheme
for project_name in PROJECT_NAMES:
    project_id = get_project_id(project_name)
    if not project_id:
        continue  # Skip if project ID is not found

    update_permission_scheme(project_id, PERMISSION_SCHEME_ID, project_name, PERMISSION_SCHEME_NAME)
    
    # Add a delay to avoid hitting rate limits
    sleep(1)