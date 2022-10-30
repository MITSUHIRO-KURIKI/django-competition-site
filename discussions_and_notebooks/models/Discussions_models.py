from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from competitions.models import (
    Competitions, JoinCompetitionUsers,
)
from django.utils import timezone
from django.dispatch import receiver
from django.core.mail import send_mass_mail
from django.db.models.signals import post_save

User = get_user_model()


# summernote_helper
summernote_helper = settings.SUMMERNOTE_HELPER

class DiscussionTags(models.Model):
    
    name = models.CharField('タグ', max_length=25, blank=False, null=False, unique=True,
                            help_text='アルファベット、数字、アンダーバー、ハイフン 25文字以下')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'discussion_tags_model'
        verbose_name=verbose_name_plural='Discussionタグ一覧'

class DiscussionThemes(models.Model):

    post_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='related_discussion_themes_post_user',)
    post_competition_or_none = models.ForeignKey(Competitions, db_index=True, on_delete=models.CASCADE, blank=True, null=True,
                                                 related_name='related_discussion_themes_post_competition_or_none',)
    tags_or_none = models.ManyToManyField(DiscussionTags, verbose_name='タグ', blank=True,
                                          related_name='related_discussion_themes_tags_or_none',)
    title = models.CharField(verbose_name='タイトル', max_length=50, blank=False, null=False,
                             help_text='アルファベット、数字、アンダーバー、ハイフン 50文字以下')
    text = models.TextField(verbose_name='本文', max_length=50000, blank=False, null=False,
                            help_text=f'タグベースで 10,000文字以下。アップロード画像は横幅が{settings.SUMMERNOTE_IMAGE_WIDTH}pxに圧縮されます。'+'<br>'+summernote_helper)

    is_top = models.BooleanField(default=False)
    use_bot_icon = models.BooleanField(default=False)
    date_create = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.id}_{self.title[:10]}'

    class Meta:
        db_table = 'discussion_themes_model'
        verbose_name=verbose_name_plural='Discussion一覧'


# コンペティションに紐づくDiscussionが作成されたとき、コンペティション参加者が通知設定している場合にメール送信
def create_discussion_email_message(instance, target):
    email_message = f"""
    {target.join_user.username}さん

    参加しているコンペティション「{instance.post_competition_or_none.title}」に新たなDiscussionが追加されました

    追加されたDiscussionはこちらです。
    「{instance.title}」 by {instance.post_user.username}さん
    {settings.FRONTEND_URL}discussions/discussion_pk/{instance.pk}
    """
    return email_message

@receiver(post_save, sender=DiscussionThemes)
def competition_notice_discussion(sender, instance, created, **kwargs):
    if settings.USE_EMAIL_NOTIFICATION:
        if created:
            competition = instance.post_competition_or_none
            if competition:
                if competition.date_close > timezone.now():
                    join_competition_target = JoinCompetitionUsers.objects.filter(join_user__related_custom_user_mail_settings_user__email_receipt_user_competition_notice=True,competition=competition).exclude(join_user=instance.post_user).all()

                    email_subject = '参加しているコンペティションに新たなDiscussionが追加されました'
                    from_email = settings.FROM_EMAIL_ADDRESS  # 送信者

                    message_list=[]
                    for target in join_competition_target:
                        email_message=create_discussion_email_message(instance, target)
                        message = (email_subject, email_message, from_email, [target.join_user.email])
                        message_list.append(message)

                    message_tuple = tuple(message_list)
                    send_mass_mail(message_tuple, fail_silently=True)
