from django.core.checks import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from main.models import Room
import json
from .permission_decorator import check_permission
from django.core.paginator import Paginator

from .forms import RegisterUser

# Create your views here.
@login_required(login_url='login')
def index(request):
    rooms_created = Room.objects.filter(user_admin = request.user)
    user = User.objects.get(username = request.user.username)
    all_rooms_joined = user.approved_users.all()
    rooms_joined = []
    for room in all_rooms_joined:
        if room not in rooms_created:
            rooms_joined.append(room)
    return render(request,
                template_name = 'index.html',
                context={'rooms_created': rooms_created,
                        'rooms_joined': rooms_joined})


@login_required(login_url='login')
@check_permission
def accept_pending_requests(request):
    response = {'status': False}
    json_str = request.body.decode(encoding='UTF-8')
    data_json = json.loads(json_str)
    try:
        room = Room.objects.get(room=data_json['room_name'])
        if data_json['accept_all']:
            print("accpet all")
            pending_request = room.get_pending_requests()
            for user in pending_request:
                room.approved_users.add(user)
                room.pending_requests.remove(user)
                messages.info(request, "All requests accepted.")
        else:
            print(f"Accept {data_json['user']} request")
            user =  User.objects.get(username=data_json['user'])
            room.pending_requests.remove(user)
            room.approved_users.add(user)
        response['status'] = True
        return JsonResponse(response)
    except Exception as e:
        messages.info(request, "Something went wrong")
        response['error'] = f'{e.__class__.__name__}'
        return JsonResponse(response)


@login_required(login_url='login')
@check_permission
def reject_incoming_request(request):
    response = {'status': False}
    json_str = request.body.decode(encoding='UTF-8')
    data_json = json.loads(json_str)
    try:
        room = Room.objects.get(room=data_json['room_name'])
        user = User.objects.get(username=data_json['user'])
        room.pending_requests.remove(user)
        response['status'] = True
        return JsonResponse(response)
    except Exception as e:
        messages.info(request, "Something went wrong")
        response['error'] = f'{e.__class__.__name__}'
        return JsonResponse(response)


@login_required(login_url='login')
@check_permission
def edit_room(request, room_name):
    room = Room.objects.get(room=room_name)
    pending_requests = room.get_pending_requests()
    approved_users = room.get_approved_users()
    approved_user = []    
    for user in approved_users:
        if user !=  request.user:
            approved_user.append(user)
    return render(request,
                template_name = "edit_room.html", 
                context = {'room': room,
                            'pending_requests': pending_requests,
                            'approved_user': approved_user})


@login_required(login_url='login')
@check_permission
def change_room_type(request):
    response = {'status': False}
    json_str = request.body.decode(encoding='UTF-8')
    data_json = json.loads(json_str)
    try:
        room = Room.objects.get(room=data_json['room_name'])
        room.is_public = data_json['is_public']
        room.is_private = data_json['is_private']
        room.save()
        if room.is_public:
            for user in room.get_pending_requests():
                room.approved_users.add(user)
                room.pending_requests.remove(user)
        messages.info(request, "Room type successfully changed.!")
        response['status'] = True
        return JsonResponse(response)
    except Exception as e:
        response['error'] = f'{e.__class__.__name__}'
        return JsonResponse(response)


@login_required(login_url='login')
@check_permission
def remove_from_chat_room(request):
    response ={"status": False}
    json_str = request.body.decode(encoding="UTF-8")
    data_json = json.loads(json_str)
    try:
        room = Room.objects.get(room=data_json['room_name'])
        user = User.objects.get(username=data_json['user'])
        room.approved_users.remove(user)
        response['status'] = True
        return JsonResponse(response)    
    except Exception as e:
        messages.info(request, "An Error Occured")
        response['error'] = f'{e.__class__.__name__}'
        return JsonResponse(response)


@login_required(login_url='login')
@check_permission
def add_user(request):
    response ={"status": False}
    json_str = request.body.decode(encoding="UTF-8")
    data_json = json.loads(json_str)
    try:
        room = Room.objects.get(room=data_json['room_name'])
        user = User.objects.get(username=data_json['username'])
        
        if user in room.approved_users.all():
            messages.info(request, f"{user} is already in this room.!")
            return JsonResponse(response)
        room.approved_users.add(user)
        if user in room.pending_requests.all():
            room.pending_requests.remove(user)
        
        response['status'] = True
        return JsonResponse(response)    
    except Exception as e:
        messages.info(request, f'Error: {e.__class__.__name__}')
        response['error'] = f'{e.__class__.__name__}'
        return JsonResponse(response)


@login_required(login_url='login')
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


@login_required(login_url='login')
def join_chat_room(request):
    response_json = {'status': False}
    json_str = request.body.decode(encoding='UTF-8')
    data_json = json.loads(json_str)
    user = request.user
    try:
        room = Room.objects.get(room=data_json['room_name'])
        response_json['status'] = True
        if request.user in room.approved_users.all():
            messages.info(request, "You have already joined this room.")
            return redirect('homepage')
        if room.is_public:
            room.approved_users.add(user)
            response_json['public_room'] = True
            messages.info(request, f"Welcome to {room}")
            return JsonResponse(response_json)
        elif room.is_private:
            room.pending_requests.add(user)
            response_json['private_room'] = True
            messages.info(request, f"Your request to join room {room} is on hold.!")
            return JsonResponse(response_json)
    except Exception as e:
        response_json['error'] = f'{e.__class__.__name__}'
        return JsonResponse(response_json)


@login_required(login_url='login')
def leave_room(request):
    response = {'status': False}
    json_str = request.body.decode(encoding='UTF-8')
    data_json = json.loads(json_str)
    room_name = data_json['room_name']
    current_user = request.user
    try:
        room = Room.objects.get(room=room_name)
        user_admin = room.user_admin
        if user_admin is not current_user:
            room.approved_users.remove(current_user)
        else:
            response['user_admin'] = True
        response['status'] = True
        return JsonResponse(response)
    except Exception as e:
        response['error'] = f'{e.__class__.__name__}'
        return JsonResponse(response)


@login_required(login_url='login')
def chat_room(request, room_name):
    room = Room.objects.get(room=room_name)
    from django.conf import settings
    debug = settings.DEBUG
    if request.user not in room.approved_users.all() and room.is_private:
        return redirect('homepage')
    return render(request,
            template_name = 'chat_room.html',
            context = {'room_name': room_name,
            'debug': debug})


@login_required(login_url='login')
def get_messages(request):
    try:
        response = {'status': False}
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        room = Room.objects.get(room=data_json['room_name'])
        approved_users = room.get_approved_users()
        user = request.user
        if room.is_private and user not in approved_users:
            messages.info(request, "Not allowed")
            return redirect("homepage")
        else:
            message_list = room.message_set.order_by('-timestamp')
            paginator = Paginator(message_list, 15)
            page_obj = paginator.page(data_json['page_number'])

            response['data'] = []
            for data in page_obj.object_list:
                response['data'].append({
                    'user': data.user.username,
                    'message': data.content,
                    'timestamp': data.timestamp
                })
            response['status'] = True

            return JsonResponse(response)
    except Exception as e:
        response['error'] = f'{e.__class__.__name__}'
        return JsonResponse(response)


def user_login(request):
    if not request.user.is_anonymous:
        return redirect('homepage')
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

def user_register(request):
    if not request.user.is_anonymous:
        return redirect('homepage')
    form = RegisterUser
    if request.method == "POST":
        form = RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("homepage")
    return render(request,
                template_name='register.html', 
                context = {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.!")
    return redirect("login")