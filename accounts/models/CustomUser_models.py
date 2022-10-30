from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, 
    AbstractUser, BaseUserManager,
)
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
# import user_settings MODEL
from user_settings.models import (
    CustomUserMailSettings,
    CustomUserProfilePublicSettings,
)
# import user_profile MODEL
from user_profile.models import (
    CustomUserProfile,
)
from uuid import uuid4
import re
from django.utils import timezone


# username 一文字目に登録できない文字( summernote の mention対策 )
def validate_bad_username_words(value):
    first_letter_sucsess_words_unicode = '[\u3040-\u309f\u30a0-\u30ff\uff61-\uff9f\u4e00-\u9fff\u3005-\u3007\u0041-\u005a\u0061-\u007a\u0030-\u0039\uff21-\uff3a\uff41-\uff5a\uff10-\uff19]'
    bad_words = ['@', '＠']
    for word in bad_words:
        if word in value:
            raise ValidationError( f"{bad_words}は登録できません", params={'value': value}, )
    first_letter_value = value[0]
    sucsess_words_compile = re.compile(first_letter_sucsess_words_unicode)
    hit = sucsess_words_compile.match(first_letter_value)
    if hit is None:
        raise ValidationError( f"1文字目に登録できない文字が含まれています", params={'value': value}, )

# 拡張ユーザモデル
class CustomUserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields): 
        if not email:
            raise ValueError('メールアドレスの入力は必須です')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields) 
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False) 
        extra_fields.setdefault('is_superuser', False)

        # social_login のフラグを立てる/ is_set_password のフラグを消す / メール認証不要でアクティブ化する
        if password is None:
            extra_fields.setdefault('unique_account_id', uuid4().hex)
            extra_fields.setdefault('is_active', True)
            extra_fields.setdefault('is_social_login', True)
            extra_fields.setdefault('is_set_password', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True) # メール認証を行わない
        extra_fields.setdefault('is_staff', True) 
        extra_fields.setdefault('is_superuser', True) 

        if extra_fields.get('is_staff') is not True: 
            raise ValueError('Superuser must have is_staff=True.') 
        if extra_fields.get('is_superuser') is not True: 
            raise ValueError('Superuser must have is_superuser=True.') 
        return self._create_user(email, password, **extra_fields) 

class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(verbose_name='メールアドレス', db_index=True, max_length=255, unique=True)
    unique_account_id = models.SlugField(verbose_name='アカウント名(日本語不可)', max_length=32, blank=False, null=False, unique=True,
                                         help_text='アルファベット、数字、アンダーバー、ハイフン 20文字以下')
    username = models.CharField(verbose_name='ユーザー名(日本語可)', max_length=20, blank=False, null=False, unique=True,
                                help_text='半角英数字 20文字以下',
                                validators=[AbstractUser.username_validator, validate_bad_username_words])
    change_email = models.EmailField(verbose_name='変更したいメールアドレス', max_length=255,
                                     blank=False, null=False, default='example@mail.com')
    
    change_email_on_request = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_social_login = models.BooleanField(default=False)
    is_set_password = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email' # UNIQUE CustomUser
    REQUIRED_FIELDS = ['unique_account_id'] # MUST Create Superuser

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], fail_silently=True, **kwargs)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_absolute_url(self):
        return self

    class Meta(AbstractBaseUser.Meta):
        db_table = 'custom_user_model'
        verbose_name=verbose_name_plural='ユーザ基本情報'


# CustomUser 作成と同時に CustomUserProfile を作成
# CustomUser 作成と同時に CustomUserMailSettings を作成
# CustomUser 作成と同時に CustomUserProfilePublicSettings を作成
@receiver(post_save, sender=CustomUser)
def create_custom_user_profile(sender, instance, created, **kwargs):
    # User モデルの新規作成時のみ実行
    if created:
        # レコードが存在しない場合作成 / 存在する場合はレコードを返す
        custom_user_profile = CustomUserProfile.objects.get_or_create(user=instance)
        custom_user_profile = CustomUserMailSettings.objects.get_or_create(user=instance)
        custom_user_profile = CustomUserProfilePublicSettings.objects.get_or_create(user=instance)