from datetime import datetime

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
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(max_length=21, blank=True, null=True)
    profile = models.ImageField(upload_to='profile_pictures/', default='default.jpg')
    age =  models.IntegerField(null=True)

    def __str__(self):
        return self.user.username


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class Election(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=[('open', 'Open'), ('closed', 'Closed')])
    election_for = models.CharField(max_length=100, blank=True)  # What the election is for
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='created_elections', null=True)
    elected_positions = models.ManyToManyField(Position, blank=True)

    def __str__(self):
        return self.name




class Candidate(models.Model):
    election = models.ForeignKey(Election, related_name='candidates', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)  # Candidate's name
    position = models.CharField(max_length=100)  # Position the candidate is running for

    def __str__(self):
        return f"{self.name} - {self.position}"



class Vote(models.Model):
    election = models.ForeignKey(Election, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.user.username} voted for {self.candidate.name}"


