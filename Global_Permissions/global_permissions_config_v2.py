import requests
import logging
import configparser

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

# Function to read configuration from .ini file
def read_config(file_path):
    config = configparser.ConfigParser()
    try:
        config.read(file_path)
    except Exception as e:
        logging.error(f"❌ Error reading configuration file: {e}")
        exit()
    return config

# Load configuration from global_permissions_config.ini
config = read_config("global_permissions_config.ini")

# Assign configuration values
try:
    holder_type = config.get("GlobalPermissions", "holder_type")
    holder_parameter = config.get("GlobalPermissions", "holder_parameter")
    permissions = [p.strip() for p in config.get("GlobalPermissions", "permissions").split(",")]
except configparser.NoSectionError:
    logging.error("❌ The 'GlobalPermissions' section is missing in the configuration file.")
    exit()
except configparser.NoOptionError as e:
    logging.error(f"❌ Missing required key in the configuration file: {e}")
    exit()

# Validate configuration
if not all([holder_type, holder_parameter, permissions]):
    logging.error("❌ Missing required configuration in global_permissions_config.ini.")
    exit()

# Jira API credentials (replace with your values)
JIRA_BASE_URL = "https://balrog.atlassian.net"
EMAIL = "your-email@example.com"
API_TOKEN = "your-api-token"

# Headers for authentication
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Function to grant global permissions
def grant_global_permission(permission, holder_type, holder_parameter):
    url = f"{JIRA_BASE_URL}/rest/api/3/permissions"
    payload = {
        "permissions": [
            {
                "holder": {
                    "type": holder_type,
                    "parameter": holder_parameter
                },
                "permission": permission
            }
        ]
    }
    
    response = requests.post(url, json=payload, headers=HEADERS, auth=(EMAIL, API_TOKEN))
    
    if response.status_code == 204:
        logging.info(f"✅ Granted '{permission}' permission to {holder_type} '{holder_parameter}' successfully!")
    else:
        logging.error(f"❌ Failed to grant '{permission}' permission. Status: {response.status_code}, Response: {response.text}")

# Grant each permission specified in the .ini file
for permission in permissions:
    grant_global_permission(permission, holder_type, holder_parameter)