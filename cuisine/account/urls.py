from django.urls import path, include
from . import views
from recipes.views import RecipeListView
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('', RecipeListView.as_view(), name='recipe_list'),
]
