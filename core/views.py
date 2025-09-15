from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Message
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import generics, permissions
from .serializers import MessageSerializer
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import MessageSerializer
from .models import Message

class MessageListView(ListView):
    model = Message
    template_name = "index.html"
    context_object_name = "messages_list"   # <-- avoid conflict with Django's messages
    ordering = ["-created_at"]
    paginate_by = 10  # optional: paginates your list, remove if you don't want pagination


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ["text"]
    template_name = "add_message.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.author = self.request.user.username
        messages.success(self.request, "Message created successfully!")
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ["text"]
    template_name = "edit_message.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        # Prevent editing others' messages
        if form.instance.author != self.request.user.username:
            return self.handle_no_permission()
        messages.success(self.request, "Message updated successfully!")
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "delete_message.html"
    success_url = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user.username and not request.user.is_superuser:
            return self.handle_no_permission()
        messages.success(self.request, "Message deleted successfully!")
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(LoginView):
    template_name = "login.html"

    def get_success_url(self):
        # respect ?next= if present, else go home
        messages.success(self.request, f"Welcome back, {self.request.user.username}!")
        return self.get_redirect_url() or reverse_lazy("index")


class UserLogoutView(LogoutView):
    def get_next_page(self):
        messages.info(self.request, "You have been logged out.")
        return reverse_lazy("index")


@login_required
def toggle_like(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.user in message.likes.all():
        message.likes.remove(request.user)
        messages.info(request, "You unliked a message.")
    else:
        message.likes.add(request.user)
        messages.success(request, "You liked a message.")
    return redirect("index")

class MessageListAPI(generics.ListCreateAPIView):
    queryset = Message.objects.all().order_by("-created_at")
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.username)


class MessageDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MessageLikeAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        user = request.user
        liked = False

        if user in message.likes.all():
            message.likes.remove(user)
            liked = False
        else:
            message.likes.add(user)
            liked = True

        return Response(
            {
                "id": message.id,
                "likes_count": message.likes.count(),
                "liked": liked,
            },
            status=status.HTTP_200_OK,
        )