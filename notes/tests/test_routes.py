from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.any_auth_user = User.objects.create(
            username='Любой авторизованный пользователь'
        )
        cls.note = Note.objects.create(title='Заголовок',
                                       text='Текст',
                                       slug='note-slug',
                                       author=cls.author)

    def test_pages_availability_for_anonymous_user(self):
        url_status = {
            'notes:home': HTTPStatus.OK,
            'users:login': HTTPStatus.OK,
            'users:signup': HTTPStatus.OK,
            'users:logout': HTTPStatus.METHOD_NOT_ALLOWED,
        }

        for name, expected_status in url_status.items():
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_pages_availability_for_auth_user(self):
        self.client.force_login(self.any_auth_user)
        urls = ('notes:list',
                'notes:add',
                'notes:success')
        for name in urls:
            with self.subTest(name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
