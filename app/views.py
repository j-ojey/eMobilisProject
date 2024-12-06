from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from app.forms import RegisterForm
from app.models import Profile


# Create your views here.
def custom_login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/app/index/')  # Redirect to the dashboard
        else:
            error_message = "Invalid username or password. Please try again."
            return render(request, 'login.html', {'form': form, 'error': error_message})

    return render(request, 'login.html', {'form': form})

    # form = LoginForm()
    # return render(request, 'login.html',{'form':form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
            form = RegisterForm()
    return render(request, 'register.html' , {'form':form})

@login_required
def index(request):
    return render(request, 'index.html')


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    return render(request, 'logout.html')

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html',
                  {
                      'username':user.username,
                      'email':user.email,
                  })