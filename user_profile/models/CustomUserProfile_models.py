from django.conf import settings
from django.db import models
from django.core.files.base import ContentFile
from user_profile.models.CustomUserProfile_ChoiceList import (
    LOCATE_CHOICES, GENDER_CHOICES,
)
from sorl.thumbnail import get_thumbnail, delete



# ユーザ追加情報モデル
def get_user_icon_image_path(instance, filename):
    return f'user_profile/user_icon/{instance.user.pk}/{filename}'

LOCATE_CHOICES_LIST = LOCATE_CHOICES()
GENDER_CHOICES_LIST = GENDER_CHOICES()

class CustomUserProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, # @receiver 対応
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='related_custom_user_profile_model',
    )

    if settings.USE_GCS:
        user_icon_default = settings.STATIC_URL.split('/')[-1] + '/user_profile/user_icon/default/default.png'
    else:
        user_icon_default = '../' + settings.STATIC_URL + '/user_profile/user_icon/default/default.png'
    user_icon = models.ImageField(verbose_name='プロフィール画像', upload_to=get_user_icon_image_path,
                                  blank=False, null=False,
                                  default=user_icon_default)

    comment = models.CharField(verbose_name='一言コメント', max_length=255, blank=True, null=True,
                               help_text='半角英数字 255文字以下',)
    locate = models.IntegerField(verbose_name='居住地', choices=LOCATE_CHOICES_LIST, default=0, blank=True, null=True)
    birth_day = models.DateField(verbose_name='誕生日', blank=True, null=True)
    gender = models.IntegerField(verbose_name='性別', choices=GENDER_CHOICES_LIST, default=0, blank=True, null=True)

    sns_id_twitter = models.CharField(verbose_name='Twitter', max_length=255, blank=True, null=True,
                                      help_text='Twitterのユーザー名を追加してください（mitsuhiroなど）',)
    sns_id_facebook = models.CharField(verbose_name='Facebook', max_length=255, blank=True, null=True,
                                      help_text='Facebookのユーザー名を追加してください（mitsuhiroなど）',)
    sns_id_instagram = models.CharField(verbose_name='Instagram', max_length=255, blank=True, null=True,
                                      help_text='Instagramのユーザー名を追加してください（mitsuhiroなど）',)
    sns_id_linkedin = models.CharField(verbose_name='LinkedIn', max_length=255, blank=True, null=True,
                                      help_text='LinkedInのユーザー名を追加してください（mitsuhiroなど）',)
    sns_id_github = models.CharField(verbose_name='GitHub', max_length=255, blank=True, null=True,
                                      help_text='GitHubのユーザー名を追加してください（mitsuhiroなど）',)
    sns_id_kaggle = models.CharField(verbose_name='Kaggle', max_length=255, blank=True, null=True,
                                      help_text='Kaggleのユーザー名を追加してください（mitsuhiroなど）',)

    def save(self, *args, **kwargs):
        super(CustomUserProfile, self).save(*args, **kwargs)
        # user_icon 画像のリサイズ処理
        try:
            resize_width = settings.USER_ICON_RESIZE_WIDTH
            resize_height = settings.USER_ICON_RESIZE_HEIGHT
            if self.user_icon.width > resize_width or self.user_icon.height > resize_height:
                new_width = resize_width
                new_height = resize_height

                resized = get_thumbnail(self.user_icon, "{}x{}".format(new_width, new_height))
                name = self.user_icon.name.split('/')[-1]
                self.user_icon.save(name, ContentFile(resized.read()), True)
                delete(resized) # キャッシュファイルの削除
        except: pass # user_icon が無い場合には処理回避

    # objects = UserAddInfoManager()
    def __str__(self):
        return self.user.email
    
    class Meta:
        db_table = 'custom_user_profile_model'
        verbose_name=verbose_name_plural='ユーザ詳細プロフィール'