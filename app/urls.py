"""
URL configuration for dVoting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app import views
from app.views import delete_election

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create_election/', views.create_election, name='create_election'),
    path('edit_election/<int:election_id>/', views.edit_election, name='edit_election'),
    path('delete_election/<int:election_id>/', delete_election, name='delete_election'),
    path('add_candidates/<int:election_id>/', views.add_candidates, name='add_candidates'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('vote/<int:election_id>/', views.vote_view, name='vote_form'),
    path('vote/', views.vote_dashboard, name='vote'),
    path('voting_history/', views.voting_history, name='voting_history'),
]


