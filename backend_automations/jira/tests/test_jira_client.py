import pytest

from jira.jira_client import (
    get_all_jira_issues,
    get_all_jira_custom_fields,
    get_statuses,
    update_selected_field,
)


from jira.models import JiraIssue
from jira.tests.factories.jira_issue_factory import JiraIssueFactory
from jira.tests.factories.jira_mapping_factory import JiraMappingFactory


@pytest.mark.skip(
    "Calls the Jira API. Only uncommented for local development purposes."
)
def test_get_all_jira_issues() -> None:
    assert get_all_jira_issues() == []


@pytest.mark.skip(
    "Calls the Jira API. Only uncommented for local development purposes."
)
def test_get_all_jira_custom_fields() -> None:
    assert list(get_all_jira_custom_fields()) == []


@pytest.mark.skip(
    "Calls the Jira API. Only uncommented for local development purposes."
)
def test_get_statuses() -> None:
    assert get_statuses() == []


@pytest.mark.skip(
    "Calls the Jira API. Only uncommented for local development purposes."
)
@pytest.mark.django_db
def test_update_selected_field() -> None:
    jira_mapping = JiraMappingFactory(
        selected_field_id="customfield_10074", selected_status_id=10065
    )
    issue: JiraIssue = JiraIssueFactory(key="EXPROJ-4", status_id="customfield_10074")
    update_selected_field(jira_mapping, [issue])
