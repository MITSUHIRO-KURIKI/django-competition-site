from django.urls import include, path
from discussions_and_notebooks.views import (
    DiscussionsView, GeneralDiscussionsView, CompetitionDiscussionsView,
    DiscussionCommentsAndPostCommentView,
    DiscussionCreateView, DiscussionUpdateView, DiscussionDeleteView,
)

app_name = 'discussions'


urlpatterns = [
    path('', DiscussionsView.as_view(), name='discussions'),
    path('general', GeneralDiscussionsView.as_view(), name='general_discussions'),
    path('competition/<str:unique_competition_id>', CompetitionDiscussionsView.as_view(), name='competition_discussions'),
    path('discussion_pk/<int:pk>', DiscussionCommentsAndPostCommentView.as_view(), name='discussion_page'),
    path('upload', DiscussionCreateView.as_view(), name='discussion_create'),
    path('discussion_pk/<int:pk>/edit', DiscussionUpdateView.as_view(), name='discussion_edit'),
    path('discussion_pk/<int:pk>/delete', DiscussionDeleteView.as_view(), name='discussion_delete'),
]