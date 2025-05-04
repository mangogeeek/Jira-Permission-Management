import requests
import logging
import argparse
import configparser
from time import sleep

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

# Function to read configuration from config.ini
def read_config(file_path):
    config = configparser.ConfigParser()
    try:
        config.read(file_path)
        jira_base_url = config["Jira"]["JIRA_BASE_URL"]
        email = config["Jira"]["EMAIL"]
        api_token = config["Jira"]["API_TOKEN"]
        return jira_base_url, email, api_token
    except Exception as e:
        logging.error(f"❌ Error reading configuration file: {e}")
        exit()

# Function to read permissions configuration from update_permissions.ini
def read_permissions_config(file_path):
    config = configparser.ConfigParser()
    try:
        config.read(file_path)
        group = config.get("Target", "GROUP", fallback=None)
        user = config.get("Target", "USER", fallback=None)
        permissions = [key.upper() for key in config["Permissions"] if config["Permissions"].getboolean(key)]
        return permissions, group, user
    except Exception as e:
        logging.error(f"❌ Error reading permissions configuration file: {e}")
        exit()

# Load configuration from config.ini
JIRA_BASE_URL, EMAIL, API_TOKEN = read_config("config.ini")

# Headers for authentication
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

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

# Function to update permission in a permission scheme
def update_permission_scheme(scheme_id, permission, target_type, target):
    url = f"{JIRA_BASE_URL}/rest/api/3/permissionscheme/{scheme_id}/permission"
    payload = {
        "holder": {
            "type": target_type,
            "parameter": target
        },
        "permission": permission
    }
    
    response = requests.post(url, json=payload, headers=HEADERS, auth=(EMAIL, API_TOKEN))
    
    if response.status_code == 201:
        logging.info(f"✅ Updated permission '{permission}' for {target_type} '{target}'.")
    else:
        logging.error(f"❌ Failed to update permission '{permission}' for {target_type} '{target}'. Status: {response.status_code}, Response: {response.text}")

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Update permissions in a Jira permission scheme.")
parser.add_argument("--scheme", required=True, help="Name of the permission scheme to update.")
args = parser.parse_args()

# Load permissions configuration from update_permissions.ini
permissions, group, user = read_permissions_config("update_permissions.ini")

# Validate permissions configuration
if not permissions:
    logging.error("❌ No permissions specified in update_permissions.ini.")
    exit()
if not group and not user:
    logging.error("❌ No group or user specified in update_permissions.ini.")
    exit()

# Get the permission scheme ID
scheme_id = get_permission_scheme_id(args.scheme)
if not scheme_id:
    exit()

# Update permissions in the permission scheme
for permission in permissions:
    if group:
        update_permission_scheme(scheme_id, permission, "group", group)
        sleep(1)  # Add a delay to avoid hitting rate limits
    if user:
        update_permission_scheme(scheme_id, permission, "user", user)
        sleep(1)  # Add a delay to avoid hitting rate limits