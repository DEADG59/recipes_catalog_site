from django.test import TestCase
from ..forms import *
from django.contrib.auth.models import User
from django.forms import ValidationError


class TestUserRegistrationForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = {'username': 'testname',
                    'email': 'test@test.com',
                    'password1': 'test-password',
                    'password2': 'test-password'}


    @classmethod
    def tearDownClass(cls):
        del cls.data


    def test_form_valid_data(self):
        form = UserRegistrationForm(data=self.data)
        self.assertTrue(form.is_valid())


    def test_form_invalid_data(self):
        form = UserRegistrationForm(data={'username': '~/*=&?<>',
                                          'email': 'testemail',
                                          'password1': 'password1',
                                          'password2': 'password2'})
        self.assertFalse(form.is_valid())


    def test_form_clean_password2(self):
        form = UserRegistrationForm(data={'username': self.data['username'],
                                          'email': self.data['email'],
                                          'password1': self.data['password1'],
                                          'password2': self.data['password2']+'a'})
        form.is_valid()
        self.assertIn('password2', form.errors)


    def test_form_save(self):
        form = UserRegistrationForm(data=self.data)
        user = form.save()
        self.assertEqual(user.username, self.data['username'])
        self.assertEqual(user.email, self.data['email'])
        self.assertTrue(user.password)


    def test_form_clean_email(self):
        form = UserRegistrationForm(data=self.data)
        form.save()

        form = UserRegistrationForm(data={'username': 'another_username',
                                          'email': 'test@test.com',
                                          'password1': 'another-password',
                                          'password2': 'another-password'})
        form.is_valid()
        self.assertIn('email', form.errors)


    def test_form_valid_similar_username(self):
        form = UserRegistrationForm(data=self.data)
        form.save()

        form = UserRegistrationForm(data={'username': 'testname',
                                          'email': 'another@email.com',
                                          'password1': 'another-password',
                                          'password2': 'another-password'})
        form.is_valid()
        self.assertIn('username', form.errors)
