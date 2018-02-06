from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from users.models import UserProfile
from .forms import NoteForm
from .models import Note


class NoteActionMixin:
    """
    Mixin to add proper message after create/edit Note object
    """
    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(NoteActionMixin, self).form_valid(form)


class CreateNoteView(LoginRequiredMixin, NoteActionMixin, generic.CreateView):
    """
    Create new Note object
    """
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_msg = "Note created!"

    def form_valid(self, form):
        note = form.save(commit=False)
        note.author = get_object_or_404(UserProfile, user=self.request.user)
        note.save()
        return super(CreateNoteView, self).form_valid(form)


class UpdateNoteView(LoginRequiredMixin, NoteActionMixin, generic.edit.UpdateView):
    """
    Update Note object
    """
    form_class = NoteForm
    model = Note
    success_msg = "Note updated!"


class NoteEditorView(LoginRequiredMixin, generic.FormView):
    """
    One View for Create and Update Note
    """
    form_class = NoteForm
    template_name = 'notes/note_form.html'

    def get_form(self, form_class=form_class):
        pk = self.request.GET.get('pk')
        if pk:
            self.note = get_object_or_404(Note, id=pk)
            return form_class(instance=self.note, **self.get_form_kwargs())
        else:
            self.note = None
            return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        self.note = form.save(commit=False)
        self.note.author = get_object_or_404(UserProfile, user=self.request.user)
        self.note.save()
        return super(NoteEditorView, self).form_valid(form)

    def get_success_url(self):
        return reverse('notes:detail', kwargs={'pk': self.note.pk})


class DetailNoteView(LoginRequiredMixin, generic.DetailView):
    """
    Display detailed info about Note object
    """
    model = Note


class ListNoteView(LoginRequiredMixin, generic.ListView):
    """
    Display all notes related to user
    """
    model = Note

    def get_queryset(self):
        queryset = super(ListNoteView, self).get_queryset()
        print(self.request.user)
        author = get_object_or_404(UserProfile, user=self.request.user)
        return queryset.filter(author=author)


class SearchResultsListView(LoginRequiredMixin, generic.ListView):
    """
    Display search results (by title or text)
    """
    model = Note
    template_name = 'notes/search_list.html'

    def get_queryset(self):
        queryset = super(SearchResultsListView, self).get_queryset()
        q = self.request.GET.get("q")
        if q:
            return queryset.filter(Q(title__icontains=q) | Q(text__icontains=q))
        return queryset
