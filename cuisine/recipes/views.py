from django.shortcuts import render, get_object_or_404
from .models import Recipe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def recipe_list(request):
    recipes = Recipe.published.all()
    paginator = Paginator(recipes, 3)
    page_number = request.GET.get('page', 1)
    try:
        recipes = paginator.page(page_number)
    except PageNotAnInteger:
        recipes = paginator.page(1)
    except EmptyPage:
        recipes = paginator.page(paginator.num_pages)
    return render(request,
                  'recipes/recipe/list.html',
                  {'recipes': recipes})


def recipe_detail(request, year, month, day, recipe_slug):
    format_date = f'{year}-{month}-{day}'
    recipe = get_object_or_404(Recipe,
                               status=Recipe.Status.PUBLISHED,
                               slug=recipe_slug,
                               publish__date=format_date)
    cuisines = recipe.cuisine.all()
    ingredients = recipe.recipes_ingredient.all()
    return render(request,
                  'recipes/recipe/detail.html',
                  {'recipe': recipe,
                   'cuisines': cuisines,
                   'ingredients': ingredients})
