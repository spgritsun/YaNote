from http import HTTPStatus

from pytest_django.asserts import assertRedirects

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.any_reg_user = User.objects.create(
            username='Любой зарегистрированный пользователь'
        )
        cls.note = Note.objects.create(title='Заголовок',
                                       text='Текст',
                                       slug='note-slug',
                                       author=cls.author)
        cls.slug_for_args = (cls.note.slug,)

    def test_pages_availability_for_anonymous_user(self):
        name_status = {
            'notes:home': HTTPStatus.OK,
            'users:login': HTTPStatus.OK,
            'users:signup': HTTPStatus.OK,
            'users:logout': HTTPStatus.METHOD_NOT_ALLOWED,
        }
        for name, expected_status in name_status.items():
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_logout_for_post_method(self):
        name = 'users:logout'
        url = reverse(name)
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        self.client.force_login(self.any_reg_user)
        names = ('notes:list',
                 'notes:add',
                 'notes:success')
        for name in names:
            with self.subTest(name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_different_users(self):
        user_status = {self.author: HTTPStatus.OK,
                       self.any_reg_user: HTTPStatus.NOT_FOUND}
        names = {
            'notes:detail',
            'notes:edit',
            'notes:delete',
        }
        for user, status in user_status.items():
            self.client.force_login(user)
            for name in names:
                with self.subTest(name):
                    url = reverse(name, args=self.slug_for_args)
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirects(self):
        names = {
            'notes:detail': self.slug_for_args,
            'notes:edit': self.slug_for_args,
            'notes:delete': self.slug_for_args,
            'notes:add': None,
            'notes:success': None,
            'notes:list': None}
        login_url = reverse('users:login')
        for name, args in names.items():
            if args is not None:
                url = reverse(name, args=args)
            else:
                url = reverse(name)
            expected_url = f'{login_url}?next={url}'
            response = self.client.get(url)
            assertRedirects(response, expected_url)
