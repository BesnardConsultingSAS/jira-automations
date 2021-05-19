import pytest
from django.contrib.auth.models import User
from django.core.management import call_command


@pytest.mark.django_db
def test_create_user() -> None:
    call_command("create_user", "John", "my-password")

    users = User.objects.all()
    assert users.count() == 1
    user: User = users.first()
    assert set(user.get_all_permissions()) == {
        "jira.view_jiramapping",
        "jira.delete_jiramapping",
        "jira.add_jiramapping",
        "jira.change_jiramapping",
    }
    user.check_password("my-password")
