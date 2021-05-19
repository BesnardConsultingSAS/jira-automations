from django.db import models


class JiraIssue(models.Model):
    key = models.TextField(unique=True)
    status_id = models.TextField()
    selected_field_value = models.DateTimeField(null=True, blank=True)


class JiraMapping(models.Model):
    selected_field_id = models.TextField(null=True, blank=True)
    selected_status_id = models.IntegerField(null=True, blank=True)
