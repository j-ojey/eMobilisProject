from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EditProfileForm, PositionForm

from app.forms import RegisterForm, ElectionForm, ProfileUpdateForm, UserUpdateForm
from app.models import Election, Candidate, Vote, Profile, Position


# Create your views here.
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Profile  # Assuming you have a Profile model


def custom_login(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)

            login(request, user)

            # Check if the user is an admin or a regular user
            if user.is_staff:
                return redirect('admin_dashboard')  # Redirect to admin dashboard if admin
            else:
                return redirect('user_dashboard')  # Redirect to user dashboard if not an admin

        else:
            error_message = "Invalid username or password. Please try again."
            return render(request, 'login.html', {'form': form, 'error': error_message})

    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
            form = RegisterForm()
    return render(request, 'register.html' , {'form':form})

@login_required
def dashboard(request):
    active_votes = Election.objects.filter(status='open').order_by('created_at')  # Or any other sorting criteria

    voting_history = Vote.objects.filter(user=request.user).order_by('-timestamp')  # Fetch voting history

    return render(request, 'dashboard.html', {
        'voting_history': voting_history,
        'active_votes': active_votes,
    })


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    return render(request, 'logout.html')

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html',{'user':request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EditProfileForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'edit_profile.html', context)



def index(request):
    return render(request, 'index.html')


'''Admin DashBoard'''
@login_required()
def admin_dashboard(request):
    registered_users = User.objects.count()
    active_elections = Election.objects.filter(status='open').count()
    votes_cast = Vote.objects.count()
    elections = Election.objects.all()
    users = User.objects.all()

    context = {
        'registered_users':registered_users,
        'active_elections':active_elections,
        'votes_cast': votes_cast,
        'elections':elections,
        'users':users,
    }
    return render(request, 'admin_dashboard.html', context)

#Create Election
def create_election(request):
    if request.method == 'POST':
        election_form = ElectionForm(request.POST)

        if election_form.is_valid():
            # Save the election
            election = election_form.save(commit=False)
            election.created_by = request.user  # Set the user who created the election
            election.save()  # Save the election instance

            elected_positions = election_form.cleaned_data.get('elected_positions')
            if elected_positions:
                election.elected_positions.set(elected_positions)  # Set the positions if selected
                election.save()

            # Redirect to the admin dashboard
            messages.success(request, "Election created successfully!")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        election_form = ElectionForm()

    return render(request, 'create_election.html', {'election_form': election_form})

# Add candidates to an election
def add_candidates(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    candidates = Candidate.objects.filter(election=election)

    if request.method == 'POST':
        for candidate in candidates:
            candidate_name = request.POST.get(f'name_{candidate.id}')
            if candidate_name:
                candidate.name = candidate_name
                candidate.save()
        messages.success(request, "Candidates added successfully!")
        return redirect('admin_dashboard')

    return render(request, 'add_candidates.html', {'election': election, 'candidates': candidates})





# Edit Election
def edit_election(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    candidates = election.candidates.all()  # Get all candidates associated with the election

    if request.method == 'POST':
        if 'election_form' in request.POST:
            # Handle updating election details
            election.name = request.POST['name']
            election.description = request.POST['description']
            election.status = request.POST['status']
            election.save()
            messages.success(request, 'Election updated successfully!')
            return redirect('admin_dashboard')

        elif 'candidate_form' in request.POST:
            # Handle adding new candidate
            candidate_name = request.POST['name']
            candidate_position = request.POST['position']
            Candidate.objects.create(
                election=election,
                name=candidate_name,
                position=candidate_position
            )
            messages.success(request, 'Candidate added successfully!')
            return redirect('edit_election', election_id=election.id)

    context = {'election': election, 'candidates': candidates}
    return render(request, 'edit_election.html', context)


# Delete Election
def delete_election(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    election.delete()
    messages.success(request, 'Election deleted successfully!')
    return redirect('admin_dashboard')



@login_required
def vote_view(request, election_id):
    # Get the election and related candidates
    election = get_object_or_404(Election, id=election_id)
    candidates = Candidate.objects.filter(election=election)

    if request.method == 'POST':
        # Process the voting
        for position in election.elected_positions.all():
            candidate_id = request.POST.get(f'candidate_{position}')
            if candidate_id:
                candidate = get_object_or_404(Candidate, id=candidate_id)
                # Create a new vote record in the database
                Vote.objects.create(user=request.user, election=election, candidate=candidate)
                messages.success(request, f"Vote casted for {candidate.name} in {position} position.")

        # After voting, redirect to the dashboard or another page
        return redirect('dashboard')  # Replace with the desired redirect

    context = {
        'election': election,
        'candidates': candidates,
    }
    return render(request, 'vote_form.html', context)


def vote_dashboard(request):
    elections = Election.objects.filter(status='open')
    return render(request, 'vote.html', {'elections': elections})


def voting_history(request):
    # Ensure the user is logged in
    if request.user.is_authenticated:
        # Fetch the voting history for the logged-in user
        votes = Vote.objects.filter(user=request.user).order_by('-timestamp')
        return render(request, 'voting_history.html', {'votes': votes})
    else:
        return redirect('login')