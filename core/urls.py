from django.urls import path
from .views import (
    MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView,
    UserLoginView, UserLogoutView, toggle_like,
    MessageListAPI, MessageDetailAPI, MessageLikeAPI
)

urlpatterns = [
    # Web views
    path("", MessageListView.as_view(), name="index"),
    path("add/", MessageCreateView.as_view(), name="add_message"),
    path("edit/<int:pk>/", MessageUpdateView.as_view(), name="edit_message"),
    path("delete/<int:pk>/", MessageDeleteView.as_view(), name="delete_message"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("like/<int:pk>/", toggle_like, name="like_message"),

    # API endpoints
    path("api/messages/", MessageListAPI.as_view(), name="api_messages"),
    path("api/messages/<int:pk>/", MessageDetailAPI.as_view(), name="api_message_detail"),
    path("api/messages/<int:pk>/like/", MessageLikeAPI.as_view(), name="api_message_like"),
]
