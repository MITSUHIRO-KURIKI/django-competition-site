from django.urls import include, path
from user_profile.views import (
    AccountId_UserProfile_UpDataView, UserProfileView,
)

app_name = 'user_profile'

urlpatterns = [
    path('', AccountId_UserProfile_UpDataView.as_view(), name='user_profile_edit'),
    path('<str:unique_account_id>/', UserProfileView.as_view(), name='user_profile'),
]