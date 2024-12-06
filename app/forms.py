from django import forms
from django.core.exceptions import ValidationError

from app.models import Login, Register


class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = '__all__'

        widgets={
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'@Username','aria-label':'Username'}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password', 'aria-label':'Password'}),
        }

class RegisterForm(forms.ModelForm):
    class Meta:
        model =Register
        fields = '__all__'

        widgets={
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter your password'}),
            'confirm_password': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Re-enter your password'}),
            'age':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter your age'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError("The two password fields must match.")
        return cleaned_data