from django.urls import reverse

from notes.forms import NoteForm

from .test_setup import TestSetUp


class TestContent(TestSetUp):

    def test_notes_list_for_different_users(self):
        users_status = {
            self.author: True,
            self.any_reg_user: False}
        for user, status in users_status.items():
            self.client.force_login(user)
            url = reverse('notes:list')
            response = self.client.get(url)
            object_list = response.context['object_list']
            self.assertEqual(self.note in object_list, status)

    def test_pages_contains_form(self):
        names_args = {'notes:add': None,
                      'notes:edit': self.slug_for_args}
        self.client.force_login(self.author)
        for name, args in names_args.items():
            url = reverse(name, args=args)
            response = self.client.get(url)
            assert 'form' in response.context
            assert isinstance(response.context['form'], NoteForm)
