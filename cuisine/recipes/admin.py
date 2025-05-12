from django.contrib import admin
from .models import Recipe, Cuisine, Product, Measure, Ingredient


@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
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