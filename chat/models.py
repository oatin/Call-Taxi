from django.db import models
from django.contrib.auth.models import User as AuthUser

class Chat(models.Model):
    sender = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='sent_chats')
    receiver = models.ForeignKey('TaxiDriver', on_delete=models.CASCADE, related_name='received_chats')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat({self.sender.username} -> {self.receiver.user.username}): {self.message}"
