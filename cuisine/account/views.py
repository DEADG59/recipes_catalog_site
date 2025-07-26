from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


class UserLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('login')


# class UserPasswordChangeView(auth_views.PasswordChangeView):
#     success_url = reverse_lazy('account:password_change_done')
#
#
# class UserPasswordResetView(auth_views.PasswordResetView):
#     success_url = reverse_lazy('account:password_reset_done')
#
#
# class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
#     success_url = reverse_lazy('account:password_reset_complete')
