from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Book(models.Model):
    link=models.CharField(max_length=225)
    name=models.TextField()
    genre=models.TextField()
    audio=models.FileField()
    user=models.ForeignKey(User, null=True,blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name=models.TextField()

    def __str__(self):
        return self.name
