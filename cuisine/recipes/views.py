from django.shortcuts import render, get_object_or_404
from .models import Recipe
from .pagination import Pagination
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView


class RecipeListView(ListView):
    queryset = Recipe.published.all()
    context_object_name = 'recipes'
    paginate_by = 3
    template_name = 'recipes/recipe/list.html'

    def get_context_data(self, **kwargs):
        paginator = Paginator(self.queryset, self.paginate_by)
        page_number = self.request.GET.get('page', 1)
        context = Pagination(5, paginator, page_number)
        context['paginator'] = paginator
        context['is_paginated'] = True
        context['objects_list'] = context['page_obj'].object_list
        context[self.context_object_name] = context['objects_list']
        return context

class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/recipe/detail.html'

    def get_object(self, queryset=None):
         return get_object_or_404(Recipe,
                                  status=Recipe.Status.PUBLISHED,
                                  slug=self.kwargs['recipe_slug'],
                                  publish__date=f"{self.kwargs['year']}-{self.kwargs['month']}-{self.kwargs['day']}")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cuisines = self.object.cuisine.all()
        ingredients = self.object.recipes_ingredient.all()
        context['cuisines'] = cuisines
        context['ingredients'] = ingredients
        return context
