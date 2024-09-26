from django.db import models
from django.contrib.auth.models import User as AuthUser
from login.models import *
from home.models import Ride

class Chat(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='chats')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat in Ride {self.ride.id}: {self.sender.username}"