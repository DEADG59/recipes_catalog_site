from django.contrib import admin
from .models import *


class CuisineInline(admin.TabularInline):
    model = Recipe.cuisine.through


@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    inlines = [
        CuisineInline,
    ]

    list_display = ['title']
    search_fields = ['title']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        CuisineInline,
    ]
    exclude = ['cuisine']
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'product', 'amount', 'measure']
    search_fields = ['recipe', 'product']
    raw_id_fields = ['recipe', 'product', 'measure']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'recipe', 'created', 'active']
    list_filter = ['name', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
