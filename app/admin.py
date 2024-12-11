from django.contrib import admin

from app.models import Login, Register, Election, Profile, Position, Vote, Candidate

# Register your models here.
admin.site.register(Login)
admin.site.register(Register)
admin.site.register(Election)
admin.site.register(Profile)

