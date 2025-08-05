from django.shortcuts import render, get_object_or_404
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import *
from django.views.generic import CreateView, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse


class UserLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('login')


class UserRegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('account:register_done')


class UserRegisterDoneView(TemplateView):
    template_name = 'registration/register_done.html'


class UserProfileView(DetailView):
    model = User
    context_object_name = 'profile'
    template_name = 'account/profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model,
                                 username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = False
        if self.request.user.username == self.object.username:
            context['owner'] = True
        # print(context)
        return context



class UserProfileEditView(LoginRequiredMixin, TemplateView):
    template_name = 'account/edit.html'

    def get_context_data(self, **kwargs):
        context = {'view': self}
        context['user_form'] = UserEditForm(instance=self.request.user)
        context['profile_form'] = ProfileEditForm(instance=self.request.user.profile)
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        return HttpResponse(status=204)
