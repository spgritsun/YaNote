from django.urls import reverse
from pytest_django.asserts import assertRedirects

from .test_setup import TestSetUp
from notes.models import Note


class TestRoutes(TestSetUp):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug'
        }

    def test_user_can_create_note(self):
        url = reverse('notes:add')
        self.client.force_login(self.author)
        Note.objects.all().delete()  # &&& ??????????????
        response = self.client.post(url, data=self.form_data)
        assertRedirects(response, reverse('notes:success'))
        assert Note.objects.count() == 1
        new_note = Note.objects.get()
        assert new_note.title == self.form_data['title']
        assert new_note.text == self.form_data['text']
        assert new_note.slug == self.form_data['slug']
        assert new_note.author == self.author
