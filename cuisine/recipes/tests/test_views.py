from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import *
from ..views import *
from ..forms import CommentForm
import datetime


class RecipeListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test_name')
        number_of_recipes = 10
        for number in range(number_of_recipes):
            Recipe.objects.create(title=f'test_title {number}',
                                  slug=f'test-title-{number}',
                                  author=cls.user,
                                  description='',
                                  status=Recipe.Status.PUBLISHED)
        cls.url = reverse('recipes:recipe_list')


    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        del cls.url
        super().tearDownClass()


    def test_view_url_exists_at_urlpatterns(self):
        resp = self.client.get('/recipes/')
        self.assertEqual(resp.status_code, 200)


    def test_view_url_uses_correct_template(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'recipes/recipe/list.html')


    def test_view_valid_attributes(self):
        view = RecipeListView()
        self.assertEqual(view.paginate_by, 3)
        self.assertEqual(view.context_object_name, 'recipes')
        queryset = view.queryset
        self.assertEqual(list(queryset), list(Recipe.published.all()))


    def test_pagination_is_three(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['recipes']) == 3)
        self.assertEqual(resp.context['left_pages'], [])
        self.assertEqual(resp.context['right_pages'], [2,3,4])
        self.assertEqual(resp.context['left_pages_more'], 0)
        self.assertEqual(resp.context['right_pages_more'], 0)


    def test_last_page_all_recipes(self):
        resp = self.client.get(self.url + '?page=4')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['recipes']) == 1)
        self.assertEqual(resp.context['left_pages'], [1, 2, 3])
        self.assertEqual(resp.context['right_pages'], [])
        self.assertEqual(resp.context['left_pages_more'], 0)
        self.assertEqual(resp.context['right_pages_more'], 0)


    def test_parameter_page_is_more_last_page(self):
        resp = self.client.get(self.url + '?page=10')
        self.assertEqual(resp.context['page_obj'].number, 4)


    def test_parameter_page_is_not_integer(self):
        resp = self.client.get(self.url + '?page=abc')
        self.assertEqual(resp.context['page_obj'].number, 1)


class RecipeDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test_user')
        cls.cuisine = Cuisine.objects.create(title='test_cuisine')
        cls.date = datetime.datetime(2025, 1, 20, 15, 30, 59)
        cls.recipe = Recipe.objects.create(title='test recipe',
                                       slug='test-recipe',
                                       author=cls.user,
                                       description='',
                                       publish=cls.date,
                                       created=cls.date,
                                       updated=cls.date,
                                       status=Recipe.Status.PUBLISHED)
        cls.recipe.cuisine.set([cls.cuisine.id])
        cls.product = Product.objects.create(title='test_product')
        cls.measure = Measure.objects.create(title='test_measure')
        cls.ingredient = Ingredient(recipe=cls.recipe,
                                product=cls.product,
                                amount=5,
                                measure=cls.measure)
        cls.comments = Comment(recipe=cls.recipe,
                           name='test_name',
                           email='test@test.com',
                           body='')
        cls.url = reverse('recipes:recipe_detail', args=[cls.recipe.publish.year,
                                                         cls.recipe.publish.month,
                                                         cls.recipe.publish.day,
                                                         cls.recipe.slug])

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.cuisine.delete()
        cls.product.delete()
        cls.measure.delete()
        del cls.url
        del cls.date
        super().tearDownClass()


    def test_view_url_exists_at_urlpatterns(self):
        publish = self.recipe.publish
        resp = self.client.get(f'/recipes/{publish.year}/{publish.month}/{publish.day}/{self.recipe.slug}')
        self.assertEqual(resp.status_code, 200)


    def test_view_url_uses_correct_template(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'recipes/recipe/detail.html')


    def test_view_valid_attributes(self):
        view = RecipeDetailView()
        self.assertEqual(view.model, Recipe)
        self.assertEqual(view.context_object_name, 'recipe')


    def test_view_get_object(self):
        view = RecipeDetailView()
        view.request = self.client
        publish = self.recipe.publish
        view.kwargs = {'year': publish.year,
                       'month': publish.month,
                       'day': publish.day,
                       'recipe_slug': self.recipe.slug}
        self.assertEqual(view.get_object(), self.recipe)


    def test_view_get_context_data(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        obj = resp.context['object']
        self.assertEqual(list(resp.context['cuisines']), list(obj.cuisine.all()))
        self.assertEqual(list(resp.context['ingredients']), list(obj.recipes_ingredient.all()))
        self.assertEqual(list(resp.context['comments']), list(obj.comments.filter(active=True)))
        self.assertEqual(resp.context['form'].declared_fields, CommentForm().declared_fields)


class CommentCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test_user')
        cls.recipe = Recipe.objects.create(title='test recipe',
                                           slug='test-recipe',
                                           author=cls.user,
                                           description='',
                                           status=Recipe.Status.PUBLISHED)

        cls.form_data = CommentForm({'name': 'test_name',
                                     'email': 'test@test.com',
                                     'body': 'test text'})
        cls.url = reverse('recipes:recipe_comment', kwargs={'recipe_id': cls.recipe.id})


    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        del cls.form_data
        del cls.url
        super().tearDownClass()


    def test_view_method_get_return_404(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 404)


    def test_view_valid_attributes(self):
        view = CommentCreateView()
        self.assertEqual(view.model, Comment)
        self.assertEqual(view.form_class, CommentForm)


    def test_view_form_valid(self):
        view = CommentCreateView()
        view.request = self.client
        view.kwargs = {'recipe_id': self.recipe.id}
        self.assertEqual(view.form_valid(self.form_data).status_code, 302)


    def test_model_comment_valid_data_and_have_foreign_key_recipe(self):
        view = CommentCreateView()
        view.request = self.client
        view.kwargs = {'recipe_id': self.recipe.id}
        view.form_valid(self.form_data)
        comment = Comment.objects.get(name='test_name')
        self.assertEqual(comment.email, 'test@test.com')
        self.assertEqual(comment.body, 'test text')
        self.assertEqual(comment.recipe, self.recipe)


    def test_view_valid_success_url(self):
        view = CommentCreateView()
        view.request = self.client
        view.kwargs = {'recipe_id': self.recipe.id}
        view.form_valid(self.form_data)
        self.assertEqual(view.success_url, reverse('recipes:recipe_detail', args=[self.recipe.publish.year,
                                                                                  self.recipe.publish.month,
                                                                                  self.recipe.publish.day,
                                                                                  self.recipe.slug]))
