from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from uuid import uuid4
from datetime import datetime, timedelta


User = get_user_model()

# 仮登録/本登録機能
# TOKEN発行用モデル
class UserActivateTokensManager(models.Manager):

    # サインアップ時のメールアドレスの認証
    def activate_user_by_token(self, token):
        custom_user_activate_tokens = self.filter(
            token=token,
            expired_at__gte=datetime.now()
        ).first()
        # 認証URLの有効期限判定
        if custom_user_activate_tokens is None:
            raise ValidationError('仮登録URLの有効期限が切れています。再度サインアップしてください。')
        else:
            user = custom_user_activate_tokens.user
            user.is_active = True
            user.save()  # SUCCESS
    
    # メールアドレス変更時のメールアドレスの認証
    def activate_change_email_by_token(self, token):
        custom_user_email_activate_tokens = self.filter(
            token=token,
            expired_at__gte=datetime.now()
        ).first()
        # 認証URLの有効期限判定
        # 二回アクセスで 再登録されることを回避
        if custom_user_email_activate_tokens is None:
            custom_user_email_activate_tokens = self.filter(token=token).first()
            user = custom_user_email_activate_tokens.user
            user.change_email_on_request = False
            user.save()
            raise ValidationError('仮登録URLの有効期限が切れています')
        else:
            user = custom_user_email_activate_tokens.user
            if user.change_email_on_request is True:
                user.change_email_on_request = False
                user.save() # 同じアドレスによって弾かれた場合に備えて一旦モデル保存
                user.email = user.change_email # email の変更
                user.change_email = 'example@mail.com' # 変更後の email を認証したら change_email フィールドをリセット
                user.save()  # SUCCESS
            else:
                raise ValidationError('ERROR: 再度メールアドレスの変更を行ってください')

class UserActivateTokens(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    token = models.UUIDField(db_index=True, editable=False)
    expired_at = models.DateTimeField()

    objects = UserActivateTokensManager()

    def __str__(self):
        return self.user.email
    
    class Meta:
        db_table = 'custom_user_activate_tokens_model'
        verbose_name=verbose_name_plural='認証トークン発行'


# 認証のメール送信機能
@receiver(post_save, sender=User)
def publish_token(sender, instance, created, **kwargs):

    # サインアップ時のメールアドレスの認証
    # User モデルの新規作成時のみ実行
    if created:
        if instance.is_active is False:
            custom_user_activate_tokens = UserActivateTokens.objects.create(
                user = instance,
                token=str(uuid4()),
                expired_at=datetime.now()+timedelta(seconds=settings.CREATE_USER_TOKEN_EXPIRED_SECOUND_TIME)
            )

            custom_user_activate_subject = '仮登録完了'
            custom_user_activate_message = f"""
            {instance.username}さん

            仮登録を受け付けました。
            以下のURLにアクセスして、本登録を完了してください。

            {settings.FRONTEND_URL}accounts/activate/{custom_user_activate_tokens.token}
            ※このパスワード再設定URLの有効期限は{int(settings.CREATE_USER_TOKEN_EXPIRED_SECOUND_TIME / (60*60))}時間です。有効期限を過ぎると無効になります。

            """
            from_email = settings.FROM_EMAIL_ADDRESS  # 送信者
            # CustomUser.email_user を呼び出してメール送信
            instance.email_user(custom_user_activate_subject, custom_user_activate_message, from_email)
    else:
    # メールアドレス変更時のメールアドレスの認証
        if instance.change_email_on_request:
            custom_user_activate_tokens = UserActivateTokens.objects.create(
                user = instance,
                token=str(uuid4()),
                expired_at=datetime.now()+timedelta(seconds=settings.CREATE_USER_TOKEN_EXPIRED_SECOUND_TIME)
            )

            custom_user_change_email_subject = 'メールアドレスの変更を受け付けました'
            custom_user_change_email_message = f"""
            {instance.username}さん

            メールアドレスの変更を受け付けました
            以下のURLにアクセスして、新しいメールアドレスの認証完了してください。

            {settings.FRONTEND_URL}accounts/email_change/{custom_user_activate_tokens.token}
            ※このパスワード再設定URLの有効期限は{int(settings.CREATE_USER_TOKEN_EXPIRED_SECOUND_TIME / (60*60))}時間です。有効期限を過ぎると無効になります。

            """
            from_email = settings.FROM_EMAIL_ADDRESS  # 送信者
            recipient_list = [f'{instance.change_email}']  # 宛先
            send_mail(custom_user_change_email_subject, custom_user_change_email_message, from_email, recipient_list, fail_silently=True)