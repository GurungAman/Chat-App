from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.models import Room, Message


# Create your views here.
@login_required(login_url='login')
def index(request):
    if request.method == "POST":
        room_name = request.POST['room-name-input']
        room_name = room_name.strip()
        if room_name == "":
            messages.info(request, "Room Name cannot be empty.!")
            return redirect('homepage')
        room, _ = Room.objects.get_or_create(room=room_name)
        return redirect(chat_room, room_name=room)
    return render(request, template_name = 'index.html')


@login_required(login_url='login')
def chat_room(request, room_name):
    try:
        room = Room.objects.get(room=room_name)
        message = reversed(room.message_set.order_by('-timestamp')[:15])
    except:
        messages.info(request, "Room Does not exist!")
        return redirect('homepage')
    return render(request,
            template_name = 'chat_room.html',
            context = {'room_name': room_name,
                        'message': message
                        })


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("homepage")
        else:
            return render(request=request, 
                    template_name="log_in.html",
                    context={"error_message": "Invalid credentials.!"})
    return render(request, template_name="log_in.html")
