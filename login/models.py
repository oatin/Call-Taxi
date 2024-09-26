from django.db import models
from django.contrib.auth.models import User as AuthUser, AbstractUser
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('passenger', 'ผู้โดยสาร'),
        ('driver', 'คนขับ'),
    ]
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_driver = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='passenger')

    def __str__(self):
        return self.username

    class Meta:
        permissions = [
            ("can_view", "Can view user"),
        ]