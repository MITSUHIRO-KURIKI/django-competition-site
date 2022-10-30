from django.urls import include, path
from vote.views import (
    vote_post, 
)

app_name = 'vote'

urlpatterns = [
    path('post', vote_post, name='vote_post'),
]