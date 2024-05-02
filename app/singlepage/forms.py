from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator
from singlepage.models import User
from django.forms import ImageField, FileInput
from django.forms.widgets import ClearableFileInput

# Form for the login page with username and password fields and a submit button
############################################################################################################
class UsernamesForm(forms.Form):        
    usernames = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': "form-control placeholder-style",
            'placeholder': "Nom d'utilisateur",
            'style': 'background-color: rgba(198, 182, 182, 0.1); border: none; border-radius: 7px; color: white;',
            }),
        required=True,
        max_length=100,
        min_length=1,
        strip=True,
        error_messages={'required': 'Veuillez entrer au moins un nom d’utilisateur'}
    )


class PasswordForm(forms.Form):
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': "form-control placeholder-style",
            'placeholder': "Mot de passe",
            'style': 'background-color: rgba(198, 182, 182, 0.1); border: none; border-radius: 7px; color: white;',
            }),
        required=True,
        max_length=100,
        min_length=1,
        strip=True,
        error_messages={'required': 'Veuillez entrer un mot de passe'}
    )

class SignupForm(UserCreationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': "form-control placeholder-style",
            'placeholder': 'Nom d’utilisateur',
            'style': 'background-color: rgba(198, 182, 182, 0.1); border: none; border-radius: 7px; color: white;',
            }),
        required=True,
        max_length=20,
        min_length=1,
        error_messages={'required': 'Veuillez entrer au moins un nom d’utilisateur'},
        # validators=[
        #     RegexValidator(
        #         regex='^[a-zA-Z0-9]*$',
        #         message='Votre nom d’utilisateur ne doit contenir que des lettres et des chiffres',
        #     )
        # ]
    )
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': "form-control placeholder-style",
            'placeholder': 'Mot de passe',
            'style': 'background-color: rgba(198, 182, 182, 0.1); border: none; border-radius: 7px; color: white;',
            }),
        error_messages={'required': 'Veuillez entrer un mot de passe'},
        # validators=[
        #     MinLengthValidator(8, message='Votre mot de passe doit contenir au moins 8 caractères'),
        # ]
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': "form-control placeholder-style",
            'placeholder': 'Confirmer le mot de passe',
            'style': 'background-color: rgba(198, 182, 182, 0.1); border: none; border-radius: 7px; color: white;',
            }),
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

        
############################################################################################################

# Form for updating the username, profile picture and password of a user in the settings page

############################################################################################################
class UpdateUserNameForm(forms.ModelForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': "form-control placeholder-style",
            'placeholder': 'Nom d’utilisateur',
            'style': 'background-color: rgba(198, 182, 182, 0.1); border: none; border-radius: 4px; color: white;'}),
        required=False,
        max_length=20,
        min_length=1,
        error_messages={'required': 'Veuillez entrer au moins un nom d’utilisateur'},
    )

    class Meta:
        model = User
        fields = ['username']

class UpdatePictureForm(forms.ModelForm):
    profile_image = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control form-control-sm',
        'id': 'profile-image-input'}))
    class Meta:
        model = User
        fields = ['profile_image']

class UpdatePasswordForm(forms.ModelForm):
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': "form-control placeholder-style",
            'placeholder': "Mot de passe",
            'style': 'background-color: rgba(198, 182, 182, 0.1); border: none; border-radius: 7px; color: white;',
            }),
        required=False,
        max_length=100,
        min_length=1,
        error_messages={'required': 'Veuillez entrer un mot de passe'},
    )

    class Meta:
        model = User
        fields = ['password']

############################################################################################################
