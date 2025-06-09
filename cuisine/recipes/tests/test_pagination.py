from ..pagination import Pagination
from django.core.paginator import Paginator
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Recipe


class PaginationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test user')
        number_of_recipes = 10
        for number in range(number_of_recipes):
            Recipe.objects.create(title=f'test {number} recipe',
                                  slug=f'test-{number}-recipe',
                                  author=cls.user,
                                  description='',
                                  status=Recipe.Status.PUBLISHED)
        cls.recipes = Recipe.published.all()
        cls.paginator = Paginator(cls.recipes, 2) # 5 страниц


    @classmethod
    def tearDownClass(cls):
        del cls.paginator
        cls.user.delete()


    def test_page_number_is_1(self):
        pagination = Pagination(2, self.paginator, 1)
        self.assertEqual(list(pagination['page_obj']), list(self.paginator.page(1)))
        self.assertEqual(pagination['left_pages'], [])
        self.assertEqual(pagination['right_pages'], [2,3])
        self.assertEqual(pagination['left_pages_more'], 0)
        self.assertEqual(pagination['right_pages_more'], 5)


    def test_page_number_is_2(self):
        pagination = Pagination(2, self.paginator, 2)
        self.assertEqual(list(pagination['page_obj']), list(self.paginator.page(2)))
        self.assertEqual(pagination['left_pages'], [1])
        self.assertEqual(pagination['right_pages'], [3,4])
        self.assertEqual(pagination['left_pages_more'], 0)
        self.assertEqual(pagination['right_pages_more'], 5)


    def test_page_number_is_3(self):
        pagination = Pagination(2, self.paginator, 3)
        self.assertEqual(list(pagination['page_obj']), list(self.paginator.page(3)))
        self.assertEqual(pagination['left_pages'], [1,2])
        self.assertEqual(pagination['right_pages'], [4,5])
        self.assertEqual(pagination['left_pages_more'], 0)
        self.assertEqual(pagination['right_pages_more'], 0)


    def test_page_number_is_4(self):
        pagination = Pagination(2, self.paginator, 4)
        self.assertEqual(list(pagination['page_obj']), list(self.paginator.page(4)))
        self.assertEqual(pagination['left_pages'], [2,3])
        self.assertEqual(pagination['right_pages'], [5])
        self.assertEqual(pagination['left_pages_more'], 1)
        self.assertEqual(pagination['right_pages_more'], 0)


    def test_page_number_is_5(self):
        pagination = Pagination(2, self.paginator, 5)
        self.assertEqual(list(pagination['page_obj']), list(self.paginator.page(5)))
        self.assertEqual(pagination['left_pages'], [3,4])
        self.assertEqual(pagination['right_pages'], [])
        self.assertEqual(pagination['left_pages_more'], 1)
        self.assertEqual(pagination['right_pages_more'], 0)


    def test_page_number_out_of_range(self):
        pagination = Pagination(2, self.paginator, 10)
        self.assertEqual(pagination['left_pages'], [3, 4])
        self.assertEqual(pagination['right_pages'], [])
        self.assertEqual(pagination['left_pages_more'], 1)
        self.assertEqual(pagination['right_pages_more'], 0)


    def test_page_number_is_not_integer(self):
        pagination = Pagination(2, self.paginator, 'abc')
        self.assertEqual(list(pagination['page_obj']), list(self.paginator.page(1)))
        self.assertEqual(pagination['left_pages'], [])
        self.assertEqual(pagination['right_pages'], [2, 3])
        self.assertEqual(pagination['left_pages_more'], 0)
        self.assertEqual(pagination['right_pages_more'], 5)
