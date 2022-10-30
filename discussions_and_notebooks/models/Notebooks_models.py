from django.conf import settings
from django.db import models
from competitions.models import (
    Competitions, JoinCompetitionUsers,
)
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.core.mail import send_mass_mail
from django.dispatch import receiver
from django.db.models.signals import (
    post_save,
)
from discussions_and_notebooks.Convert.ConvertNotebook import (
    notebook_convert,
)



# notebook_file アップロード先フォルダ
def get_notebook_file_path(instance, filename):
    return f'discussions_and_notebooks/notebooks/{instance.post_user.id}/{instance.id}/{filename}'
# notebook_data_file アップロード先フォルダ
def get_notebook_data_file_path(instance, filename):
    return f'discussions_and_notebooks/notebooks/{instance.post_user.id}/{instance.id}/{filename}'
# notebook_file file_size_validator
def notebook_file_size_validator(value):
    limit = settings.NOTEBOOK_FILESIZE_LIMIT
    if value.size > limit:
        raise ValidationError(f'File too large. Size should not exceed {int(limit/1000000)}MB.')
# notebook_data_file file_size_validator
def notebook_data_file_size_validator(value):
    limit = settings.NOTEBOOK_DATA_FILESIZE_LIMIT
    if value.size > limit:
        raise ValidationError(f'File too large. Size should not exceed {int(limit/1000000)}MB.')

notebook_data_file_allowed_extensions_list = [
    'csv','tsv','txt','json','pkl','pth','model','h5','ckpt','py','zip','tar',
]

def notebook_data_file_helper():
    NOTEBOOK_DATA_FILESIZE_HELPER = \
    f'データを添付できます。<br>\
    <div class="badge badge-pill badge-info">Allowed file formats:</div>\
    <div>{ [ "."+str(x) for x in notebook_data_file_allowed_extensions_list ] }</div>\
    <div>( Maximum size: {int(settings.NOTEBOOK_DATA_FILESIZE_LIMIT/1000000)}MB )</div>'
    return NOTEBOOK_DATA_FILESIZE_HELPER


class NotebookTags(models.Model):
    
    name = models.CharField('タグ', max_length=25, blank=False, null=False, unique=True,
                            help_text='アルファベット、数字、アンダーバー、ハイフン 25文字以下')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'notebook_tags_model'
        verbose_name=verbose_name_plural='Notebookタグ一覧'


class NotebookThemes(models.Model):

    post_user = models.ForeignKey(settings.AUTH_USER_MODEL, # @receiver 対応
                                  on_delete=models.CASCADE,
                                  related_name='related_notebook_themes_post_user',)
    post_competition_or_none = models.ForeignKey(Competitions, db_index=True, on_delete=models.CASCADE, blank=True, null=True,
                                                 related_name='related_notebook_themes_post_competition_or_none',)
    tags_or_none = models.ManyToManyField(NotebookTags, verbose_name='タグ', blank=True,
                                          related_name='related_notebook_themes_tags_or_none',)
    
    title = models.CharField(verbose_name='タイトル', max_length=50, blank=False, null=False,
                             help_text='アルファベット、数字、アンダーバー、ハイフン 50文字以下')

    notebook_file = models.FileField(verbose_name='Notebook File', upload_to=get_notebook_file_path,
                                     blank=False, null=False,
                                     validators=[FileExtensionValidator(allowed_extensions=['ipynb']), notebook_file_size_validator],
                                     help_text=f'ipynb ファイルを投稿できます( 上限: {int(settings.NOTEBOOK_FILESIZE_LIMIT/1000000)}MB )')
    notebook_data_file = models.FileField(verbose_name='追加データ', upload_to=get_notebook_data_file_path,
                                          blank=True, null=True,
                                          validators=[FileExtensionValidator(allowed_extensions=notebook_data_file_allowed_extensions_list), notebook_data_file_size_validator],
                                          help_text=notebook_data_file_helper())

    is_top = models.BooleanField(default=False)
    use_bot_icon = models.BooleanField(default=False)
    date_create = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):

        # data_file処理(upload_to に instance.id を使うため)
        data_file_process = False
        if self.id is None: # instance.id がないとき(初回登録時発火)
            data_file_process = True
            notebook_file_ = self.notebook_file
            notebook_data_file_ = self.notebook_data_file
            self.notebook_file = None # 一旦 Null で保存
            self.notebook_data_file = None # 一旦 Null で保存
        
        super(NotebookThemes, self).save(*args, **kwargs) # 一度保存(data_file処理以外でも共通)

        if data_file_process:
            self.notebook_file = notebook_file_
            self.notebook_data_file = notebook_data_file_
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")
            super(NotebookThemes, self).save(*args, **kwargs)


    def __str__(self):
        return f'{self.id}_{self.title[:10]}'

    class Meta:
        db_table = 'notebook_themes_model'
        verbose_name=verbose_name_plural='Notebook一覧'


class NotebookThemesMeta(models.Model):

    object_model = models.OneToOneField(NotebookThemes, on_delete=models.CASCADE, primary_key=True,
                                        related_name='related_notebook_themes_meta_object_model',
                                        )
    notebook_style = models.TextField(verbose_name='NotebookStyle',  blank=False, null=False, default='<style></style>')
    notebook_body = models.TextField(verbose_name='NotebookBody',  blank=False, null=False, default='[]')

    def __str__(self):
        return f'{self.object_model.id}_{self.object_model.title[:10]}'

    class Meta:
        db_table = 'notebook_themes_meta_model'
        verbose_name=verbose_name_plural='NotebookMeta'


# NotebookThemes の作成/更新による NotebookThemesMeta の更新
@receiver(post_save, sender=NotebookThemes)
def notebook_themes_post_save(sender, instance, created, **kwargs):
    if instance.notebook_file:
        # notebook2html
        notebook_themes_meta = NotebookThemesMeta.objects.get_or_create(object_model=instance)
        if settings.USE_GCS:
            notebook_file_path = str(instance.notebook_file)
        else:
            notebook_file_path = settings.MEDIA_ROOT+'/'+str(instance.notebook_file)
        file_name, style, body = notebook_convert(instance, notebook_file_path)
        notebook_themes_meta[0].notebook_style = style
        notebook_themes_meta[0].notebook_body = body
        notebook_themes_meta[0].save(update_fields=['notebook_style','notebook_body'])

# コンペティションに紐づくNotebookが作成されたとき、コンペティション参加者が通知設定している場合にメール送信
def create_notebook_email_message(instance, target):
    email_message = f"""
    {target.join_user.username}さん

    参加しているコンペティション「{instance.post_competition_or_none.title}」で新たなNotebookが作成されました

    追加されたNotebookはこちらです。
    「{instance.title}」 by {instance.post_user.username}さん
    {settings.FRONTEND_URL}notebooks/notebook_pk/{instance.pk}
    """
    return email_message

@receiver(post_save, sender=NotebookThemes)
def competition_notice_notebook(sender, instance, created, **kwargs):
    if settings.USE_EMAIL_NOTIFICATION:
        if created:
            competition = instance.post_competition_or_none
            if competition:
                if competition.date_close > timezone.now():
                    join_competition_target = JoinCompetitionUsers.objects.filter(join_user__related_custom_user_mail_settings_user__email_receipt_user_competition_notice=True,competition=competition).exclude(join_user=instance.post_user).all()
                    
                    email_subject = '参加しているコンペティションで新たなNotebookが作成されました'
                    from_email = settings.FROM_EMAIL_ADDRESS  # 送信者

                    message_list=[]
                    for target in join_competition_target:
                        email_message = create_notebook_email_message(instance, target)
                        message = (email_subject, email_message, from_email, [target.join_user.email])
                        message_list.append(message)

                    message_tuple = tuple(message_list)
                    send_mass_mail(message_tuple, fail_silently=True)