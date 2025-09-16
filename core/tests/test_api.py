import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse
from core.models import Message

@pytest.mark.django_db
def test_list_messages_api():
    Message.objects.create(text="api test", author="bob")
    client = APIClient()
    resp = client.get(reverse("api_messages"))
    assert resp.status_code == 200
    assert resp.json()[0]["text"] == "api test"

@pytest.mark.django_db
def test_create_message_api_authenticated():
    user = User.objects.create_user(username="alice", password="pw")
    client = APIClient()
    client.login(username="alice", password="pw")
    resp = client.post(reverse("api_messages"), {"text": "new msg"}, format="json")
    assert resp.status_code == 201
    assert Message.objects.filter(text="new msg", author="alice").exists()

@pytest.mark.django_db
def test_like_api_toggle():
    user = User.objects.create_user(username="alice", password="pw")
    msg = Message.objects.create(text="toggle me", author="alice")
    client = APIClient()
    client.login(username="alice", password="pw")
    resp = client.post(reverse("api_message_like", args=[msg.id]))
    assert resp.status_code == 200
    data = resp.json()
    assert data["liked"] is True
    assert data["likes_count"] == 1
