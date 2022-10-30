from django.conf import settings
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import (
    SetPasswordForm,
)

User = get_user_model()


# ユーザ登録情報の変更 メールアドレス
class UserEmailUpdateForm(forms.ModelForm):

    def save(self, commit=False):
        user = super().save(commit=False)
        # ソーシャルIDの場合にはメールアドレスの変更前にパスワードの変更を求める
        if user.is_set_password:
            if User.objects.filter(email=user.change_email).exists():
                raise ValidationError('既に登録済みのメールアドレスです')
            else:
                # メール認証を行う場合と行わない場合
                if settings.USE_EMAIL_CERTIFICATION:
                    user.change_email_on_request = True
                else:
                    user.change_email_on_request = False # メール認証をしない
                    user.email = user.change_email # emailを変更
                    user.change_email = 'example@mail.com' # ダミーデータの設定
                
                user.save()
                return user
        else:
            raise ValidationError('ソーシャルIDで作成されたユーザーのメールアドレスをするには、先にパスワードを設定してください。')

    class Meta:
        model = User
        fields = ["change_email", ]


# ユーザ登録情報の変更 アカウントID(InlineForm)
class AccountIdUpdateWithInlinesForm(forms.ModelForm):

    def save(self, commit=False):
        user = super(AccountIdUpdateWithInlinesForm, self).save(commit=False)
        user.change_email_on_request = False
        user.save()
        return user

    class Meta:
        model = User
        fields = ['username', ]
        # @mentionの遷移先URLが変更されないように unique_account_id は変更不可
        # fields = ['unique_account_id', 'username', ]


# ユーザ登録情報の変更 パスワード
class EX_PasswordChangeForm(SetPasswordForm):

    field_order = ['new_password1', 'new_password2']

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.change_email_on_request = False # メール変更で未認証の場合にはパスワード変更の要求をリセット
            self.user.is_set_password = True # ソーシャルIDのパスワードセットを確認してメールアドレスの変更を受け付ける
            self.user.save()
        return self.user

# ユーザ登録情報の変更 パスワードリセット
class EX_SetPasswordForm(SetPasswordForm):

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.change_email_on_request = False # メール変更で未認証の場合にはパスワード変更の要求をリセット
            self.user.save()
        return self.user

# ユーザ登録情報の変更 アカウントの削除
class UserDeleteForm(forms.Form):
    check_text = forms.CharField(label="確認",
                                 help_text='削除するには「delete」と入力してボタンを押してください')