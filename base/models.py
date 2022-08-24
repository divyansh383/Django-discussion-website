from distutils.command.upload import upload
from email.policy import default
from pydoc import describe
from tkinter import CASCADE
from turtle import update
from django.db import models
from django.test import modify_settings
from matplotlib.backend_bases import MouseEvent
from sympy import N
from django.contrib.auth.models import User
# Create your models here. db here
#classes re tbles, ttributes re cols
class profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    bio=models.TextField(null=True,blank=True)
    pp=models.ImageField(default='default.jpg',upload_to='propics')
    def __str__(self):
        return str(self.user.username)


class Topic(models.Model):
    name=models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.name)

class Room(models.Model):
    host=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True)
    participants=models.ManyToManyField(User,related_name="participants",blank=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-updated','-created']
    def __str__(self):
        return str(self.name)

class Message(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    room=models.ForeignKey(Room, on_delete=models.CASCADE)
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-updated','-created']
    def __str__(self):
        return str(self.body[0:50])
    