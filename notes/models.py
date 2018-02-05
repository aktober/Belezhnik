from django.db import models
from django.urls import reverse

from users.models import UserProfile


class Note(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notes:detail', args=[str(self.id)])