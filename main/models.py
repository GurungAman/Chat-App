from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    room = models.CharField(max_length=50)

    def __str__(self):
        return self.room


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username
    
    def last_10_messages(self):
        return Message.objects.all().order_by('-timestamp')[:10]