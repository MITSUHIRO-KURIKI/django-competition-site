from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


User = get_user_model()


# ログイン
class LogInForm(AuthenticationForm):

    login_remenber = forms.BooleanField(label='ログイン状態を保持する', required=False)
