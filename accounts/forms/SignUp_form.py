from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()

# サインアップ
class SignUpForm(UserCreationForm):

    def save(self, commit=True):
        user = super().save(commit=False)
        cleaned_data = super().clean()
        user.email = cleaned_data.get('email')
        user.username = cleaned_data.get("unique_account_id") # 初期の名前はユーザID
        # メール認証を行う場合と行わない場合
        if settings.USE_EMAIL_CERTIFICATION:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return user

    # 同じメールアドレスで仮登録の場合レコードを消去して再度仮登録を実行
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email, is_active=False).exists():
            User.objects.filter(email=email, is_active=False).delete()
        return email

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('unique_account_id', 'email',)