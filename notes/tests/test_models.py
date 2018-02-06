from django.contrib.auth.models import User
from django.test import TestCase

from notes.models import Note
from users.models import UserProfile


class NoteModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser',
                    email='test@gmail.com',
                    password='123',
                    is_active=True)
        self.userprofile = UserProfile.objects.create(user=self.user)

    def test_str_presentation(self):
        note = Note.objects.create(author=self.userprofile,
                    title='test title',
                    text='test text')
        self.assertEqual(str(note), 'test title')

    def test_creation(self):
        note = Note(author=self.userprofile,
                    title='test title',
                    text='test text')
        note.save()
        self.assertEqual(Note.objects.all().count(), 1)