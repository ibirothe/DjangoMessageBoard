import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Message

@pytest.mark.django_db
def test_message_list_view(client):
    Message.objects.create(text="First msg", author="bob")
    resp = client.get(reverse("index"))
    assert resp.status_code == 200
    assert "First msg" in resp.content.decode()

@pytest.mark.django_db
def test_message_create_view_requires_login(client):
    resp = client.get(reverse("add_message"))
    assert resp.status_code == 302  # redirected to login

@pytest.mark.django_db
def test_message_create_view_logged_in(client):
    user = User.objects.create_user(username="bob", password="pw")
    client.login(username="bob", password="pw")
    resp = client.post(reverse("add_message"), {"text": "Created via test"}, follow=True)
    assert resp.status_code == 200
    assert Message.objects.filter(text="Created via test", author="bob").exists()

@pytest.mark.django_db
def test_toggle_like(client):
    user = User.objects.create_user(username="bob", password="pw")
    msg = Message.objects.create(text="Likeable", author="bob")
    client.login(username="bob", password="pw")
    resp = client.get(reverse("like_message", args=[msg.id]))
    msg.refresh_from_db()
    assert msg.likes.filter(username="bob").exists()
