from django.test import TestCase

from notes.forms import NoteForm


class NoteFormTest(TestCase):

    def test_empty_title(self):
        form = NoteForm(data={'title': '',
                              'text': 'some text'})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['title'],
            ['This field is required.']
        )

    def test_empty_text(self):
        form = NoteForm(data={'title': 'some text',
                              'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            ['This field is required.']
        )