from django.conf import settings
from django.db import models
from discussions_and_notebooks.models import(
    DiscussionThemes, NotebookThemes,
)
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import (
    post_save, pre_delete,
)
from django.utils import timezone


# summernote_helper
summernote_helper = settings.SUMMERNOTE_HELPER

class Comments(models.Model):

    post_user = models.ForeignKey(settings.AUTH_USER_MODEL, # @receiver 対応
                                  on_delete=models.CASCADE,
                                  related_name='related_comments_post_user',)
    post_discussion_theme = models.ForeignKey(DiscussionThemes, db_index=True, on_delete=models.SET_NULL, blank=True, null=True,
                                              related_name='related_comments_post_discussion_theme',)
    post_notebook_theme = models.ForeignKey(NotebookThemes, db_index=True, on_delete=models.SET_NULL, blank=True, null=True,
                                            related_name='related_comments_post_notebook_theme',)
    text = models.TextField(verbose_name='本文', max_length=1000000, blank=False, null=False,
                            help_text=f'アップロード画像は横幅が{settings.SUMMERNOTE_IMAGE_WIDTH}pxに圧縮されます。'+'<br>'+summernote_helper)
    date_create = models.DateTimeField(default=timezone.now)
    
    
    class Meta:
        db_table = 'comments_model'
        verbose_name=verbose_name_plural='comment一覧'


class DiscussionCommentsCount(models.Model):
    post_discussion_theme = models.ForeignKey(DiscussionThemes, db_index=True, on_delete=models.SET_NULL, blank=True, null=True,
                                              related_name='related_comments_count_post_discussion_theme',)
    count = models.IntegerField(blank=False, null=False, default=0,)
    latest_post_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'discussion_comments_count_model'
        verbose_name=verbose_name_plural='discussion_comment数一覧'


class NotebookCommentsCount(models.Model):
    post_notebook_theme = models.ForeignKey(NotebookThemes, db_index=True, on_delete=models.SET_NULL, blank=True, null=True,
                                            related_name='related_comments_count_post_notebook_theme',)
    count = models.IntegerField(blank=False, null=False, default=0,)
    latest_post_date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'notebook_comments_count_model'
        verbose_name=verbose_name_plural='notebook_comment数一覧'


# コメントが投稿/削除されたときに DiscussionCommentsCount を更新
@receiver(post_save, sender=Comments)
def discussion_post_save_comment(sender, instance, created, **kwargs):
    if created:
        if instance.post_discussion_theme:
            discussion_comment_count = DiscussionCommentsCount.objects.get_or_create(post_discussion_theme=instance.post_discussion_theme)
            # 初めてコメントが投稿されたとき
            if discussion_comment_count[1]:
                discussion_comment_count[0].count = 1
            else:
                discussion_comment_count[0].count = Comments.objects.filter(post_discussion_theme=instance.post_discussion_theme).count()
            discussion_comment_count[0].latest_post_date = instance.date_create
            discussion_comment_count[0].save(update_fields=['count','latest_post_date'])
@receiver(pre_delete, sender=Comments)
def discussion_pre_delete_comment(sender, instance, **kwargs):
    if instance.post_discussion_theme:
        discussion_comment_count = DiscussionCommentsCount.objects.get_or_create(post_discussion_theme=instance.post_discussion_theme)
        discussion_comment_count[0].count -= 1
        discussion_comment_count[0].save(update_fields=['count'])

# コメントが投稿/削除されたときに NotebookCommentsCount を更新
@receiver(post_save, sender=Comments)
def notebook_post_save_comment(sender, instance, created, **kwargs):
    if created:
        if instance.post_notebook_theme:
            notebook_comment_count = NotebookCommentsCount.objects.get_or_create(post_notebook_theme=instance.post_notebook_theme)
            # 初めてコメントが投稿されたとき
            if notebook_comment_count[1]:
                notebook_comment_count[0].count = 1
            else:
                notebook_comment_count[0].count = Comments.objects.filter(post_notebook_theme=instance.post_notebook_theme).count()
            notebook_comment_count[0].latest_post_date = instance.date_create
            notebook_comment_count[0].save(update_fields=['count','latest_post_date'])
@receiver(pre_delete, sender=Comments)
def notebook_pre_delete_comment(sender, instance, **kwargs):
    if instance.post_notebook_theme:
        discussion_comment_count = NotebookCommentsCount.objects.get_or_create(post_notebook_theme=instance.post_notebook_theme)
        discussion_comment_count[0].count -= 1
        discussion_comment_count[0].save(update_fields=['count'])


# コメントが投稿されたDiscussion/Notebookの作成者が通知設定している場合に作成者にメール送信
def create_comment_email_message(instance, target_subject, flug):
    if flug == 'Discussion':
        email_message = f"""
        {target_subject.post_user.username}さん

        作成した{flug}「{target_subject.title}」に{instance.post_user.username}さんがコメントしました

        コメントがついた{flug}はこちらです
        {settings.FRONTEND_URL}discussions/discussion_pk/{target_subject.pk}
        """
    else:
        email_message = f"""
        {target_subject.post_user.username}さん

        作成した{flug}「{target_subject.title}」に{instance.post_user.username}さんがコメントしました

        コメントがついた{flug}はこちらです
        {settings.FRONTEND_URL}notebooks/notebook_pk/{target_subject.pk}
        """
    return email_message

@receiver(post_save, sender=Comments)
def discussion_or_notebook_notice_comment(sender, instance, created, **kwargs):
    if settings.USE_EMAIL_NOTIFICATION:
        if created:
            email_subject=None
            # Discussionへのコメント
            if instance.post_discussion_theme != None:
                target_subject = DiscussionThemes.objects.filter(pk=instance.post_discussion_theme.id).first()
                if target_subject.post_user != instance.post_user and target_subject.post_user.related_custom_user_mail_settings_user.email_receipt_user_discussion_comment_notice:
                    email_subject = '作成したDiscussionにコメントがつきました'
                    flug='Discussion'
            
            # Notebookへのコメント
            elif instance.post_notebook_theme != None:
                target_subject = NotebookThemes.objects.filter(pk=instance.post_notebook_theme.id).first()
                if target_subject.post_user != instance.post_user and target_subject.post_user.related_custom_user_mail_settings_user.email_receipt_user_notebook_comment_notice:
                    email_subject = '作成したNotebookにコメントがつきました'
                    flug='Notebook'
            
            if email_subject != None:
                email_message = create_comment_email_message(instance, target_subject, flug)
                from_email = settings.FROM_EMAIL_ADDRESS  # 送信者
                recipient_list = [f'{target_subject.post_user.email}']  # 宛先
                send_mail(email_subject, email_message, from_email, recipient_list, fail_silently=True)

