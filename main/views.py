from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, template_name = 'index.html')

def chat(request):
    pass

def chat_room(request, room_name):
    return render(request,
    template_name = 'chat_room.html',
    context = {'room_name': room_name}
    )

def user_login(request):
    pass

def user_logout(request):
    pass