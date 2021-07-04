from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Room(models.Model):
    room = models.CharField(max_length=50, unique=True)
    user_admin = models.ForeignKey(User,on_delete=models.CASCADE)
    # Users who can join the chat Room
    approved_users = models.ManyToManyField(User, related_name='approved_users', blank=True)
    # Users on hold waiting to be approved to join the chat Room
    pending_requests = models.ManyToManyField(User, related_name='pending_requests', blank=True)
    is_private = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.room

    def get_approved_users(self):
        return self.approved_users.all()
    
    def get_pending_requests(self):
        return self.pending_requests.all()
    
    def save(self, *args, **kwargs):
        self.room = slugify(self.room)
        super(Room, self).save(*args, **kwargs)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username