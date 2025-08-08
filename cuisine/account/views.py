from django.shortcuts import render, get_object_or_404
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import *
from django.views.generic import CreateView, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages


class UserLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('login')


class UserRegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Вы успешно зарегистрировались, теперь вы можете войти')
        return super().form_valid(form)


class UserPasswordChangeView(auth_views.PasswordChangeView):
    def form_valid(self, form):
        messages.success(self.request, 'Пароль успешно изменен')
        self.success_url = reverse_lazy('account:profile', args=[self.request.user])
        return super().form_valid(form)


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    def form_valid(self, form):
        messages.success(self.request, 'Новый пароль успешно сохранен')
        self.success_url = reverse_lazy('login')
        return super().form_valid(form)


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
            messages.success(request, 'Профиль успешно обновлен')
        return render(self.request,
                      self.template_name,
                      self.get_context_data())