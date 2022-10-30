from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.core.files.base import ContentFile
from sorl.thumbnail import get_thumbnail, delete
from django.core.exceptions import ValidationError
from django.core.validators import (
    FileExtensionValidator,
    MinValueValidator, MaxValueValidator,
)
from django.urls import reverse


User = get_user_model()


# overall アップロード先フォルダ
def get_overall_image_path(instance, filename):
    return f'competitions/overall/{instance.id}/{filename}'
# data_file アップロード先フォルダ
def get_data_file_path(instance, filename):
    return f'competitions/data_file/{instance.id}/{filename}'
# answer_file アップロード先フォルダ
def get_answer_file_path(instance, filename):
    return f'competitions/answer/{instance.id}/{filename}'
# username 一文字目に登録できない文字( summernote の mention対策 )
def validate_bad_unique_competition_id_words(value):
    bad_words = ['create']
    for word in bad_words:
        if len(value) == len(word):
            if word in value:
                raise ValidationError( f"{bad_words}は登録できません", params={'value': value}, )

# summernote_helper
summernote_helper = settings.SUMMERNOTE_HELPER


# metrics_help_text
def metrics_help_text():
    help_text = '対応している sklearn.metrics.XXXX の XXXX （ただし、1文字目を大文字とする）を入力するか、オリジナルの評価指標名を入力<br/>\
                <div class="badge badge-pill badge-info" data-toggle="collapse" href="#MultiCollapse-metrics" aria-expanded="false" aria-controls="MultiCollapse-metrics">対応している評価関数名<i class="bi bi-arrows-expand ml-2"></i></div>\
                <div class="collapse multi-collapse" id="MultiCollapse-metrics">\
                R2_score<br/>\
                Mean_absolute_error<br/>\
                Mean_squared_error<br/>\
                Root_mean_squared_error<br/>\
                Mean_squared_log_error<br/>\
                Root_mean_squared_log_error<br/>\
                Accuracy_score<br/>\
                Error_rate<br/>\
                Precision_score<br/>\
                Recall_score<br/>\
                F1_score (_mean / _macro / _micro / _weighted / _none)<br/>\
                F0.5_score (_mean / _macro / _micro / _weighted / _none)<br/>\
                F2_score (_mean / _macro / _micro / _weighted / _none)<br/>\
                Log_loss<br/>\
                Roc_auc_score (_Multiclass / _Multilabel)<br/>\
                Quadratic_weighted_kappa<br/>\
                MAP@K<br/>\
                </div>'
    return help_text


class CompetitionsTags(models.Model):
    
    name = models.CharField('タグ', max_length=25, blank=False, null=False, unique=True,
                            help_text='アルファベット、数字、アンダーバー、ハイフン 25文字以下')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'competitions_tags_model'
        verbose_name=verbose_name_plural='Competitionタグ一覧'


class Competitions(models.Model):

    create_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False,
                                    related_name='related_competitions_create_user',)

    unique_competition_id = models.SlugField(verbose_name='コンペティションID', db_index=True, max_length=50, blank=False, null=False, unique=True,
                                             validators=[validate_bad_unique_competition_id_words],
                                             help_text='アルファベット、数字、アンダーバー、ハイフン 50文字以下')

    if settings.USE_GCS:
        overall_default = settings.STATIC_URL.split('/')[-1] + '/competitions/overall/default/default.jpg'
    else:
        overall_default = '../' + settings.STATIC_URL + '/competitions/overall/default/default.jpg'
    overall = models.ImageField(verbose_name='Competition_Overall', upload_to=get_overall_image_path,
                                blank=False, null=False,
                                default=overall_default,
                                help_text=f'中心から {settings.COMPETITION_OVERALL_RESIZE_WIDTH}*{settings.COMPETITION_OVERALL_RESIZE_HEIGHT} にリサイズされます')

    title = models.CharField(verbose_name='タイトル', db_index=True, max_length=255, blank=False, null=False, unique=True,
                             help_text='アルファベット、数字、アンダーバー、ハイフン 255文字以下')
    subtitle = models.CharField(verbose_name='見出し説明', max_length=255, blank=False, null=False,
                                help_text='アルファベット、数字、アンダーバー、ハイフン 255文字以下')
    tags = models.ManyToManyField(CompetitionsTags, verbose_name='タグ', blank=True,
                                  related_name='related_competitions_tags',)

    overview_text = models.TextField(verbose_name='概要', blank=True, null=True,
                                     help_text=summernote_helper,)

    evaluation_text = models.TextField(verbose_name='評価基準', blank=True, null=True,
                                       help_text=summernote_helper,)
    metrics = models.CharField(verbose_name='評価指標', max_length=255, blank=True, null=True,
                               help_text=metrics_help_text())
    Evaluation_Minimize = models.BooleanField(verbose_name='評価指標の最小を上位とする', blank=False, null=False, default=True,
                                              help_text='チェックを外すと最大を上位とします')
    
    rule_text = models.TextField(verbose_name='ルール', blank=True, null=True,
                                 help_text=summernote_helper,)

    data_text = models.TextField(verbose_name='提供データの説明', blank=True, null=True,
                                 help_text=summernote_helper,)
    data_file = models.FileField(verbose_name='提供データ', upload_to=get_data_file_path,
                                blank=True, null=True,
                                validators=[FileExtensionValidator(allowed_extensions=['zip', 'tar'])],
                                help_text='提供するデータファイル(train.csv, test.csv等)をzip/tarにまとめてアップロードしてください')

    answer_file = models.FileField(verbose_name='正解データ', upload_to=get_answer_file_path,
                                   blank=True, null=True,
                                   validators=[FileExtensionValidator(allowed_extensions=['csv'])],
                                   help_text='正解ファイルのcsv。<br/>\
                                              評価対象のカラム名は predict とし、公開スコア用のカラム名 division_public_or_private の各行へ public か private を入力すること。')
    target_cols_name = models.CharField(verbose_name='予測値のカラム名', max_length=255, blank=False, null=False, default='predict',
                                        help_text='予測値のカラム名。アップロードする正解データの正解値も同じカラム名として保存する。<br/>\
                                                   カンマ区切りで複数行も指定可能。')

    Submission_Daily_Limit = models.IntegerField(verbose_name='1日(24h)あたりの提出上限', blank=False, null=False, default=5,
                                                 validators=[MinValueValidator(1), MaxValueValidator(20)],
                                                 help_text='24時間あたりの提出上限（最小値: 1, 最大値: 20）')
    Final_Evaluation_Limit = models.IntegerField(verbose_name='最終提出サブミッション上限', blank=False, null=False, default=2,
                                                 validators=[MinValueValidator(1), MaxValueValidator(5)],
                                                 help_text='最終提出として選択できるサブミッションの上限（最小値: 1, 最大値: 5）')

    is_public = models.BooleanField(verbose_name='コンペティションの公開', default=False,
                                    help_text='チェックを入れると一般に公開されます')
    create_initial_discussion = models.BooleanField(verbose_name='初期ディスカッションの作成', default=False,
                                                    help_text='主催者への質問受付のディスカッションを作成します')
    date_open = models.DateTimeField(verbose_name='開始日', default=timezone.now, blank=False, null=False)
    date_close = models.DateTimeField(verbose_name='終了日', default=timezone.now, blank=False, null=False)

    def save(self, *args, **kwargs):

        # data_file処理(upload_to に instance.id を使うため)
        data_file_process = False
        if self.id is None: # instance.id がないとき(初回登録時発火)
            data_file_process = True
            data_file_ = self.data_file
            answer_file_ = self.answer_file
            self.data_file = None # 一旦 Null で保存
            self.answer_file = None # 一旦 Null で保存
        
        super(Competitions, self).save(*args, **kwargs) # 一度保存(data_file処理以外でも共通)

        if data_file_process:
            self.data_file = data_file_
            self.answer_file = answer_file_
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")
            super(Competitions, self).save(*args, **kwargs)

        # overall 画像のリサイズ処理
        try:
            resize_width = settings.COMPETITION_OVERALL_RESIZE_WIDTH
            resize_height = settings.COMPETITION_OVERALL_RESIZE_HEIGHT
            # 画像が規定サイズの場合にはリサイズを実行しない
            if self.overall.width != resize_width and self.overall.height != resize_height:
                resized = get_thumbnail(self.overall, "{}x{}".format(resize_width, resize_height), crop='center', quality=99)
                name = self.overall.name.split('/')[-1]
                self.overall.save(name, ContentFile(resized.read()), True)
                delete(resized) # キャッシュファイルの削除
        except: pass # overall が無い場合には処理回避


    def __str__(self):
        return self.unique_competition_id
    
    class Meta:
        db_table = 'competitions_model'
        verbose_name=verbose_name_plural='Competition一覧'


class JoinCompetitionUsers(models.Model):

    join_user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE,
                                  related_name='related_join_competition_users_user',)
    competition = models.ForeignKey(Competitions, db_index=True, on_delete=models.CASCADE,
                                    related_name='related_join_competition_users_competitions',)
    date_joined = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'join_competition_users_model'
        verbose_name=verbose_name_plural='Competition参加ユーザ一覧'
