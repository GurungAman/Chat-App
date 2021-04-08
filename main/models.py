from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
    
    def last_10_messages(self):
        return message.objects.all().order_by('-timestamp')[:10]