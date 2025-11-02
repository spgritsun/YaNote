from http import HTTPStatus

from .test_setup import TestSetUp
from .common import (ADD_URL, EDIT_URL, SUCCESS_URL, LOGIN_URL, DELETE_URL,
                     HOME_URL, SIGNUP_URL, LOGOUT_URL, LIST_URL, DETAIL_URL)


class TestRoutes(TestSetUp):

    def test_status_codes(self):
        test_cases = (
            # Страницы для анонимного пользователя
            (HOME_URL, None, HTTPStatus.OK),
            (LOGIN_URL, None, HTTPStatus.OK),
            (SIGNUP_URL, None, HTTPStatus.OK),

            # Страницы для авторизованного пользователя (не автора)
            (LIST_URL, self.any_reg_user, HTTPStatus.OK),
            (ADD_URL, self.any_reg_user, HTTPStatus.OK),
            (SUCCESS_URL, self.any_reg_user, HTTPStatus.OK),
            (DETAIL_URL, self.any_reg_user, HTTPStatus.NOT_FOUND),
            (EDIT_URL, self.any_reg_user, HTTPStatus.NOT_FOUND),
            (DELETE_URL, self.any_reg_user, HTTPStatus.NOT_FOUND),

            # Страницы для автора заметки
            (DETAIL_URL, self.author, HTTPStatus.OK),
            (EDIT_URL, self.author, HTTPStatus.OK),
            (DELETE_URL, self.author, HTTPStatus.OK),
        )

        for url, user, status in test_cases:
            with self.subTest(
                    url=url,
                    user=user.username if user else 'Anonymous',
                    status=status
            ):
                self._login_as(user)
                response = self.client.get(url)
                self.assertEqual(response.status_code, status)

    def test_redirects_for_unauthorized_user(self):
        urls = (
            DETAIL_URL, EDIT_URL, DELETE_URL,
            ADD_URL, SUCCESS_URL, LIST_URL
        )
        self.client.logout()
        for url in urls:
            redirect_url = f'{LOGIN_URL}?next={url}'
            with self.subTest(url=url, redirect_url=redirect_url):
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_logout_for_all_users(self):
        test_cases = (
            (None, 'GET', HTTPStatus.METHOD_NOT_ALLOWED),
            (None, 'POST', HTTPStatus.OK),
            (self.author, 'GET', HTTPStatus.METHOD_NOT_ALLOWED),
            (self.author, 'POST', HTTPStatus.OK),
            (self.any_reg_user, 'GET', HTTPStatus.METHOD_NOT_ALLOWED),
            (self.any_reg_user, 'POST', HTTPStatus.OK),
        )
        for user, method, status in test_cases:
            with self.subTest(
                    url=LOGOUT_URL,
                    user=user.username if user else 'Anonymous',
                    method=method,
                    status=status
            ):
                self._login_as(user)
                response = getattr(self.client, method.lower())(LOGOUT_URL)
                self.assertEqual(response.status_code, status)
