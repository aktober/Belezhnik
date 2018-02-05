from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidget

from .models import Note


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'text')
        widgets = {
            'text': SummernoteWidget(),
        }