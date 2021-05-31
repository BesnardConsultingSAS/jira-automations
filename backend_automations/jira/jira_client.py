from datetime import datetime
from typing import List, Generator

import requests
from django.conf import settings
from pydantic import BaseModel, parse_obj_as
from requests.auth import HTTPBasicAuth

from jira.models import JiraIssue, JiraMapping


def get_all_jira_issues() -> list:
    start_at = 0
    total = 0
    issues = []
    while total >= start_at:
        response = requests.get(
            f"https://{settings.JIRA_DOMAIN}/rest/api/latest/search",
            {
                "jql": f"project = {settings.JIRA_BOARD} ORDER BY created DESC",
                "startAt": start_at,
            },  # type: ignore
            auth=HTTPBasicAuth(settings.JIRA_USERNAME, settings.JIRA_TOKEN),
        )
        assert response.status_code == 200, response.json()
        issues += response.json()["issues"]
        start_at += response.json()["maxResults"]
        total = response.json()["total"]
    assert (
        len(issues) == total
    ), f"issues={len(issues)}, total={total}, start_at={start_at}"
    return issues


class CustomField(BaseModel):
    id: str
    name: str


def get_all_jira_custom_fields() -> Generator[CustomField, None, None]:
    response = requests.get(
        f"https://{settings.JIRA_DOMAIN}/rest/api/2/issue/createmeta?projectKeys={settings.JIRA_BOARD}&expand=projects.issuetypes.fields",
        auth=HTTPBasicAuth(settings.JIRA_USERNAME, settings.JIRA_TOKEN),
    )
    assert response.status_code == 200, response.json()
    issuetypes = response.json()["projects"][0]["issuetypes"]

    # Nested loop with if, we could parse it better but let's say it's fine for now
    for issuetype in issuetypes:
        for field_id, field in issuetype["fields"].items():
            if field_id.startswith("customfield_"):
                yield CustomField(id=field_id, name=field["name"])


class Status(BaseModel):
    id: int
    name: str


def get_statuses() -> List[Status]:
    response = requests.get(
        f"https://{settings.JIRA_DOMAIN}/rest/api/2/project/{settings.JIRA_BOARD}/statuses",
        auth=HTTPBasicAuth(settings.JIRA_USERNAME, settings.JIRA_TOKEN),
    )
    assert response.status_code == 200, response.json()
    statuses = response.json()[0]["statuses"]
    return parse_obj_as(List[Status], statuses)


def update_selected_field(jira_mapping: JiraMapping, issues: List[JiraIssue]) -> None:
    for issue in issues:
        response = requests.put(
            f"https://{settings.JIRA_DOMAIN}/rest/api/2/issue/{issue.key}/",
            json={
                "fields": {jira_mapping.selected_field_id: datetime.now().isoformat()}
            },
            auth=HTTPBasicAuth(settings.JIRA_USERNAME, settings.JIRA_TOKEN),
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 204
