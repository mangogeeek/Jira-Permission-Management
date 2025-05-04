## Jira Permission Management Scripts

This package contains scripts to manage Jira projects and permissions. Follow the instructions below to configure and run the scripts.

* * *

### Prerequisites

1.  Python 3.x installed on your system.
2.  Required Python libraries: `requests`, `configparser`, `logging`, `csv`, `argparse`.
3.  A valid Jira API token for authentication.

* * *

### Configuration

Update the `config.ini` file with your Jira credentials:

- `JIRA_BASE_URL`: Your Jira instance URL (e.g., https://your-domain.atlassian.net).
- `EMAIL`: The email address associated with your Jira account.
- `API_TOKEN`: Your Jira API token.

Example `config.ini`:

```[Jira]
JIRA_BASE_URL = https://your-domain.atlassian.net
EMAIL = your-email@example.com
API_TOKEN = your-api-token

```

* * *

## Scripts

### 1\. List Existing Projects and Associated Permission Schemes

This script lists all Jira projects and their associated permission schemes.

**Display in Console:**

```Python
python list_jira_project_permissions_v2.py
```

Example Output

```Python
✅ Project: Bug Tracker | Permission Scheme: GitProtect Permission Scheme.
✅ Project: Bulk Restore | Permission Scheme: demo.
✅ Project: GitProtectDemo | Permission Scheme: GitProtect Permission Scheme.
✅ Project: GitProtectDemo_1738566709 | Permission Scheme: GitProtect Permission Scheme.
✅ Project: Scrum Project | Permission Scheme: GitProtect Permission Scheme.
✅ Project: Scrum Project-A | Permission Scheme: GitProtect Permission Scheme.
✅ Project: Scrum Project-B | Permission Scheme: GitProtect Permission Scheme.
✅ Project: Scrum Project-C | Permission Scheme: GitProtect Permission Scheme.
✅ Project: The Peak of Zirakzigil | Permission Scheme: SCRUM: Simplified Permission Scheme.
```

**Export to CSV:**

```Python
python list_jira_project_permissions_v2.py --csv output.csv
```

Example Output:

```Python
✅ Project: Bug Tracker | Permission Scheme: GitProtect Permission Scheme.
✅ Project: Bulk Restore | Permission Scheme: demo.
✅ Project: GitProtectDemo | Permission Scheme: GitProtect Permission Scheme.
✅ Project: GitProtectDemo_1738566709 | Permission Scheme: GitProtect Permission Scheme.
✅ Project: Scrum Project | Permission Scheme: GitProtect Permission Scheme.
✅ Project: Scrum Project-A | Permission Scheme: GitProtect Permission Scheme.
✅ Project: Scrum Project-B | Permission Scheme: GitProtect Permission Scheme.
✅ Project: Scrum Project-C | Permission Scheme: GitProtect Permission Scheme.
✅ Project: The Peak of Zirakzigil | Permission Scheme: SCRUM: Simplified Permission Scheme.
👍 Data has been written to output.csv.
```

* * *

### 2\. Map Permission Scheme to Project(s)

Update the `assign_jira_permission_scheme_v2.ini` file with the **project names** and **permission scheme name**:

`[Projects]`  
`project_names = Bulk Restore, GitProtectDemo`  
`permission_scheme_name = Bug Tracker Permission Scheme`

Run the script:

```python
python assign_jira_permission_scheme_v2.py
```

Example Output:

```Python
✅ Updated project 'Bulk Restore' with permission scheme 'Bug Tracker Permission Scheme' successfully!  
✅ Updated project 'GitProtectDemo' with permission scheme 'Bug Tracker Permission Scheme' successfully!
```

* * *

### 3\. Update a Permission Scheme with HYCU required Permissions

Update the `update_permissions.ini` file with the group or user name:

```Python
[Target]
GROUP = GitProtectGroup
USER = 
```

Run the script with the permission scheme name:

```python
python update_permissions.py --scheme demo
```

Example Output:

```python
✅ Updated permission 'ADMINISTER_PROJECTS' for group 'GitProtectGroup'.  
✅ Updated permission 'BROWSE_PROJECTS' for group 'GitProtectGroup'.  
✅ Updated permission 'ADD_COMMENTS' for group 'GitProtectGroup'.  
✅ Updated permission 'ASSIGN_ISSUES' for group 'GitProtectGroup'.  
✅ Updated permission 'CREATE_ATTACHMENTS' for group 'GitProtectGroup'.  
✅ Updated permission 'CREATE_ISSUES' for group 'GitProtectGroup'.  
✅ Updated permission 'EDIT_ISSUES' for group 'GitProtectGroup'.  
✅ Updated permission 'LINK_ISSUES' for group 'GitProtectGroup'.  
✅ Updated permission 'MODIFY_REPORTER' for group 'GitProtectGroup'.  
✅ Updated permission 'MANAGE_WATCHERS' for group 'GitProtectGroup'.  
✅ Updated permission 'RESOLVE_ISSUES' for group 'GitProtectGroup'.  
✅ Updated permission 'SCHEDULE_ISSUES' for group 'GitProtectGroup'.  
✅ Updated permission 'VIEW_VOTERS_AND_WATCHERS' for group 'GitProtectGroup'.
```

* * *
