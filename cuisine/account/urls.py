from django.urls import path, include
from . import views
from recipes.views import RecipeListView
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('', RecipeListView.as_view(), name='recipe_list'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('register/done/', views.UserRegisterDoneView.as_view(), name='register_done'),

]