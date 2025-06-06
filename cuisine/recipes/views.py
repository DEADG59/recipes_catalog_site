from django.shortcuts import render, get_object_or_404, Http404
from django.urls import reverse_lazy
from .models import Recipe, Comment
from .pagination import Pagination
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView
from .forms import CommentForm


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
        comments = self.object.comments.filter(active=True)
        form = CommentForm()
        context['cuisines'] = cuisines
        context['ingredients'] = ingredients
        context['comments'] = comments
        context['form'] = form
        return context


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        raise Http404()


    def form_valid(self, form):
        comment = form.save(commit=False)
        recipe = get_object_or_404(Recipe,
                                    id=self.kwargs['recipe_id'],
                                    status=Recipe.Status.PUBLISHED)
        comment.recipe = recipe
        self.success_url = reverse_lazy('recipes:recipe_detail', args=[recipe.publish.year,
                                                                       recipe.publish.month,
                                                                       recipe.publish.day,
                                                                       recipe.slug])
        return super().form_valid(form)
