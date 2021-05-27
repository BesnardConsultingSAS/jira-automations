from unittest.mock import patch, MagicMock

import pytest
from django.test.client import Client
from django.contrib.auth.models import User, Permission

from accounts.tests.factories.user_factory import UserFactory
from jira.jira_client import CustomField, Status
from jira.models import JiraIssue
from jira.tests.factories.jira_mapping_factory import JiraMappingFactory
from jira.tests.get_all_jira_issues_mock import mocked_jira_issues


@patch(
    "jira.jira_client.get_all_jira_custom_fields",
    MagicMock(
        return_value=[CustomField(id="customfield_10073", name="To Review Date")]
    ),
)
@patch(
    "jira.jira_client.get_statuses",
    MagicMock(return_value=[Status(id=2313, name="Done Done (Merged)")]),
)
@pytest.mark.django_db
class TestJiraCustomFieldsView:
    def test_get_jira_custom_fields_view(self, client: Client) -> None:
        user: User = UserFactory()
        user.user_permissions.add(Permission.objects.get(codename="view_jiramapping"))
        client.force_login(user)

        response = client.get("/jira/custom-fields-mapping/")

        assert response.status_code == 200
        assert response.context["form"].available_custom_fields == [
            CustomField(id="customfield_10073", name="To Review Date")
        ]


@patch(
    "jira.jira_client.get_all_jira_issues",
    MagicMock(return_value=mocked_jira_issues),
)
@patch(
    "jira.webhooks_client.trigger_webhooks",
    MagicMock(),
)
@pytest.mark.django_db
class TestUpdateJiraIssueView:
    def test_update_jira_issue_view(
        self,
        client: Client,
    ) -> None:
        jira_mapping = JiraMappingFactory(
            selected_field_id="customfield_10074", selected_status_id=10065
        )
        user: User = UserFactory()
        client.force_login(user)

        with patch(
            "jira.jira_client.update_selected_field",
        ) as patched_update_selected_field:
            response = client.post("/jira/update-jira-issue/")

        assert response.status_code == 302
        assert response.headers["Location"] == "/jira/custom-fields-mapping/"
        assert JiraIssue.objects.count() == len(mocked_jira_issues)

        assert patched_update_selected_field.call_count == 1
        assert patched_update_selected_field.call_args_list[0][0] == (
            jira_mapping,
            [JiraIssue.objects.get(key="EXPROJ-4")],
        )
