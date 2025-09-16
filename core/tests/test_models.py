import pytest
from django.contrib.auth.models import User
from core.models import Message

@pytest.mark.django_db
def test_message_str_and_defaults():
    msg = Message.objects.create(text="Hello world")
    assert str(msg).startswith("Anonymous:")
    assert msg.author == "Anonymous"
    assert msg.created_at is not None

@pytest.mark.django_db
def test_total_likes():
    user = User.objects.create_user(username="alice", password="pw")
    msg = Message.objects.create(text="Like me!")
    msg.likes.add(user)
    assert msg.total_likes() == 1
