from django.urls import path, include
from . import views
from recipes.views import RecipeListView
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('', RecipeListView.as_view(), name='recipe_list'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('password_change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('reset/<str:uidb64>/<str:token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('profile/edit/', views.UserProfileEditView.as_view(), name='edit'),
    path('profile/<str:username>/', views.UserProfileView.as_view(), name='profile'),

]