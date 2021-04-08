from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def index(request):
    return render(request, template_name = 'index.html')

@login_required(login_url='login')
def chat(request):
    pass

@login_required(login_url='login')
def chat_room(request, room_name):
    return render(request,
            template_name = 'chat_room.html',
            context = {'room_name': room_name}
            )

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
