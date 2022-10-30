from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from discussions_and_notebooks.models import(
    DiscussionThemes, NotebookThemes,
)
from comments.models import(
    Comments,
)
from user_inquiry.models.UserInquiry_ChoiceList import (
    SITUATION_CHOICES_LIST, FIXED_SUBJECT_CHOICES_LIST,
)
from django.utils import timezone
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save

User = get_user_model()


SITUATION_CHOICES_LIST = SITUATION_CHOICES_LIST()
FIXED_SUBJECT_CHOICES_LIST = FIXED_SUBJECT_CHOICES_LIST()

class UserInquiry(models.Model):

    inquirer_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                      related_name='related_user_inquiry_inquirer_user',)
    email = models.EmailField(verbose_name='連絡用メールアドレス', max_length=255, blank=False, null=False,
                              help_text='内容によっては私たちからお問い合わせ内容について連絡させて頂きます',)

    subject_comment = models.ForeignKey(Comments, on_delete=models.SET_NULL, blank=True, null=True,
                                        related_name='related_user_inquiry_subject_comment',)
    subject_discussion = models.ForeignKey(DiscussionThemes, on_delete=models.SET_NULL, blank=True, null=True,
                                           related_name='related_user_inquiry_subject_discussion',)
    subject_notebook = models.ForeignKey(NotebookThemes, on_delete=models.SET_NULL, blank=True, null=True,
                                         related_name='related_user_inquiry_subject_notebook',)
    
    fixed_subject = models.IntegerField(verbose_name='定形内容', choices=FIXED_SUBJECT_CHOICES_LIST, default=90, blank=True, null=True)
    subject_text = models.TextField(verbose_name='問い合わせ内容', max_length=1000, blank=True, null=True,)
    
    date_create = models.DateTimeField(default=timezone.now)

    situation = models.IntegerField(verbose_name='対応状況', choices=SITUATION_CHOICES_LIST, default=0, blank=True, null=True)
    date_complete = models.DateTimeField(default=None, blank=True, null=True,)  
    
    class Meta:
        db_table = 'user_inquiry_model'
        verbose_name=verbose_name_plural='問い合わせ一覧'


# 問い合わせ内容のメール通知（admin）
def create_inquirer_email_message(instance):
    subject_comment_pk=None
    subject_discussion_pk=None
    subject_notebook_pk=None
    if instance.subject_comment:
        subject_comment_pk = instance.subject_comment.id
    if instance.subject_discussion:
        subject_discussion_pk = instance.subject_discussion.id
    if instance.subject_notebook:
        subject_notebook_pk = instance.subject_notebook.id
    email_message = f"""
    date_create: {instance.date_create}
    fixed_subject: {instance.fixed_subject}
    subject_text:
    {instance.subject_text}

    ++++

    inquirer_user: {instance.inquirer_user} ( {instance.inquirer_user.username} )
    email: {instance.email}

    ++++

    subject_comment: {instance.subject_comment} ( pk: {subject_comment_pk} )
    subject_discussion: {instance.subject_discussion} ( pk: {subject_discussion_pk} )
    subject_notebook: {instance.subject_notebook} ( pk: {subject_notebook_pk} )

    """
    return email_message

@receiver(post_save, sender=UserInquiry)
def inquirer_notice_admin(sender, instance, created, **kwargs):
    if settings.USE_EMAIL_INQUIRY_NOTIFICATION_ADMIN:
        if created:
            email_subject = '問い合わせがありました'
            email_message = create_inquirer_email_message(instance)
            from_email = settings.FROM_EMAIL_ADDRESS  # 送信者
            recipient_list = [f'{settings.ADMIN_EMAIL_ADDRESS}']  # 宛先
            send_mail(email_subject, email_message, from_email, recipient_list, fail_silently=True)