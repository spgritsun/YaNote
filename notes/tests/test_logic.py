from contextlib import contextmanager
from http import HTTPStatus
from pytils.translit import slugify

from notes.models import Note
from notes.forms import WARNING
from .test_setup import TestSetUp
from .common import ADD_URL, EDIT_URL, SUCCESS_URL, LOGIN_URL, DELETE_URL


class TestLogic(TestSetUp):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.WARNING = WARNING

    def setUp(self):
        super().setUp()
        self.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug'
        }

    @contextmanager
    def before_after_notes_count(self, delta):
        count_before = Note.objects.count()
        yield
        count_after = Note.objects.count()
        self.assertEqual(count_after, count_before + delta)

    def test_user_can_create_note(self):
        self._login_as(self.author)
        with self.before_after_notes_count(delta=1):
            response = self.client.post(ADD_URL, data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        new_note = Note.objects.get(slug=self.form_data['slug'])
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        self._login_as(None)
        with self.before_after_notes_count(delta=0):
            response = self.client.post(ADD_URL, data=self.form_data)
        expected_url = f'{LOGIN_URL}?next={ADD_URL}'
        self.assertRedirects(response, expected_url)

    def test_not_unique_slug(self):
        self._login_as(self.author)
        self.form_data['slug'] = self.note.slug
        with self.before_after_notes_count(delta=0):
            response = self.client.post(ADD_URL, data=self.form_data)
        self.assertFormError(response.context['form'], 'slug',
                             self.note.slug + self.WARNING)

    def test_empty_slug(self):
        self._login_as(self.author)
        self.form_data.pop('slug')
        with self.before_after_notes_count(delta=1):
            response = self.client.post(ADD_URL, data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        new_note = Note.objects.last()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_edit_note(self):
        self._login_as(self.author)
        response = self.client.post(EDIT_URL, self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.form_data['title'])
        self.assertEqual(self.note.text, self.form_data['text'])
        self.assertEqual(self.note.slug, self.form_data['slug'])

    def test_other_user_cant_edit_note(self):
        self._login_as(self.any_reg_user)
        response = self.client.post(EDIT_URL, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)

    def test_author_can_delete_note(self):
        self._login_as(self.author)
        with self.before_after_notes_count(delta=-1):
            response = self.client.post(DELETE_URL)
        self.assertRedirects(response, SUCCESS_URL)

    def test_other_user_cant_delete_note(self):
        self._login_as(self.any_reg_user)
        with self.before_after_notes_count(delta=0):
            response = self.client.post(DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
