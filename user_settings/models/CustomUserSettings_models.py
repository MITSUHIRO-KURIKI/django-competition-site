from django.conf import settings
from django.db import models



class CustomUserMailSettings(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, # @receiver 対応
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='related_custom_user_mail_settings_user',
    )

    email_receipt_permission_all = models.BooleanField(verbose_name='全ての案内を受信する', default=True)
    email_receipt_permission_important_notice = models.BooleanField(verbose_name='重要な案内のみ受信する', default=False)

    email_receipt_user_competition_notice = models.BooleanField(verbose_name='参加しているCompetitionへの新規投稿をメールで通知する', default=False,
                                                                help_text='ただし、Competition終了後には通知されません',)
    email_receipt_user_discussion_comment_notice = models.BooleanField(verbose_name='作成したDiscussionへのコメントをメールで通知する', default=False)
    email_receipt_user_notebook_comment_notice = models.BooleanField(verbose_name='作成したNotebookへのコメントをメールで通知する', default=False)

    # objects = CustomUserSettingsManager()
    def __str__(self):
        return self.user.email
    
    class Meta:
        db_table = 'custom_user_mail_settings_model'
        verbose_name=verbose_name_plural='ユーザメール受信設定'


class CustomUserProfilePublicSettings(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, # @receiver 対応
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='related_custom_user_profile_public_settings_model',
    )

    user_profile_is_authenticated_only = models.BooleanField(verbose_name='ログインているユーザーに公開する', default=True)
    user_profile_is_all_public = models.BooleanField(verbose_name='一般(ログインしていないユーザー)に公開する', default=False,
                                                     help_text='ログインているユーザーにも公開されます')
    search_robot_public = models.BooleanField(verbose_name='検索エンジンへのインデックスを許可しない', default=True)
    username_public = models.BooleanField(verbose_name='ユーザーネームを公開する', default=True)
    comment_public = models.BooleanField(verbose_name='一言コメントを公開する', default=False)
    user_icon_public = models.BooleanField(verbose_name='ユーザーアイコンを公開する', default=True)
    locate_public = models.BooleanField(verbose_name='居住地を公開する', default=False)
    birth_day_public = models.BooleanField(verbose_name='誕生日を公開する', default=False)
    gender_public = models.BooleanField(verbose_name='性別を公開する', default=False)
    sns_id_public = models.BooleanField(verbose_name='登録しているSNSのURLを公開する', default=False)

    # objects = CustomUserSettingsManager()
    def __str__(self):
        return self.user.email
    
    class Meta:
        db_table = 'custom_user_profile_public_settings_model'
        verbose_name=verbose_name_plural='ユーザプロフィール公開範囲設定'