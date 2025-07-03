from django.shortcuts import render, get_object_or_404, Http404
from django.urls import reverse_lazy
from .models import Recipe, Comment
from .pagination import Pagination
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, FormView
from .forms import CommentForm, SearchForm
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


class RecipeListView(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = 3
    template_name = 'recipes/recipe/list.html'

    def get_queryset(self):
        queryset = Recipe.published.all()
        self.tag = None
        if 'tag_slug' in self.kwargs:
            self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
            queryset = queryset.filter(tags__in=[self.tag])
        return queryset


    def get_context_data(self, **kwargs):
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page', 1)
        context = Pagination(5, paginator, page_number)
        context['paginator'] = paginator
        context['is_paginated'] = True
        context['objects_list'] = context['page_obj'].object_list
        context[self.context_object_name] = context['objects_list']
        context['tag'] = self.tag
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
        ingredients = self.object.recipes_ingredient.all()
        recipe_tags_ids = self.object.tags.values_list('id', flat=True)
        similar_recipes = Recipe.published.filter(tags__in=recipe_tags_ids)\
                                          .exclude(id=self.object.id)
        similar_recipes = similar_recipes.annotate(same_tags=Count('tags'))\
                                         .order_by('-same_tags', '-publish')[:4]
        comments = self.object.comments.filter(active=True)
        form = CommentForm()
        context['ingredients'] = ingredients
        context['similar_recipes'] = similar_recipes
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


class RecipeSearch(FormView):
    form_class = SearchForm
    template_name = 'recipes/recipe/search.html'
    query = None
    results = None

    def get(self, request, *args, **kwargs):
        if 'query' in request.GET:

            query = request.GET.get('query')
            search_vector = SearchVector('title', 'description', config='russian')
            search_query = SearchQuery(query, config='russian')
            results = Recipe.published.annotate(search=search_vector,
                                                rank=SearchRank(search_vector, search_query)
                                                ).filter(search=search_query).order_by('-rank')
            context = self.get_context_data()
            context['query'] = query
            context['results'] = results
            return render(request, self.template_name, context)
        return self.render_to_response(self.get_context_data())
