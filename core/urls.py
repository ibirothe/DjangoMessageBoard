from django.urls import path
from .views import MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView

urlpatterns = [
    path("", MessageListView.as_view(), name="index"),
    path("add/", MessageCreateView.as_view(), name="add_message"),
    path("edit/<int:pk>/", MessageUpdateView.as_view(), name="edit_message"),
    path("delete/<int:pk>/", MessageDeleteView.as_view(), name="delete_message"),
]
