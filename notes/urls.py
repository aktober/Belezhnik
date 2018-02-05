from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path(r'create/', views.CreateNoteView.as_view(), name='create'),
    path(r'detail/<int:pk>/', views.DetailNoteView.as_view(), name='detail'),
    path(r'update/<int:pk>/', views.UpdateNoteView.as_view(), name='update'),
    path(r'editor/', views.NoteEditorView.as_view(), name='editor'),
    path(r'list/', views.ListNoteView.as_view(), name='list'),
    path(r'search/', views.SearchResultsListView.as_view(), name='search'),
]