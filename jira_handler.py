import requests
import json
import os
from requests.auth import HTTPBasicAuth
from jira_commands import COMMANDS_TO_JIRA

API_TOKEN = os.getenv("API_TOKEN")
auth = HTTPBasicAuth("r.r.kabilan0435@gmail.com", API_TOKEN)

JIRA_URL = "https://kabilan10.atlassian.net/rest/api/3/issue"
headers = {"Accept": "application/json", "Content-Type": "application/json"}

def create_jira_issue(payload):
    issue_title = payload.get('issue', {}).get('title', 'No title provided')
    github_comment = payload.get('comment', {}).get('body', '')

    commands = [cmd for cmd in github_comment.split() if cmd in COMMANDS_TO_JIRA]
    created_issues = []

    for command in commands:
        jira_info = COMMANDS_TO_JIRA[command]
        key, issue_type = jira_info["key"], jira_info["issue_type"]

        payload = json.dumps({
            "fields": {
                "project": {"key": key},
                "issuetype": {"id": issue_type},
                "summary": issue_title,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [{"type": "paragraph", "content": [{"text": github_comment, "type": "text"}]}]
                }
            }
        })

        response = requests.request(
            "POST",  # Specify the method
            JIRA_URL, 
            data=payload, 
            headers=headers, 
            auth=auth
        )        
        created_issues.append(json.loads(response.text))

    return created_issues
