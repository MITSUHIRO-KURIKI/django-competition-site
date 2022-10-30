from competitions.models import (
    Competitions, CompetitionsTags, 
    JoinCompetitionUsers,
)
from submission.models import (
    SubmissionUser,
)
from django.views.generic import (
    ListView, DetailView,
    DeleteView,
)
from common_scripts import (
    get_pagenator_object,
)
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.db.models import (
    Count,
)


# Competition一覧の表示(is_public = True)
class CompetitionsView(ListView):

    model = Competitions
    template_name = 'competitions/CompetitionsList/competitions_list.html'
    context_object_name = "ACTIVE_COMPETITIONS_EXCLUDE_UserJoin"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        paginate_by_num = 6

        # GETリクエストパラメータの取得
        tag=None
        request_tag = self.request.GET.get('tag')
        join_page = self.request.GET.get('join_page')
        close_page = self.request.GET.get('close_page')
        private_page = self.request.GET.get('private_page')

        if request_tag is not None:
            tag = get_object_or_404(CompetitionsTags, name=request_tag)

        if self.request.user.is_anonymous:
            context.update({
                'User_JOINED_COMPETITIONS': None,
            })
        else:
            if tag is not None:
                # コンペティションのうち開催中のものでタグと一致するもの
                competition_data = self.model.objects.filter(date_close__gt = timezone.now(), is_public=True, tags=tag).all()
            else:
                # コンペティションのうち開催中のものすべて
                competition_data = self.model.objects.filter(date_close__gt = timezone.now(), is_public=True).all()
            
            # 参加人数の取得
            competition_data = competition_data.annotate(join_user_count=Count(
                                'related_join_competition_users_competitions__join_user',
                                distinct=True,
                                )
                            )
            # ユーザが参加しているもの
            competition_data = competition_data.filter(related_join_competition_users_competitions__join_user  = self.request.user)
            User_JOINED_COMPETITIONS = get_pagenator_object(competition_data, paginate_by_num, join_page)
            
            context.update({
                'User_JOINED_COMPETITIONS': User_JOINED_COMPETITIONS,
            })
        
        if tag is not None:
            # 終了したコンペティションでタグと一致するもの
            competition_data = self.model.objects.filter(date_close__lte = timezone.now(), is_public=True, tags=tag).all()
        else:
            # 終了したコンペティションすべて
            competition_data = self.model.objects.filter(date_close__lte = timezone.now(), is_public=True).all()

        # 参加人数の取得
        competition_data = competition_data.annotate(join_user_count=Count(
                               'related_join_competition_users_competitions__join_user',
                               distinct=True,
                               )
                           )
        CLOSE_COMPETITIONS_EXCLUDE_UserJoin = get_pagenator_object(competition_data, paginate_by_num, close_page)
        context.update({
            'CLOSE_COMPETITIONS_EXCLUDE_UserJoin': CLOSE_COMPETITIONS_EXCLUDE_UserJoin,
        })

        # ユーザがどのコンペティションにもjoinしていない場合チュートリアル表示
        if self.request.user.is_anonymous:
            IS_TUTORIAL = False
        elif JoinCompetitionUsers.objects.filter(join_user=self.request.user).exists():
            IS_TUTORIAL = False
        else:
            IS_TUTORIAL = True

        # 非公開のコンペティション
        if self.request.user.is_superuser or self.request.user.is_staff:
            competition_data = self.model.objects.filter(is_public=False).all()
            PRIVATE_COMPETITIONS = get_pagenator_object(competition_data, paginate_by_num, private_page)
            context.update({
                'PRIVATE_COMPETITIONS': PRIVATE_COMPETITIONS,
            })
        context.update({
                # チュートリアルの表示
                'IS_TUTORIAL': IS_TUTORIAL,
                # 登録タグ一覧
                'TAGS': CompetitionsTags.objects.all(),
                # Pagination tag
                'use_page_tags': ['tag', 'join_page', 'active_page', 'close_page', 'private_page'],
                # 表示しているタグ名
                'SELECT_TAG': request_tag,
            })
        return context

    def get_queryset(self, **kwargs):

        paginate_by_num = 6

        # GETリクエストパラメータの取得
        tag=None
        request_tag = self.request.GET.get('tag')
        active_page = self.request.GET.get('active_page')
        
        if request_tag is not None:
            tag = get_object_or_404(CompetitionsTags, name=request_tag)
        
        # 開催中のコンペティション
        if self.request.user.is_anonymous:
            # 開催中のコンペティションすべて
            if tag is not None:
                competition_data = self.model.objects.filter(date_close__gt = timezone.now(), tags=tag, is_public=True).all()
            else:
                competition_data = self.model.objects.filter(date_close__gt = timezone.now(), is_public=True).all()
        else:
            # 開催中のコンペティションのうちユーザが参加していないもの
            if tag is not None:
                competition_data = self.model.objects.filter(date_close__gt = timezone.now(), tags=tag, is_public=True).exclude(related_join_competition_users_competitions__join_user = self.request.user).all()
            else:
                competition_data = self.model.objects.filter(date_close__gt = timezone.now(), is_public=True).exclude(related_join_competition_users_competitions__join_user = self.request.user).all()

        # 参加人数の取得
        competition_data = competition_data.annotate(join_user_count=Count(
                               'related_join_competition_users_competitions__join_user',
                               distinct=True,
                               )
                           )
        ACTIVE_COMPETITIONS_EXCLUDE_UserJoin = get_pagenator_object(competition_data, paginate_by_num, active_page)
        return ACTIVE_COMPETITIONS_EXCLUDE_UserJoin


# Competitionページの表示(一般ユーザは is_public = True のみ)
class CompetitionDetailView(ListView):
    model = Competitions
    template_name = 'competitions/CompetitionPage/competition_page.html'
    context_object_name = "COMPETITION_DATA"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        unique_competition_id = self.kwargs['unique_competition_id']

        competition = get_object_or_404(self.model, unique_competition_id=unique_competition_id)

        if self.request.user.is_anonymous:
            IS_USER_COMPETITION_JOINED = False
            context.update({
                    # ユーザ登録状況
                    'IS_USER_COMPETITION_JOINED': IS_USER_COMPETITION_JOINED,
                })
        else:
            if Competitions.objects.filter(unique_competition_id=unique_competition_id, related_join_competition_users_competitions__join_user=self.request.user).exists():
                IS_USER_COMPETITION_JOINED=True
            else:
                IS_USER_COMPETITION_JOINED=False
            context.update({
                    # ユーザ登録状況
                    'IS_USER_COMPETITION_JOINED': IS_USER_COMPETITION_JOINED,
                })

        # コンペに参加している場合としていない場合でINFO_MODALを変化
        if IS_USER_COMPETITION_JOINED:
            IS_INFO_MODAL_FIRST = False
            IS_INFO_MODAL_SECOND = True
        else:
            IS_INFO_MODAL_FIRST = True
            IS_INFO_MODAL_SECOND = False

        # ユーザがどのコンペティションにもjoinしていない場合かつ表示中のコンペティションが開催中の場合チュートリアル表示(IS_INFO_MODAL_FIRST)
        now = timezone.localtime(timezone.now())
        date_close = timezone.localtime(competition.date_close)
        
        if self.request.user.is_anonymous:
            IS_TUTORIAL = False
        elif IS_INFO_MODAL_FIRST:
            if not JoinCompetitionUsers.objects.filter(join_user=self.request.user).exists() and (now < date_close):
                IS_TUTORIAL = True
            else:
                IS_TUTORIAL = False
        
        # 表示中のコンペティションにJOINしていて、表示中のコンペティションが開催中の場合かつどのコンペでもSubmitしていない場合チュートリアル表示(IS_INFO_MODAL_SECOND)
        if self.request.user.is_anonymous:
            IS_TUTORIAL = False
        elif IS_INFO_MODAL_SECOND:
            if IS_USER_COMPETITION_JOINED and (now < date_close) and not SubmissionUser.objects.filter(join_user=self.request.user).exists():
                IS_TUTORIAL = True
            else:
                IS_TUTORIAL = False

        context.update({
                # 表示する Info-Modal の選択
               'IS_INFO_MODAL_FIRST': IS_INFO_MODAL_FIRST,
               'IS_INFO_MODAL_SECOND': IS_INFO_MODAL_SECOND,
                # チュートリアルの表示
                'IS_TUTORIAL': IS_TUTORIAL,
                # 参加ユーザ数
                'User_JOINED_COUNT': self.model.objects.filter(related_join_competition_users_competitions__competition =competition).count(),
                # 現在時刻
                'DATE_NOW': timezone.now(), 
        })
        return context

    def get_queryset(self, **kwargs):

        unique_competition_id = self.kwargs['unique_competition_id']

        # 一般ユーザは is_public = True のみ
        if self.request.user.is_superuser or self.request.user.is_staff:
            COMPETITION_DATA = get_object_or_404(self.model, unique_competition_id=unique_competition_id)
            if not COMPETITION_DATA.is_public:
                messages.add_message(self.request, messages.INFO,
                                    f'このコンペティションは公開されていません。機能が制限されています。',)
        else:
            COMPETITION_DATA = get_object_or_404(self.model, unique_competition_id=unique_competition_id, is_public=True)
        
        now = timezone.localtime(timezone.now())
        date_open = timezone.localtime(COMPETITION_DATA.date_open)
        date_close = timezone.localtime(COMPETITION_DATA.date_close)
        
        open_progress_seconds = int( (now - date_open).total_seconds() )
        close_remain_seconds = int( (date_close - now).total_seconds() )

        if open_progress_seconds < 0:
            messages.add_message(self.request, messages.WARNING,
                                 f'このコンペティションは開催前です',)
        elif 0 < close_remain_seconds < (86400)*2:
            messages.add_message(self.request, messages.WARNING,
                                 f'このコンペティションはまもなく終了します',)
        return COMPETITION_DATA