from django.shortcuts import render, get_object_or_404
from .models import Recipe


def recipe_list(request):
    recipes = Recipe.published.all()
    return render(request,
                  'recipes/recipe/list.html',
                  {'recipes': recipes})


def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe,
                               id=id,
                               status=Recipe.Status.PUBLISHED)
    cuisines = Recipe.published.get(id=id).cuisine.all()
    return render(request,
                  'recipes/recipe/detail.html',
                  {'recipe': recipe,
                   'cuisines': cuisines})
