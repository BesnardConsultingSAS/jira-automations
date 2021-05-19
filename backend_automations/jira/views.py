from typing import List

from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from jira.forms import JiraCustomFieldsMappingForm
from jira import jira_client
from jira.models import JiraMapping, JiraIssue


@method_decorator(login_required, name="dispatch")
class JiraCustomFieldsMappingView(View):
    @method_decorator(permission_required("jira.view_jiramapping"), name="dispatch")
    def get(self, request: HttpRequest) -> HttpResponse:
        jira_mapping_instance, _ = JiraMapping.objects.get_or_create()
        form = JiraCustomFieldsMappingForm(jira_mapping_instance=jira_mapping_instance)
        return render(
            request,
            "jira/jira_custom_fields.html",
            {"form": form},
        )

    @method_decorator(permission_required("jira.change_jiramapping"), name="dispatch")
    def post(self, request: HttpRequest) -> HttpResponse:
        jira_mapping_instance, _ = JiraMapping.objects.get_or_create()
        form = JiraCustomFieldsMappingForm(
            jira_mapping_instance=jira_mapping_instance, data=request.POST
        )
        if form.is_valid():
            form.save()
            return redirect(
                request.META.get("HTTP_REFERER", "redirect_if_referer_not_found")
            )

        return render(
            request,
            "jira/jira_custom_fields.html",
            {"form": form},
        )


def refresh_jira_issues(jira_mapping_instance: JiraMapping) -> QuerySet[JiraIssue]:
    JiraIssue.objects.all().delete()
    jira_issues = jira_client.get_all_jira_issues()
    return JiraIssue.objects.bulk_create(
        [
            JiraIssue(
                key=jira_issue["key"],
                status_id=jira_issue["fields"]["status"]["id"],
                selected_field_value=jira_issue["fields"][
                    jira_mapping_instance.selected_field_id
                ],
            )
            for jira_issue in jira_issues
        ]  # type: ignore
    )


def update_jira_issues() -> List[JiraIssue]:
    jira_mapping_instance, _ = JiraMapping.objects.get_or_create()
    if (
        jira_mapping_instance.selected_field_id
        and jira_mapping_instance.selected_status_id
    ):
        refresh_jira_issues(jira_mapping_instance)

        jira_issues_to_update = JiraIssue.objects.filter(
            status_id=jira_mapping_instance.selected_status_id,
            selected_field_value__isnull=True,
        )

        jira_client.update_selected_field(
            jira_mapping_instance, list(jira_issues_to_update)
        )
        return list(jira_issues_to_update)
    return []


@method_decorator(login_required, name="dispatch")
class UpdateJiraIssuesView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        update_jira_issues()
        return redirect("custom-fields-mapping")
