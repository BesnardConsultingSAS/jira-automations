from django.urls import path

from jira.views import JiraCustomFieldsMappingView, UpdateJiraIssuesView

urlpatterns = [
    path(
        "custom-fields-mapping/",
        JiraCustomFieldsMappingView.as_view(),
        name="custom-fields-mapping",
    ),
    path(
        "update-jira-issue/",
        UpdateJiraIssuesView.as_view(),
        name="update-jira-issue",
    ),
]
