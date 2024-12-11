from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from app.models import Login, Register, Election, Candidate, Profile, Position


class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = '__all__'

        widgets={
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'@Username','aria-label':'Username'}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password', 'aria-label':'Password'}),
        }

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter your password'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("The two password fields must match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # This hashes the password
        if commit:
            user.save()
        return user



class ElectionForm(forms.ModelForm):
    elected_positions = forms.ModelMultipleChoiceField(queryset=Position.objects.all(), required=False)

    class Meta:
        model = Election
        fields = ['name', 'description', 'status', 'election_for']


class PositionForm(forms.Form):
    position_name = forms.CharField(max_length=255)
    candidates = forms.CharField(widget=forms.Textarea, help_text="Enter up to 3 candidates separated by commas.")

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'profile', 'age']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    profile_picture = forms.ImageField(required=False, label="Profile Picture")
    phone = forms.CharField(max_length=15, required=False, label="Phone Number")
    address = forms.CharField(widget=forms.Textarea, required=False, label="Address")

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        # Add custom styling
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })