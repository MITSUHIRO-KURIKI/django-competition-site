from django.urls import include, path
from submission.views import (
    SubmissionCreateView, SubmissionSelectUpdateView,
)

app_name = 'submission'

urlpatterns = [
    path('<str:unique_competition_id>', SubmissionCreateView.as_view(), name='submission'),
    path('<str:unique_competition_id>/user_submissions', SubmissionSelectUpdateView.as_view(), name='user_submissions'),
]
