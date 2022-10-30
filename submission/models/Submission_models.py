from django.contrib.auth import get_user_model
from django.db import models
from competitions.models import Competitions
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.core.validators import (
    MinValueValidator, MaxValueValidator,
)
User = get_user_model()

# submission_file アップロード先フォルダ
def submission_file_path(instance, filename):
    return f'submission/{instance.competition.unique_competition_id}/{instance.join_user.id}/{instance.id}/{filename}'

class SubmissionUser(models.Model):

    join_user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competitions, db_index=True, on_delete=models.CASCADE)

    submission_file = models.FileField(verbose_name='Submit Data File', upload_to=submission_file_path,
                                       blank=False, null=False,
                                       validators=[FileExtensionValidator(allowed_extensions=['csv'])],
                                       help_text='提出するファイル要件はコンペティションページを確認してください')
    submission_file_description = models.CharField(verbose_name='Describe submission', max_length=140, blank=True, null=True,
                                                   help_text='アルファベット、数字、アンダーバー、ハイフン 140文字以下')

    public_score = models.FloatField(verbose_name='パブリックスコア', blank=True, null=True, default=None,)
    private_score = models.FloatField(verbose_name='プライベートスコア', blank=True, null=True, default=None,)

    Final_Evaluation = models.BooleanField(verbose_name='最終提出の対象', blank=False, null=False, default=False,
                                           help_text='最終評価の対象とするファイル')

    date_submission = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):

        # data_file処理(upload_to に instance.id を使うため)
        data_file_process = False
        if self.id is None: # instance.id がないとき(初回登録時発火)
            data_file_process = True
            submission_file_ = self.submission_file
            self.submission_file = None # 一旦 Null で保存
        
        super(SubmissionUser, self).save(*args, **kwargs) # 一度保存(data_file処理以外でも共通)

        if data_file_process:
            self.submission_file = submission_file_
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")
            super(SubmissionUser, self).save(*args, **kwargs)

    class Meta:
        db_table = 'submission_users_model'
        verbose_name=verbose_name_plural='Submission一覧'