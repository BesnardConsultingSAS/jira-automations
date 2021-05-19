import factory
from factory.django import DjangoModelFactory

from jira.models import JiraMapping


class JiraMappingFactory(DjangoModelFactory):
    class Meta:
        model = JiraMapping

    selected_field_id = factory.Sequence(lambda n: f"customfield_{n}")
    selected_status_id = factory.Sequence(lambda n: n)
