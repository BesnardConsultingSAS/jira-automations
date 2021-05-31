from typing import Any

from django import forms

from jira.jira_client import (
    get_all_jira_custom_fields,
    get_statuses,
)
from jira.models import JiraMapping


class JiraCustomFieldsMappingForm(forms.Form):
    status = forms.ChoiceField(label="Status", choices=[(None, "")], required=False)
    custom_field = forms.ChoiceField(
        label="Custom Field", choices=[(None, "")], required=False
    )

    def __init__(
        self,
        jira_mapping_instance: JiraMapping,
        *args: Any,
        **kwargs: dict,
    ) -> None:
        self.jira_mapping_instance = jira_mapping_instance
        self.available_statuses = get_statuses()
        self.available_custom_fields = list(get_all_jira_custom_fields())

        super().__init__(*args, **kwargs)

        self.fields["status"].initial = jira_mapping_instance.selected_status_id
        self.fields["custom_field"].initial = jira_mapping_instance.selected_field_id
        self.fields["status"].choices += [
            (status.id, f"{status.name} ({status.id})")
            for status in self.available_statuses
        ]
        self.fields["custom_field"].choices += [
            (custom_field.id, f"{custom_field.name} ({custom_field.id})")
            for custom_field in self.available_custom_fields
        ]

    def save(self) -> JiraMapping:
        self.jira_mapping_instance.selected_status_id = self.cleaned_data["status"]
        self.jira_mapping_instance.selected_field_id = self.cleaned_data["custom_field"]
        self.jira_mapping_instance.save()
        return self.jira_mapping_instance
