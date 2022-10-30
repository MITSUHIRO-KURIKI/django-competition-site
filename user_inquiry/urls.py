from django.urls import include, path
from user_inquiry.views import (
    UserInquiryCreateView,
)

app_name = 'user_inquiry'

urlpatterns = [
    path('', UserInquiryCreateView.as_view(), name='user_inquiry_form'),
]