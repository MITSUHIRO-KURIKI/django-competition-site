from django.conf import settings
from accounts.models.CustomUser_models import (
    CustomUser,
)
from competitions.models import (
    Competitions, JoinCompetitionUsers, CompetitionsTags,
)
from discussions_and_notebooks.models import (
    DiscussionTags, DiscussionThemes,
)
from discussions_and_notebooks.models import (
    NotebookTags, NotebookThemes,
)
from submission.models import (
    SubmissionUser,
)
from comments.models import (
    Comments,
)
from bookmark.models import(
    DiscussionBookmarks, NotebookBookmarks, CommentBookmarks,
)
from vote.models import(
    DiscussionVotes, NotebookVotes, CommentVotes,
)
from user_settings.models.CustomUserSettings_models import (
    CustomUserMailSettings,
)
from django.views.generic import TemplateView
from django.utils import timezone
import datetime
import time
import random
from uuid import uuid4
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


def dummy_text(short=False):
    if not short:
        text='<h1 class=""><span style="font-size: 2.5rem;">これはダミーコンペティションです。</span><br></h1><h2 class="">これはダミーコンペティションです。</h2><h3 class="">これはダミーコンペティションです。</h3><h4 class="">これはダミーコンペティションです。</h4><h5 class="">これはダミーコンペティションです。</h5><h6 class="">これはダミーコンペティションです。</h6><p><br></p><hr><p><br></p><p><br></p><blockquote class="blockquote"><p>これはダミーコンペティションです。</p></blockquote><p><br></p><pre class="">これはダミーコンペティションです。</pre><p><br></p><p><a href="https://google.com" rel="noopener noreferrer" target="_blank">これはダミーコンペティションです。</a></p><p><br><br></p><table class="table table-sm table-striped table-hover table-bordered col-11 text-break" style="width: 720.675px; flex-basis: 91.6667%; max-width: 91.6667%;"><tbody><tr class="row m-0 p-0"><td class="col m-0 p-0" style="width: 359.337px;">これはダミーコンペティションです。<br></td><td class="col m-0 p-0" style="width: 359.337px;">これはダミーコンペティションです。<br></td></tr><tr class="row m-0 p-0" style="background-image: ; background-position-x: ; background-position-y: ; background-size: ; background-repeat-x: ; background-repeat-y: ; background-attachment: ; background-origin: ; background-clip: ;"><td class="col m-0 p-0" style="width: 359.337px;">これはダミーコンペティションです。<br></td><td class="col m-0 p-0" style="width: 359.337px;">これはダミーコンペティションです。<br></td></tr><tr class="row m-0 p-0"><td class="col m-0 p-0" style="width: 359.337px;">これはダミーコンペティションです。<br></td><td class="col m-0 p-0" style="width: 359.337px;">これはダミーコンペティションです。<br></td></tr></tbody></table>'
    else:
        text='<p><span style="font-size: 1rem;">ダミーコメント</span><br></p><p><br></p><blockquote class="blockquote"><p>ダミーコメント</p></blockquote><p><br></p><pre class="">ダミーコメント</pre><p><br></p><table class="table table-sm table-striped table-hover table-bordered col-11 text-break" style="width: 797.675px; flex-basis: 91.6667%; max-width: 91.6667%;"><tbody><tr class="row m-0 p-0"><td class="col m-0 p-0" style="width: 397.837px;">ダミー</td><td class="col m-0 p-0" style="width: 397.837px;">ダミー</td></tr><tr class="row m-0 p-0"><td class="col m-0 p-0" style="width: 397.837px;">ダミー</td><td class="col m-0 p-0" style="width: 397.837px;">ダミー</td></tr></tbody></table>'
    return text

def create_date_random():
    if random.random() > 0.5:
        m1=100
        if random.random() > 0.5:
            m2=100
        else:
            m2=1000
    else:
        m1=1000
        if random.random() > 0.5:
            m2=100
        else:
            m2=1000
    m1 = random.random()*10
    m2 = random.random()*10
    return m1, m2

if settings.USE_GCS:
    competition_data_file_path = None
    competition_answer_SINGLE_file_path = None
    competition_answer_MULTI_file_path = None
else:
    competition_data_file_path = '../' + settings.STATIC_URL + '/SampleData/Competition/SampleCompetitionProvidedData.zip'
    competition_answer_SINGLE_file_path = '../' + settings.STATIC_URL + '/SampleData/Competition/answer.csv'
    competition_answer_MULTI_file_path = '../' + settings.STATIC_URL + '/SampleData/Competition/answer_multi.csv'
    notebook_file_path = '../' + settings.STATIC_URL + '/SampleData/Notebook/Sample1.ipynb'


class CreateDummyData(TemplateView, LoginRequiredMixin):

    template_name = "management/create_dummy_data/create_dummy_data.html"
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        IS_DEBUG = settings.DEBUG
        context.update({'IS_DEBUG': IS_DEBUG,
                        })
        return context
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            if not settings.DEBUG:
                messages.add_message(self.request, messages.INFO,
                                    f'DEBUG環境のみ使用できます',)
                return redirect('management:home')
            elif settings.USE_EMAIL_CERTIFICATION or settings.USE_EMAIL_NOTIFICATION or settings.USE_DJANGO_TOOLBAR:
                messages.add_message(self.request, messages.INFO,
                                    f'ダミーデータを作成するには一旦settingsの USE_EMAIL_CERTIFICATION, USE_EMAIL_NOTIFICATION, USE_DJANGO_TOOLBAR をOFFにしてください',)
                return redirect('management:home')
            return super().get(self, request, *args, **kwargs)
        else:
            raise Http404

    def post(self, request, *args, **kwargs):

        if self.request.user.is_superuser:
            if settings.USE_EMAIL_CERTIFICATION or settings.USE_EMAIL_NOTIFICATION:
                messages.add_message(self.request, messages.INFO,
                                    f'ダミーデータを作成するには一旦settingsの USE_EMAIL_CERTIFICATION と USE_EMAIL_NOTIFICATION をOFFにしてください',)
                return redirect('management:home')

            t_start_1 = time.time()
            print('*'*20);print('START CREATE DUMMY DATA');print('*'*20)

            ########## 
            # サーバ負荷軽減
            ##########
            SLEEP_TIME=0

            ##########
            # 作成数の設定
            ##########
            # ユーザの作成
            GENERAL_N=8
            STAFF_N=2
            # タグの作成
            TAGS_N=3
            # コンペティションの作成
            COMP_N=5


            # ユーザの作成
            unique_account_id_list=[]
            for i in range(GENERAL_N):
                uuid=str(uuid4())[:6]
                m1, _ = create_date_random()
                if random.random() > 0.5:
                    date_joined = timezone.now() - datetime.timedelta(hours=int(random.random()*m1))
                else:
                    date_joined = timezone.now() + datetime.timedelta(hours=int(random.random()*m1))
                CustomUser.objects.create_user(email=f'{uuid}@mail.com',
                                               unique_account_id=f'{uuid}_userID',
                                               username=f'user_{uuid}',
                                               is_active=True,
                                               is_staff=False,
                                               is_superuser=False,
                                               date_joined=date_joined,
                                               )
                unique_account_id_list.append(f'{uuid}_userID')
                time.sleep(SLEEP_TIME)
            for i in range(STAFF_N):
                uuid=str(uuid4())[:6]
                m1, _ = create_date_random()
                if random.random() > 0.5:
                    date_joined = timezone.now() - datetime.timedelta(hours=int(random.random()*m1))
                else:
                    date_joined = timezone.now() + datetime.timedelta(hours=int(random.random()*m1))
                CustomUser.objects.create_user(email=f'staff_{uuid}@mail.com',
                                               unique_account_id=f'STAFF_{uuid}_userID',
                                               username=f'user_{uuid}_STAFF',
                                               is_active=True,
                                               is_staff=True,
                                               is_superuser=False,
                                               date_joined=date_joined,
                                               )
                unique_account_id_list.append(f'STAFF_{uuid}_userID')
                time.sleep(SLEEP_TIME)
            print('*'*20);print('CREATE USER');print(unique_account_id_list);print('*'*20)

            # メール通知設定
            for unique_account_id in unique_account_id_list:
                email_receipt_user_competition_notice=False
                email_receipt_user_discussion_comment_notice=False
                email_receipt_user_notebook_comment_notice=False
                if random.random() > 0.5:
                    email_receipt_user_competition_notice=True
                if random.random() > 0.5:
                    email_receipt_user_discussion_comment_notice=True
                if random.random() > 0.5:
                    email_receipt_user_notebook_comment_notice=True
                
                custom_user_mail_settings_model = CustomUserMailSettings.objects.filter(user__unique_account_id=unique_account_id).all()
                custom_user_mail_settings_model.update(email_receipt_user_competition_notice=email_receipt_user_competition_notice,
                                                       email_receipt_user_discussion_comment_notice=email_receipt_user_discussion_comment_notice,
                                                       email_receipt_user_notebook_comment_notice=email_receipt_user_notebook_comment_notice,
                                                       )

            # タグの作成
            competition_tags_name_list=[]
            discussion_tags_name_list=[]
            notebook_tags_name_list=[]
            for i in range(TAGS_N):
                uuid=str(uuid4())[:3]
                CompetitionsTags.objects.create(name=f'dummy-comp-{uuid}')
                DiscussionTags.objects.create(name=f'dummy-dis-{uuid}')
                NotebookTags.objects.create(name=f'dummy-note-{uuid}')
                competition_tags_name_list.append(f'dummy-comp-{uuid}')
                discussion_tags_name_list.append(f'dummy-dis-{uuid}')
                notebook_tags_name_list.append(f'dummy-note-{uuid}')
                time.sleep(SLEEP_TIME)

            print('*'*20);print('CREATE TAGS');print(competition_tags_name_list);print(discussion_tags_name_list);print(notebook_tags_name_list);print('*'*20)


            # コンペティションの作成
            competition_unique_competition_id_list=[]
            for i in range(COMP_N):
                uuid=str(uuid4())[:6]
                m1, m2 = create_date_random()
                
                # 40% は終了させる
                if random.random() > 0.4:
                    date_open = timezone.now() - datetime.timedelta(hours=int(random.random()*m1))
                    date_close = timezone.now() + datetime.timedelta(hours=int(random.random()*m2))
                else:
                    date_close = timezone.now() + datetime.timedelta(hours=int(random.random()*-m2))
                    date_open = date_close - datetime.timedelta(hours=int(random.random()*m1))
                
                tags_list=[]
                # 30%の確率でタグが付与され、それぞれ60%の確率で割当が行われる
                if random.random() > 0.7:
                    for i in range(TAGS_N):
                        if random.random() > 0.6:
                            tags_list.append(competition_tags_name_list[i])
                tags=CompetitionsTags.objects.filter(name__in=tags_list)
                if random.random() > 0.5:
                    Competitions.objects.create(create_user=self.request.user,
                                                unique_competition_id=uuid,
                                                title=f'ダミーコンペ-シングル予測({uuid})',
                                                subtitle='これはダミーコンペです',
                                                overview_text=dummy_text(),
                                                evaluation_text=dummy_text(),
                                                metrics='Accuracy_score',
                                                Evaluation_Minimize=False,
                                                rule_text=dummy_text(),
                                                data_text=dummy_text(),
                                                data_file=competition_data_file_path,
                                                answer_file=competition_answer_SINGLE_file_path,
                                                target_cols_name='predict',
                                                is_public=True,
                                                date_open=date_open,
                                                date_close=date_close,
                                                ).tags.set(tags)
                else:
                    Competitions.objects.create(create_user=self.request.user,
                                                unique_competition_id=uuid,
                                                title=f'ダミーコンペ-マルチ予測({uuid})',
                                                subtitle='これはダミーコンペです',
                                                overview_text=dummy_text(),
                                                evaluation_text=dummy_text(),
                                                metrics='Root_mean_squared_error',
                                                Evaluation_Minimize=True,
                                                rule_text=dummy_text(),
                                                data_text=dummy_text(),
                                                data_file=competition_data_file_path,
                                                answer_file=competition_answer_MULTI_file_path,
                                                target_cols_name='cat, dog',
                                                is_public=True,
                                                date_open=date_open,
                                                date_close=date_close,
                                                ).tags.set(tags)
                competition_unique_competition_id_list.append(uuid)
                time.sleep(SLEEP_TIME)
            print('*'*20);print('CREATE COMPETITION');print(competition_unique_competition_id_list);print('*'*20)


            # ユーザ行動の作成
            dummy_discussion_title_list=[]
            dummy_notebook_title_list=[]
            print('\n');print('*'*20);print('USER ACTION')
            for user_unique_account_id in unique_account_id_list:
                user = CustomUser.objects.filter(unique_account_id=user_unique_account_id).first()
                # コンペティションへの参加と行動
                for competition_unique_competition_id in competition_unique_competition_id_list:
                    # 参加(70%)
                    if random.random() > 0.3:
                        competition = Competitions.objects.filter(unique_competition_id=competition_unique_competition_id).first()
                        m1, _ = create_date_random()
                        date_joined = competition.date_open + datetime.timedelta(hours=int(random.random()*m1))
                        JoinCompetitionUsers.objects.create(join_user=user,
                                                            competition=competition,
                                                            date_joined=date_joined,)
                        # Submit(90%)
                        if random.random() > 0.1:
                            Final_Evaluation_select=0
                            for i in range(5):
                                if random.random() > 0.5:
                                    # 最終評価対象の選択
                                    if Final_Evaluation_select == 0:
                                        Final_Evaluation=True
                                    elif random.random() > 0.8:
                                        Final_Evaluation_select += 1
                                        if Final_Evaluation_select >= 3:
                                            Final_Evaluation=False
                                        else:
                                            Final_Evaluation=True
                                    else:
                                        Final_Evaluation=False
                                    # 提出日
                                    m1, _ = create_date_random()
                                    date_submission = date_joined + datetime.timedelta(hours=int(random.random()*m1))

                                    SubmissionUser.objects.create(join_user=user,
                                                                  competition=competition,
                                                                  public_score=random.random(),
                                                                  private_score=random.random(),
                                                                  Final_Evaluation=Final_Evaluation,
                                                                  date_submission=date_submission,)

                        # Discussion(50%)
                        if random.random() > 0.5:
                            for i in range(1):
                                if random.random() > 0.5:
                                    if random.random() > 0.95:
                                        is_top=True
                                    else:
                                        is_top=False
                                    if random.random() > 0.95:
                                        use_bot_icon=True
                                    else:
                                        use_bot_icon=False
                                    uuid=str(uuid4())[:12]
                                    m1, _ = create_date_random()
                                    date_create = date_joined + datetime.timedelta(hours=int(random.random()*m1/10))
                                    tags_list=[]
                                    # 30%の確率でタグが付与され、それぞれ60%の確率で割当が行われる
                                    if random.random() > 0.7:
                                        for i in range(TAGS_N):
                                            if random.random() > 0.6:
                                                tags_list.append(discussion_tags_name_list[i])
                                    tags=DiscussionTags.objects.filter(name__in=tags_list)
                                    DiscussionThemes.objects.create(post_user=user,
                                                                    post_competition_or_none=competition,
                                                                    title=f'ダミーディスカッション_comp_({uuid})',
                                                                    text=dummy_text(short=True),
                                                                    is_top=is_top,
                                                                    use_bot_icon=use_bot_icon,
                                                                    date_create=date_create,
                                                                    ).tags_or_none.set(tags)
                                    dummy_discussion_title_list.append(f'ダミーディスカッション_comp_({uuid})')

                        # Notebook(50%)
                        if not settings.USE_GCS:
                            if random.random() > 0.5:
                                for i in range(1):
                                    if random.random() > 0.5:
                                        if random.random() > 0.95:
                                            is_top=True
                                        else:
                                            is_top=False
                                        if random.random() > 0.95:
                                            use_bot_icon=True
                                        else:
                                            use_bot_icon=False
                                        uuid=str(uuid4())[:12]
                                        m1, _ = create_date_random()
                                        date_create = date_joined + datetime.timedelta(hours=int(random.random()*m1/10))
                                        tags_list=[]
                                        # 30%の確率でタグが付与され、それぞれ60%の確率で割当が行われる
                                        if random.random() > 0.7:
                                            for i in range(TAGS_N):
                                                if random.random() > 0.6:
                                                    tags_list.append(notebook_tags_name_list[i])
                                        tags=NotebookTags.objects.filter(name__in=tags_list)
                                        NotebookThemes.objects.create(post_user=user,
                                                                    post_competition_or_none=competition,
                                                                    title=f'ダミーノートブック_comp_({uuid})',
                                                                    notebook_file=notebook_file_path,
                                                                    is_top=is_top,
                                                                    use_bot_icon=use_bot_icon,
                                                                    date_create=date_create,
                                                                    ).tags_or_none.set(tags)
                                        dummy_notebook_title_list.append(f'ダミーノートブック_comp_({uuid})')

                    time.sleep(SLEEP_TIME)

                # Competitionに紐づかないDiscussion(50%)
                if random.random() > 0.5:
                    for i in range(1):
                        if random.random() > 0.5:
                            if random.random() > 0.95:
                                is_top=True
                            else:
                                is_top=False
                            if random.random() > 0.95:
                                use_bot_icon=True
                            else:
                                use_bot_icon=False
                            uuid=str(uuid4())[:12]
                            m1, _ = create_date_random()
                            date_create = user.date_joined + datetime.timedelta(hours=int(random.random()*m1))
                            tags_list=[]
                            # 30%の確率でタグが付与され、それぞれ60%の確率で割当が行われる
                            if random.random() > 0.7:
                                for i in range(TAGS_N):
                                    if random.random() > 0.6:
                                        tags_list.append(discussion_tags_name_list[i])
                            tags=DiscussionTags.objects.filter(name__in=tags_list)
                            DiscussionThemes.objects.create(post_user=user,
                                                            title=f'ダミーディスカッション_({uuid})',
                                                            text=dummy_text(short=True),
                                                            is_top=is_top,
                                                            use_bot_icon=use_bot_icon,
                                                            date_create=date_create,
                                                            ).tags_or_none.set(tags)
                            dummy_discussion_title_list.append(f'ダミーディスカッション_({uuid})')

                # Competitionに紐づかないNotebook(50%)
                if not settings.USE_GCS:
                    if random.random() > 0.5:
                        for i in range(1):
                            if random.random() > 0.5:
                                if random.random() > 0.95:
                                    is_top=True
                                else:
                                    is_top=False
                                if random.random() > 0.95:
                                    use_bot_icon=True
                                else:
                                    use_bot_icon=False
                                uuid=str(uuid4())[:12]
                                m1, _ = create_date_random()
                                date_create = user.date_joined + datetime.timedelta(hours=int(random.random()*m1))
                                tags_list=[]
                                # 30%の確率でタグが付与され、それぞれ60%の確率で割当が行われる
                                if random.random() > 0.7:
                                    for i in range(TAGS_N):
                                        if random.random() > 0.6:
                                            tags_list.append(notebook_tags_name_list[i])
                                tags=NotebookTags.objects.filter(name__in=tags_list)
                                NotebookThemes.objects.create(post_user=user,
                                                            title=f'ダミーノートブック_({uuid})',
                                                            notebook_file=notebook_file_path,
                                                            is_top=is_top,
                                                            use_bot_icon=use_bot_icon,
                                                            date_create=date_create,
                                                            ).tags_or_none.set(tags)
                                dummy_notebook_title_list.append(f'ダミーノートブック_({uuid})')


            # コメント、ブックマーク、投票
            dummy_comment_text_list=[]
            print('\n');print('*'*20);print('USER ACTION Comment Bookmark Vote')

            for user_unique_account_id in unique_account_id_list:
                user = CustomUser.objects.filter(unique_account_id=user_unique_account_id).first()
                dummy_discussion = DiscussionThemes.objects.filter(title__in=dummy_discussion_title_list)
                if not settings.USE_GCS:
                    dummy_notebook = NotebookThemes.objects.filter(title__in=dummy_notebook_title_list)

                for discussion in dummy_discussion:
                    # コメント
                    for i in range(1):
                        if random.random() > 0.5:
                            uuid=str(uuid4())[:12]
                            m1, _ = create_date_random()
                            date_create=user.date_joined + datetime.timedelta(hours=int(random.random()*m1))
                            Comments.objects.create(post_user=user,
                                                    post_discussion_theme=discussion,
                                                    text=dummy_text(short=True)+uuid,
                                                    date_create=date_create,
                                                    )
                            dummy_comment_text_list.append(dummy_text(short=True)+uuid)
                    # ブックマーク
                    if random.random() > 0.5:
                        DiscussionBookmarks.objects.create(user=user,
                                                           subject=discussion,
                                                           )
                    # 投票
                    if random.random() > 0.5:
                        if random.random() > 0.5:
                            DiscussionVotes.objects.create(user=user,
                                                           subject=discussion,
                                                           votes=1,)
                        else:
                            DiscussionVotes.objects.create(user=user,
                                                           subject=discussion,
                                                           votes=-1,)
                    time.sleep(SLEEP_TIME)

                if not settings.USE_GCS:
                    for notebook in dummy_notebook:
                        # コメント
                        for i in range(1):
                            if random.random() > 0.5:
                                uuid=str(uuid4())[:12]
                                m1, _ = create_date_random()
                                date_create=user.date_joined + datetime.timedelta(hours=int(random.random()*m1))
                                Comments.objects.create(post_user=user,
                                                        post_notebook_theme=notebook,
                                                        text=dummy_text(short=True)+uuid,
                                                        date_create=date_create,
                                                        )
                                dummy_comment_text_list.append(dummy_text(short=True)+uuid)
                        # ブックマーク
                        if random.random() > 0.5:
                            NotebookBookmarks.objects.create(user=user,
                                                            subject=notebook,
                                                            )
                        # 投票
                        if random.random() > 0.5:
                            if random.random() > 0.5:
                                NotebookVotes.objects.create(user=user,
                                                            subject=notebook,
                                                            votes=1,)
                            else:
                                NotebookVotes.objects.create(user=user,
                                                            subject=notebook,
                                                            votes=-1,)
                        time.sleep(SLEEP_TIME)


            # コメントへのブックマークと投票
            print('\n');print('*'*20);print('USER ACTION Bookmark Vote for Comment')
            for user_unique_account_id in unique_account_id_list:
                user = CustomUser.objects.filter(unique_account_id=user_unique_account_id).first()
                dummy_comment = Comments.objects.filter(text__in=dummy_comment_text_list)

                for comment in dummy_comment:
                    # ブックマーク
                    if random.random() > 0.5:
                        CommentBookmarks.objects.create(user=user,
                                                        subject=comment,
                                                        )
                    # 投票
                    if random.random() > 0.5:
                        if random.random() > 0.5:
                            CommentVotes.objects.create(user=user,
                                                        subject=comment,
                                                        votes=1,)
                        else:
                            CommentVotes.objects.create(user=user,
                                                        subject=comment,
                                                        votes=-1,)
                    time.sleep(SLEEP_TIME)
                time.sleep(SLEEP_TIME)

            print('*'*20);print('DONE');print(f"::: ElapsedTime: {time.time() - t_start_1:.0f}s :::");print('*'*20)
            
            messages.add_message(self.request, messages.INFO,
                                 f'ダミーデータ作成完了',)
            messages.add_message(self.request, messages.INFO,
                                 f'ダミーのコンペティションでサブミットするには、当該コンペティションの answer file を再設定してください。',)
            messages.add_message(self.request, messages.INFO,
                                 f'ダミーデータをすべて削除するには、Userを削除した後（紐付つくDiscussion/Notebook/Comment/CompetitionJoin/Submittion/Bookmark/Voteも削除されます）、Competitionデータ、及びCompetition/Discussion/NotebookのTagを削除します',)
            return redirect('management:home')
        else:
            raise Http404