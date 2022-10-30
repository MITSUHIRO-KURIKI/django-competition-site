from django.urls import include, path
from user_settings.views import (
    UserSettingsEmailEditView, UserSettingsProfileEditView,
)

app_name = 'user_settings'

urlpatterns = [
    path('profile_settings/', UserSettingsProfileEditView.as_view(), name='user_settings_profile_edit'),
    path('email_settings/', UserSettingsEmailEditView.as_view(), name='user_settings_email_edit'),
]