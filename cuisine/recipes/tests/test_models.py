from django.test import TestCase
from django.contrib.auth.models import User
from ..models import *


class CuisineModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Cuisine.objects.create(title='test_title')
        cls.cuisine = Cuisine.objects.get(title='test_title')

    @classmethod
    def tearDownClass(cls):
        cls.cuisine.delete()
        super().tearDownClass()

    def test_title_label(self):
        field_label = self.cuisine._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_title_max_length(self):
        max_length = self.cuisine._meta.get_field('title').max_length
        self.assertEqual(max_length, 250)

    def test_title_ordering(self):
        ordering = self.cuisine._meta.ordering
        self.assertEqual(ordering[0], 'title')

    def test_object_name_is_title(self):
        self.assertEqual(self.cuisine.title, str(self.cuisine))


class RecipeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test_user')
        cls.cuisine = Cuisine.objects.create(title='test_cuisine')
        cls.recipe = Recipe.objects.create(title='test_title',
                                           slug='test_slug',
                                           author=cls.user,
                                           description='test_description',
                                           status=Recipe.Status.PUBLISHED)
        cls.recipe.cuisine.set([cls.cuisine.id])
        cls.recipe_1 = Recipe.objects.get(title='test_title')

    @classmethod
    def tearDownClass(cls):
        User.objects.get(username='test_user').delete()
        Cuisine.objects.get(title='test_cuisine').delete()
        super().tearDownClass()

    def test_published_manager(self):
        published_manager = Recipe.published.filter(title='test_title')
        default_manager = Recipe.objects.filter(title='test_title').filter(status=Recipe.Status.PUBLISHED)
        self.assertEqual(published_manager[0], default_manager[0])

    def test_title_label(self):
        field_label = self.recipe_1._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_title_max_length(self):
        max_length = self.recipe_1._meta.get_field('title').max_length
        self.assertEqual(max_length, 250)

    def test_slug_label(self):
        field_label = self.recipe_1._meta.get_field('slug').verbose_name
        self.assertEqual(field_label, 'slug')

    def test_slug_max_length(self):
        max_length = self.recipe_1._meta.get_field('slug').max_length
        self.assertEqual(max_length, 250)

    def test_author_label(self):
        field_label = self.recipe_1._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_author_foreign_key(self):
        author = self.recipe_1.author.username
        self.assertEqual(author, 'test_user')

    def test_cuisine_label(self):
        field_label = self.recipe_1._meta.get_field('cuisine').verbose_name
        self.assertEqual(field_label, 'cuisine')

    def test_cuisine_many_to_many(self):
        cuisine = self.recipe.cuisine.all()[0]
        self.assertEqual(str(cuisine), 'test_cuisine')

    def test_description_label(self):
        field_label = self.recipe_1._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_publish_label(self):
        field_label = self.recipe_1._meta.get_field('publish').verbose_name
        self.assertEqual(field_label, 'publish')

    def test_publish_default(self):
        default = self.recipe_1._meta.get_field('publish').default
        self.assertEqual(default, timezone.now)

    def test_created_label(self):
        field_label = self.recipe_1._meta.get_field('created').verbose_name
        self.assertEqual(field_label, 'created')

    def test_created_auto_now_add(self):
        auto_now_add = self.recipe_1._meta.get_field('created').auto_now_add
        self.assertTrue(auto_now_add)

    def test_updated_title(self):
        field_label = self.recipe_1._meta.get_field('updated').verbose_name
        self.assertEqual(field_label, 'updated')

    def test_updated_auto_now(self):
        auto_now = self.recipe_1._meta.get_field('updated').auto_now
        self.assertTrue(auto_now)

    def test_status_label(self):
        field_label = self.recipe_1._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'status')

    def test_status_default(self):
        default = self.recipe_1._meta.get_field('status').default
        self.assertEqual(default, Recipe.Status.DRAFT)

    def test_status_max_length(self):
        max_length = self.recipe_1._meta.get_field('status').max_length
        self.assertEqual(max_length, 250)

    def test_status_choices(self):
        choices = self.recipe_1._meta.get_field('status').choices
        self.assertEqual(choices, Recipe.Status.choices)

    def test_class_status_draft(self):
        draft = Recipe.Status.DRAFT
        self.assertEqual(draft.value, 'DF')
        self.assertEqual(draft.label, 'Draft')

    def test_class_status_published(self):
        published = Recipe.Status.PUBLISHED
        self.assertEqual(published.value, 'PB')
        self.assertEqual(published.label, 'Published')

    def test_publish_ordering(self):
        ordering = self.recipe_1._meta.ordering
        self.assertEqual(ordering[0], '-publish')

    def test_object_name_is_title(self):
        self.assertEqual(self.recipe_1.title, str(self.recipe_1))


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Product.objects.create(title='test_title')
        cls.product = Product.objects.get(title='test_title')


    @classmethod
    def tearDownClass(cls):
        cls.product.delete()
        super().tearDownClass()

    def test_title_label(self):
        field_label = self.product._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_title_max_length(self):
        max_length = self.product._meta.get_field('title').max_length
        self.assertEqual(max_length, 250)


class MeasureModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Measure.objects.create(title='test_title')
        cls.measure = Measure.objects.get(title='test_title')

    @classmethod
    def tearDownClass(cls):
        cls.measure.delete()
        super().tearDownClass()

    def test_title_label(self):
        field_label = self.measure._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_title_max_length(self):
        max_length = self.measure._meta.get_field('title').max_length
        self.assertEqual(max_length, 250)


class IngredientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test_user')
        cls.recipe = Recipe.objects.create(title='test_title_recipe',
                                           slug='test_slug_recipe',
                                           author=cls.user,
                                           description='test_description',)
        cls.product = Product.objects.create(title='test_title_product')
        cls.measure = Measure.objects.create(title='test_title_measure')
        Ingredient.objects.create(recipe=cls.recipe,
                                  product=cls.product,
                                  amount=1,
                                  measure=cls.measure)
        cls.ingredient = Ingredient.objects.get(amount=1)

    @classmethod
    def tearDownClass(cls):
        User.objects.get(username='test_user').delete()
        super().tearDownClass()

    def test_recipe_label(self):
        field_label = self.ingredient._meta.get_field('recipe').verbose_name
        self.assertEqual(field_label, 'recipe')

    def test_recipe_foreign_key(self):
        recipe = self.ingredient.recipe.title
        self.assertEqual(recipe, 'test_title_recipe')