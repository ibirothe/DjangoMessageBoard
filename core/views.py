from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Message

class MessageListView(ListView):
    model = Message
    template_name = "index.html"
    context_object_name = "messages"
    ordering = ["-created_at"]

class MessageCreateView(CreateView):
    model = Message
    fields = ["author", "text"]
    template_name = "add_message.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        if not form.cleaned_data.get("author"):
            form.instance.author = "Anonymous"
        return super().form_valid(form)
    
class MessageUpdateView(UpdateView):
    model = Message
    fields = ["author", "text"]
    template_name = "edit_message.html"
    success_url = reverse_lazy("index")

class MessageDeleteView(DeleteView):
    model = Message
    template_name = "delete_message.html"
    success_url = reverse_lazy("index")
