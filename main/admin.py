from django.contrib import admin
from main.models import Message, Room

# Register your models here.
admin.site.register(Room)
admin.site.register(Message)