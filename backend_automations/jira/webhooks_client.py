import requests

from backend_automations import settings
from jira.models import JiraIssue


def trigger_webhooks(jira_issue: JiraIssue) -> None:
    for webhook_url in settings.WEBHOOK_URLS_TO_TRIGGER:
        requests.post(webhook_url, json={"key": jira_issue.key})
