import requests
import logging
import csv
import argparse
from time import sleep
import configparser  # Add this import

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

# Headers for authentication
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Function to fetch all projects
def get_all_projects():
    url = f"{JIRA_BASE_URL}/rest/api/3/project"
    response = requests.get(url, headers=HEADERS, auth=(EMAIL, API_TOKEN))
    
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"❌ Failed to fetch projects. Status: {response.status_code}, Response: {response.text}")
        return None

# Function to fetch permission scheme for a project
def get_permission_scheme_for_project(project_id):
    url = f"{JIRA_BASE_URL}/rest/api/3/project/{project_id}/permissionscheme"
    response = requests.get(url, headers=HEADERS, auth=(EMAIL, API_TOKEN))
    
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"❌ Failed to fetch permission scheme for project ID {project_id}. Status: {response.status_code}, Response: {response.text}")
        return None

# Function to write data to CSV
def write_to_csv(file_name, data):
    with open(file_name, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Project Name", "Project Key", "Permission Scheme"])
        writer.writerows(data)
    logging.info(f"👍 Data has been written to {file_name}")

# Parse command-line arguments
parser = argparse.ArgumentParser(description="List Jira projects and their permission schemes.")
parser.add_argument("--csv", help="Dump the data into a CSV file. Specify the file name.")
args = parser.parse_args()

# Fetch all projects
projects = get_all_projects()
if not projects:
    exit()

# Prepare data for CSV or console output
output_data = []
for project in projects:
    project_name = project["name"]
    project_key = project["key"]
    project_id = project["id"]
    
    # Fetch permission scheme for the project
    permission_scheme = get_permission_scheme_for_project(project_id)
    
    if permission_scheme:
        scheme_name = permission_scheme.get("name", "No permission scheme assigned")
        logging.info(f"✅ Project: {project_name} | Permission Scheme: {scheme_name}")
        output_data.append([project_name, project_key, scheme_name])
    else:
        logging.error(f"❌ Project: {project_name} | Failed to fetch permission scheme.")
        output_data.append([project_name, project_key, "Failed to fetch permission scheme"])
    
    # Add a delay to avoid hitting rate limits
    sleep(1)

# Write to CSV if --csv flag is provided
if args.csv:
    write_to_csv(args.csv, output_data)
else:
    # Display data in the console
    # Remove or comment out the following loop
    # for row in output_data:
    #     logging.info(f"Project: {row[0]} | Key: {row[1]} | Permission Scheme: {row[2]}")
    pass