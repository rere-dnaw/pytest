import json
from unittest.mock import patch

from django.core import mail
from django.test import TestCase, Client
from blockchain.views import send_email
from pytest_refresh.settings import EMAIL_HOST_USER


# class EmailTest(TestCase):
def test_send_email_success(mailoutbox, settings) -> None:
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    assert len(mailoutbox) == 0
    mail.send_mail(
        subject="Email subject",
        message="Email body",
        from_email="test@email.com",
        recipient_list=["recipient@email.com"],
        fail_silently=False,
    )
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == "Email subject"
    assert mailoutbox[0].body == "Email body"


def test_post_email_no_arguments(client):
    with patch("blockchain.views.send_email") as mocked_send_email:
        response = client.post(path="/send_email")
        assert response.status_code == 200
        response_content = json.loads(response.content)
        print(response_content)
        assert response_content["status"] == "success"
        assert response_content["info"] == "email sent successfully"


def test_get_email_no_args_should_fail(client):
    response = client.get(path="/send_email")
    assert response.status_code == 405
    assert json.loads(response.content) == {"detail": 'Method "GET" not allowed.'}
