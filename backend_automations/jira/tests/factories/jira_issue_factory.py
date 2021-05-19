import factory
from factory.django import DjangoModelFactory

from jira.models import JiraIssue


class JiraIssueFactory(DjangoModelFactory):
    class Meta:
        model = JiraIssue

    key = factory.Sequence(lambda n: f"EXAMPLE-{n}")
    status_id = factory.Sequence(lambda n: f"customfield_{n}")
