from django.contrib.auth import get_user_model
from django.test import TestCase

from notes.models import Note

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
