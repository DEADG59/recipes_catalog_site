from django.test import TestCase
from ..forms import CommentForm
from django.contrib.auth.models import User
from ..models import Comment, Recipe


class CommentFormTest(TestCase):
    def setUp(self):
        self.data = {'name': 'test name',
                     'email': 'test@test.com',
                     'body': 'test text'}


    def test_form_valid_attributes(self):
        form = CommentForm
        self.assertEqual(form.Meta.model, Comment)
        self.assertEqual(form.Meta.fields, ['name', 'email', 'body'])


    def test_form_valid_data(self):
        form = CommentForm(data=self.data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['name'], 'test name')
        self.assertEqual(form.cleaned_data['email'], 'test@test.com')
        self.assertEqual(form.cleaned_data['body'], 'test text')


    def test_form_invalid_data(self):
        data = {'name': 'a'*81,
                'email': 'test',
                'body': ''}
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('body', form.errors)


    def test_form_save(self):
        form = CommentForm(data=self.data)
        self.assertTrue(form.is_valid())
        instance = form.save(commit=False)
        self.assertEqual(instance.name, 'test name')
        self.assertEqual(instance.email, 'test@test.com')
        self.assertEqual(instance.body, 'test text')