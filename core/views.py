from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Message
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ["text"]
    template_name = "add_message.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user.username
        else:
            form.instance.author = "Anonymous"
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = "login.html"

    def get_success_url(self):
        return reverse_lazy("index")

class UserLogoutView(LogoutView):
    def get_next_page(self):
        return reverse_lazy("index")

class MessageListView(ListView):
    model = Message
    template_name = "index.html"
    context_object_name = "messages"
    ordering = ["-created_at"]
    
class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ["text"]
    template_name = "edit_message.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        if form.instance.author != self.request.user.username:
            return self.handle_no_permission()
        return super().form_valid(form)

class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "delete_message.html"
    success_url = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user.username and not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

@login_required
def toggle_like(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.user in message.likes.all():
        message.likes.remove(request.user)
    else:
        message.likes.add(request.user)
    return redirect("index")