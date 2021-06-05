from django.core.checks import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from main.models import Room, Message
import json


# Create your views here.
def is_public_room(room_name):
    room = Room.objects.get(room=room_name)
    if room.is_public:
        return True
    else:
        return False

def approve_pending_requests(room_name, users):
    room = Room.objects.get(room=room_name)
    pending_users = room.get_pending_requests()
    for user in users:
        if user in pending_users:
            room.pending_requests.remove(user)
            room.approved_users.add(user)


def create_chat_room(request):
    json_str = request.body.decode(encoding='UTF-8')
    data_json = json.loads(json_str)
    user = request.user
    response_json = {'status': False}
    try:
        room = Room.objects.create(
            room = data_json['room_name'],
            user_admin = user,
            is_public = data_json['is_public'],
            is_private = data_json['is_private']
        )
        room.approved_users.add(user)
        response_json['status'] = True
        messages.info(request, f'Room {room.room} created successfully by {room.user_admin}')
        return JsonResponse(response_json)
    except Exception as e:
        response_json['error'] = f'{e.__class__.__name__}'
        return JsonResponse(response_json)

def join_chat_room(request):
    response_json = {'status': False}
    json_str = request.body.decode(encoding='UTF-8')
    data_json = json.loads(json_str)
    user = request.user
    try:
        room = Room.objects.get(room=data_json['room_name'])
        response_json['status'] = True
        if room.is_public:
            room.approved_users.add(user)
            response_json['public_room'] = True
            return JsonResponse(response_json)
        elif room.is_private:
            room.pending_requests.add(user)
            response_json['private_room'] = True
            return JsonResponse(response_json)
    except Exception as e:
        response_json['error'] = f'{e.__class__.__name__}'
        return JsonResponse(response_json)

@login_required(login_url='login')
def index(request):
    rooms_created = Room.objects.filter(user_admin = request.user)
    user = User.objects.get(username = request.user.username)
    all_rooms_joined = user.approved_users.all()
    rooms_joined = []
    for room in all_rooms_joined:
        if not room in rooms_created:
            rooms_joined.append(room)
    return render(request,
                template_name = 'index.html',
                context={'rooms_created': rooms_created,
                        'rooms_joined': rooms_joined})


@login_required(login_url='login')
def chat_room(request, room_name):
    try:
        room = Room.objects.get(room=room_name)
        user = request.user
        message = reversed(room.message_set.order_by('-timestamp')[:15])
    except Exception as e:
        messages.info(request, "Room Does not exist!")
        return redirect('homepage')
    return render(request,
            template_name = 'chat_room.html',
            context = {'room_name': room_name,
                        'message': message
                        })

def leave_room(request):
    response = {'status': False}
    json_str = request.body.decode(encoding='UTF-8')
    data_json = json.loads(json_str)
    room_name = data_json['room']
    current_user = request.user
    try:
        room = Room.objects.get(room=room_name)
        user_admin = room.user_admin
        if user_admin != current_user:
            room.approved_users.remove(current_user)
        else:
            response['user_admin'] = True
        response['status'] = True
    except Exception as e:
        response['error'] = f'{e.__class__.__name__}'
    return JsonResponse(response)


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
