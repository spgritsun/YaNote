from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

SLUG = 'note-slug'
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')
HOME_URL = reverse('notes:home')
LIST_URL = reverse('notes:list')
ADD_URL = reverse('notes:add')
SUCCESS_URL = reverse('notes:success')
DETAIL_URL = reverse('notes:detail', args=(SLUG,))
EDIT_URL = reverse('notes:edit', args=(SLUG,))
DELETE_URL = reverse('notes:delete', args=(SLUG,))

User = get_user_model()


class TestSetUp(TestCase):

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

    def _login_as(self, user):
        if user:
            self.client.force_login(user)
        else:
            self.client.logout()
