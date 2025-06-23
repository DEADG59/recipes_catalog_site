from django.test import TestCase
from django.contrib.auth.models import User
from ..models import *


class RecipeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test_user')
        cls.recipe = Recipe.objects.create(title='test_title',
                                           slug='test_slug',
                                           author=cls.user,
                                           description='test_description',
                                           status=Recipe.Status.PUBLISHED)
        Recipe.objects.create(title='test_title_draft',
                              slug='test_title_draft',
                              author=cls.user,
                              description='',
                              status=Recipe.Status.DRAFT)


    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()


    def test_published_manager(self):
        published_manager = Recipe.published.filter(title='test_title')
        default_manager = Recipe.objects.filter(title='test_title').filter(status=Recipe.Status.PUBLISHED)
        self.assertEqual(list(published_manager), list(default_manager))


    def test_title_max_length(self):
        max_length = self.recipe._meta.get_field('title').max_length
        self.assertEqual(max_length, 250)


    def test_slug_max_length(self):
        max_length = self.recipe._meta.get_field('slug').max_length
        self.assertEqual(max_length, 250)


    def test_author_foreign_key(self):
        author = self.recipe.author.username
        self.assertEqual(author, 'test_user')


    def test_publish_default(self):
        default = self.recipe._meta.get_field('publish').default
        self.assertEqual(default, timezone.now)


    def test_created_auto_now_add(self):
        auto_now_add = self.recipe._meta.get_field('created').auto_now_add
        self.assertTrue(auto_now_add)


    def test_updated_auto_now(self):
        auto_now = self.recipe._meta.get_field('updated').auto_now
        self.assertTrue(auto_now)


    def test_status_default(self):
        default = self.recipe._meta.get_field('status').default
        self.assertEqual(default, Recipe.Status.DRAFT)


    def test_status_max_length(self):
        max_length = self.recipe._meta.get_field('status').max_length
        self.assertEqual(max_length, 250)


    def test_status_choices(self):
        choices = self.recipe._meta.get_field('status').choices
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
        ordering = self.recipe._meta.ordering
        self.assertEqual(ordering, ['-publish'])


    def test_object_name_is_title(self):
        self.assertEqual(self.recipe.title, str(self.recipe))


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.create(title='test_title')


    @classmethod
    def tearDownClass(cls):
        cls.product.delete()
        super().tearDownClass()


    def test_title_max_length(self):
        max_length = self.product._meta.get_field('title').max_length
        self.assertEqual(max_length, 250)


class MeasureModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.measure = Measure.objects.create(title='test_title')


    @classmethod
    def tearDownClass(cls):
        cls.measure.delete()
        super().tearDownClass()


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
        cls.ingredient = Ingredient.objects.create(recipe=cls.recipe,
                                                   product=cls.product,
                                                   amount=1,
                                                   measure=cls.measure)


    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.product.delete()
        cls.measure.delete()
        super().tearDownClass()


    def test_recipe_foreign_key(self):
        recipe = self.ingredient.recipe.title
        self.assertEqual(recipe, 'test_title_recipe')


    def test_product_foreign_key(self):
        product = self.ingredient.product.title
        self.assertEqual(product, 'test_title_product')


    def test_measure_foreign_key(self):
        measure = self.ingredient.measure.title
        self.assertEqual(measure, 'test_title_measure')


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test username')
        cls.recipe = Recipe.objects.create(title='test title recipe',
                                           slug='test-title-recipe',
                                           author=cls.user,
                                           description='',
                                           status=Recipe.Status.PUBLISHED)
        cls.comment = Comment.objects.create(recipe=cls.recipe,
                                             name='test name',
                                             email='test@test.com',
                                             body='')


    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()


    def test_recipe_field_foreign_key(self):
        recipe = self.comment.recipe.title
        self.assertEqual(recipe, 'test title recipe')


    def test_name_field_max_length(self):
        field_name = self.comment._meta.get_field('name')
        self.assertEqual(field_name.max_length, 80)


    def test_created_field_auto_now_add(self):
        field_created = self.comment._meta.get_field('created')
        self.assertTrue(field_created.auto_now_add)


    def test_updated_field_auto_now(self):
        field_updated = self.comment._meta.get_field('updated')
        self.assertTrue(field_updated.auto_now)


    def test_active_field_default(self):
        field_active = self.comment._meta.get_field('active')
        self.assertTrue(field_active.default)


    def test_meta_class_ordering(self):
        ordering = self.comment._meta.ordering
        self.assertEqual(ordering, ['-created'])
