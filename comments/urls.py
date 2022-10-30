from django.urls import include, path
from comments.views import (
    CommentUpdateView, CommentDeleteView,
)

app_name = 'comments'

urlpatterns = [
    path('<int:pk>/edit', CommentUpdateView.as_view(), name='comment_update'),
    path('<int:pk>/delete', CommentDeleteView.as_view(), name='comment_delete'),
]