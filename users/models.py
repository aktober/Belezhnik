from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.CharField(max_length=256, default='')
    picture = models.ImageField(upload_to='profile_pics', null=True, blank=True)

    def __str__(self):
        return self.user.username
