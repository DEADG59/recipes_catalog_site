from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import re
from .models import Profile
from django.utils.translation import gettext_lazy as _


def validate_no_russian_chars(value):
    if re.search(r'[а-яА-Я]', value):
        raise forms.ValidationError('Можно использовать только латинские буквы.')

def validate_special_chars(value):
    if re.search(r'[@\+]', value):
        raise forms.ValidationError('Можно использовать только символы - _ .')


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя',
                               min_length=4,
                               max_length=80,
                               validators=[validate_no_russian_chars,
                                           validate_special_chars],
                               help_text='только латинские буквы, цифры и символы - . _')

    password1 = forms.CharField(label='Пароль',
                                min_length=8,
                                max_length=64,
                                widget=forms.PasswordInput,
                                validators=[validate_no_russian_chars])

    password2 = forms.CharField(label='Повторите пароль',
                                min_length=8,
                                max_length=64,
                                widget=forms.PasswordInput,
                                validators=[validate_no_russian_chars])

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {'email': 'E-mail'}


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Аккаунт с таким e-mail уже существует.')
        return email


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
            Profile.objects.create(user=user)
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя или e-mail'
        self.error_messages['invalid_login'] = 'Пожалуйста, введите правильные имя пользователя или e-mail и пароль.'


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError('Это имя пользователя уже используется.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(id=self.instance.id).filter(email=email).exists():
            raise forms.ValidationError('Этот e-mail уже используется.')
        return email


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']
        labels = {'photo': 'Фото'}
