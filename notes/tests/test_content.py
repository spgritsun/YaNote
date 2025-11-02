from notes.forms import NoteForm

from .test_setup import TestSetUp

from .common import LIST_URL, ADD_URL, EDIT_URL


class TestContent(TestSetUp):

    def test_notes_list_for_different_users(self):
        users_status = (
            (self.author, True),
            (self.any_reg_user, False))
        for user, status in users_status:
            with self.subTest(user=user, status=status):
                self._login_as(user)
                response = self.client.get(LIST_URL)
                object_list = response.context['object_list']
                self.assertEqual(self.note in object_list, status)

    def test_pages_contains_form(self):
        urls = (ADD_URL, EDIT_URL)
        self._login_as(self.author)
        for url in urls:
            with self.subTest(user=self.author, url=url):
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
