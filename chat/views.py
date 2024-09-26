from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
def chat_view(request):
    return TemplateView.as_view(template_name='chat_page/chat.html')(request)