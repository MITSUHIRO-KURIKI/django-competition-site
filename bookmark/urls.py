from django.urls import include, path
from bookmark.views import (
    bookmark_post, 
)

app_name = 'bookmark'

urlpatterns = [
    path('post', bookmark_post, name='bookmark_post'),
]