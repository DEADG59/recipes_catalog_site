from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import UserRegistrationForm
from django.views.generic import CreateView, TemplateView


class UserLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('login')


class UserRegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('account:register_done')


class UserRegisterDoneView(TemplateView):
    template_name = 'registration/register_done.html'
