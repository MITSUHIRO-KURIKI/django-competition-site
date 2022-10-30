from django.urls import include, path
from discussions_and_notebooks.views import (
    NotebooksView, GeneralNotebooksView, CompetitionNotebooksView,
    NotebookPageView, NotebookFileDataView, NotebookCommentsAndPostCommentView,
    NotebookCreateView, NotebookUpdateView, NotebookDeleteView,
)

app_name = 'notebooks'

urlpatterns = [
    path('', NotebooksView.as_view(), name='notebooks'),
    path('general', GeneralNotebooksView.as_view(), name='general_notebooks'),
    path('competition/<str:unique_competition_id>', CompetitionNotebooksView.as_view(), name='competition_notebooks'),
    path('notebook_pk/<int:pk>', NotebookPageView.as_view(), name='notebook_page'),
    path('notebook_pk/<int:pk>/data', NotebookFileDataView.as_view(), name='notebook_file_data'),
    path('notebook_pk/<int:pk>/comments', NotebookCommentsAndPostCommentView.as_view(), name='notebook_page_comments'),
    path('upload', NotebookCreateView.as_view(), name='notebook_create'),
    path('notebook_pk/<int:pk>/edit', NotebookUpdateView.as_view(), name='notebook_edit'),
    path('notebook_pk/<int:pk>/delete', NotebookDeleteView.as_view(), name='notebook_delete'),
]