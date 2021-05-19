from django.core.management.base import BaseCommand

from jira.views import update_jira_issues


class Command(BaseCommand):
    help = "Update Jira Issue target field"

    def handle(self, *args, **options):
        updated_issues = update_jira_issues()
        if updated_issues:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Updated Jira issues: {', '.join([issue.key for issue in updated_issues])}"
                )
            )
        else:
            self.stdout.write(self.style.SUCCESS(f"No Jira issues updated."))
