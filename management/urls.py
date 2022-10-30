from django.conf import settings
from django.urls import include, path
from management.views import (
    HomeView,
    TagsUpdateView,
    InquiryListView,
    CompetitionTagsDeleteView, DiscussionTagsDeleteView, NotebookTagsDeleteView,
)
if settings.DEBUG:
    from management.views import CreateDummyData


app_name = 'management'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('tags/', TagsUpdateView.as_view(), name='tags_list'),
    path('tags/delete/competition/<int:pk>', CompetitionTagsDeleteView.as_view(), name='delete_competition_tags'),
    path('tags/delete/discussion/<int:pk>', DiscussionTagsDeleteView.as_view(), name='delete_discussion_tags'),
    path('tags/delete/notebook/<int:pk>', NotebookTagsDeleteView.as_view(), name='delete_notebook_tags'),
    path('inquiry/', InquiryListView.as_view(), name='inquiry_list'),
    # path('inquiry/<int:pk>', .as_view(), name='inquiry_list_detail'),
]
if settings.DEBUG:
    urlpatterns += [path('dummy/create', CreateDummyData.as_view(), name='create_dummy_data'),]