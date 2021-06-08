"""ChatApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('login/', views.user_login, name='login'),
    path('create_chat_room/', views.create_chat_room, name='create_chat_room'),
    path('join_chat_room/', views.join_chat_room, name='join_chat_room'),
    path('edit_room/<slug:room_name>', views.edit_room, name='edit_room'),
    path('change_room_type/', views.change_room_type, name='change_room_type'),
    path('remove_from_chat/', views.remove_from_chat_room, name='remove_from_chat_room'),
    path('check_user/', views.check_user, name='check_user'),
    path('accept_pending_request/', views.accept_pending_requests, name='accept_pending_requests'),
    path('reject_incoming_request/', views.reject_incoming_request, name='reject_incoming_request'),
    path('chat/<slug:room_name>/', views.chat_room, name='chat_room'),
    path('leave_room/', views.leave_room, name='leave_room'),
]
