from django.conf import settings
from django.contrib.auth import (
    get_user_model, logout,
)
from django.contrib.auth.views import (
    PasswordResetConfirmView, 
    PasswordChangeView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    UpdateView, DeleteView
)
from accounts.models import (
    UserActivateTokens, 
)
from accounts.forms import (
    EX_PasswordChangeForm, 
    UserEmailUpdateForm,
    EX_SetPasswordForm,
    UserDeleteForm,
)
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from axes.utils import reset


User = get_user_model()


# ユーザ登録情報の変更 メールアドレス
class UserEmailUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    template_name = 'accounts/ChangeEmail/user_email_update_form.html'
    success_url = reverse_lazy('accounts:email_change')
    form_class = UserEmailUpdateForm

    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):

        # メール認証する場合としない場合のメッセージの分岐
        if settings.USE_EMAIL_CERTIFICATION:
            messages.add_message(self.request, messages.INFO,
                                f'Change of e-mail address has been accepted.\n\
                                An authentication email has been sent to your new email address.\n\
                                Please complete the authentication from the email sent to you.',
                                )
        else:
            messages.add_message(self.request, messages.INFO,
                                f'Email address change completed.'
                                )
        return super().form_valid(form)

def ActivateChangeUserEmailView(request, token):

    token_res = UserActivateTokens.objects.activate_change_email_by_token(token)
    logout(request)
    messages.add_message(request, messages.INFO,
                            f'Email address change completed.\n\
                              Please login with your new email address.')
    return redirect('login')


# ユーザ登録情報の変更 パスワード
class EX_PasswordChangeView(PasswordChangeView):
    template_name = 'accounts/PasswordChange/password_change.html'
    form_class = EX_PasswordChangeForm


# ユーザ登録情報の変更 パスワードリセット
# django-axes
# https://stackoverflow.com/questions/56015855/how-to-perform-additional-actions-on-passwordreset-in-django
class EX_PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/ResetPassword/password_reset_confilm.html'
    form_class = EX_SetPasswordForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        reset(username=user.email)
        messages.add_message(self.request, messages.INFO,
                                f'Password reset completed.\n\
                                  Please login with your a new password.')
        return super().form_valid(form)


# ユーザ情報の削除
class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'accounts/UserDelete/delete.html'
    success_url = reverse_lazy('login')
    form_class = UserDeleteForm

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        form = self.get_form()
        
        check_text = request.POST['check_text']

        if check_text=='delete':
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            messages.add_message(self.request, messages.WARNING,
                                 f'False',)
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object.delete()
        messages.add_message(self.request, messages.INFO,
                            f'I have withdrawn from the service.\n\
                            Thank you for using our service.',)
        return redirect(self.get_success_url())