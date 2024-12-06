from django import forms
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Login(models.Model):
    username =  models.CharField(max_length=25, null=False)
    password = models.CharField(max_length=128, null=False)

    '''Constructor to return something from the class'''
    def __str__(self):
        return self.username

class Register(models.Model):
    username = models.CharField(max_length=25, null=False)
    email = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=128, null=False)
    confirm_password = models.CharField(max_length=128, null=False)
    age = models.IntegerField(null=True)


    '''Constructor'''
    def __str__(self):
        return self.email



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.ImageField(upload_to='profile_pictures/', default='default.jpg')
    age =  models.IntegerField(null=True)

    def __str__(self):
        return self.user.age