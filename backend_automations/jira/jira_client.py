from datetime import datetime
from typing import List, Callable

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


def get_filter_custom_fields_function(project_id: int) -> Callable[[dict], bool]:
    def filter_function(field: dict) -> bool:
        return (
            field["id"].startswith("customfield_")
            and "project" in field.get("scope", {})
            and field["scope"]["project"]["id"] == project_id
        )

    return filter_function


def get_all_jira_custom_fields() -> List[CustomField]:
    project_id = get_jira_project_id()
    filter_custom_fields_function = get_filter_custom_fields_function(project_id)
    response = requests.get(
        f"https://{settings.JIRA_DOMAIN}/rest/api/2/field",
        auth=HTTPBasicAuth(settings.JIRA_USERNAME, settings.JIRA_TOKEN),
    )
    assert response.status_code == 200, response.json()
    return parse_obj_as(
        List[CustomField], list(filter(filter_custom_fields_function, response.json()))
    )


def get_jira_project_id() -> int:
    response = requests.get(
        f"https://{settings.JIRA_DOMAIN}/rest/api/2/project/{settings.JIRA_BOARD}",
        auth=HTTPBasicAuth(settings.JIRA_USERNAME, settings.JIRA_TOKEN),
    )
    assert response.status_code == 200, response.json()
    return response.json()["id"]


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
