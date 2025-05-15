from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('<int:id>/', views.recipe_detail, name='recipe_detail'),
]