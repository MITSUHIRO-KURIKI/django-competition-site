from django.conf import settings
from django.urls import include, path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from accounts.views import (
    SignUpView, ActivateUserView, LogInView, LogoutView,
    UserEmailUpdateView, ActivateChangeUserEmailView,
    EX_PasswordResetConfirmView, EX_PasswordChangeView,
    UserDeleteView,
)


app_name = 'accounts'

urlpatterns = [
    # サインアップ
    path('signup/', SignUpView.as_view(), name='signup'),
    # サインアップ_本登録
    path('temp_activate/', TemplateView.as_view(template_name='accounts//SignUp//temp_active_user.html'), name='temp_active_user'),
    path('activate/<uuid:token>', ActivateUserView, name='activate'),
    # ログイン/ログアウト処理
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logput'),
    # パスワード変更
    path('password_change/', EX_PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts//PasswordChange//password_change_done.html'), name='password_change_done'),
    # パスワード再設定(ソーシャルIDでパスワード未設定の場合には表示しない)
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts//ResetPassword//password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', EX_PasswordResetConfirmView.as_view(), name='password_reset_confilm'),
    # メールアドレスの変更
    path('email_change/', UserEmailUpdateView.as_view(), name='email_change'),
    path('email_change/<uuid:token>', ActivateChangeUserEmailView, name='email_change_confilm'),
    # アカウントの削除
    path('delete_account/', UserDeleteView.as_view(), name='delete_account'),
    # 外部 urls.py 参照
    path('profile/', include('user_profile.urls', namespace='user_profile')),
    path('settings/', include('user_settings.urls', namespace='user_settings')),
]

if settings.USE_EMAIL_CERTIFICATION:
    urlpatterns += [
        path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts//ResetPassword//password_reset.html',
                                                                    from_email=settings.FROM_EMAIL_ADDRESS,
                                                                    subject_template_name='accounts//ResetPassword//include//password_reset_subject.txt',
                                                                    email_template_name='accounts//ResetPassword//include//password_reset_email.html'), name='password_reset'),
    ]
else:
    urlpatterns += [
        path('password_reset/', TemplateView.as_view(template_name='accounts//ResetPassword//password_reset_.html'), name='password_reset'),
                                                                    
    ]