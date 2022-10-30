from extra_views import (
    InlineFormSetFactory, UpdateWithInlinesView,
)
from django.views.generic import (
    ListView,
)
from accounts.forms import (
    AccountIdUpdateWithInlinesForm,
)
from user_profile.models import (
    CustomUserProfile, 
)
from user_settings.models import (
    CustomUserProfilePublicSettings, 
)
from competitions.models import (
    Competitions, JoinCompetitionUsers,
)
from submission.models import (
    SubmissionUser,
)
from discussions_and_notebooks.models import (
    NotebookThemes, DiscussionThemes,
)
from comments.models import (
    Comments,
)
from vote.models import(
    DiscussionVotes, NotebookVotes, CommentVotes,
)
from bookmark.models import(
    DiscussionBookmarks, NotebookBookmarks, CommentBookmarks,
)
from common_scripts import (
    get_pagenator_object,
)
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q
from django.db.models import (
    Case, When, Value, IntegerField,
    Min, Max, Count, Sum,
)


User = get_user_model()

# ユーザ登録情報の編集 (MultiFormView)
class UserProfileUpdateInline(InlineFormSetFactory):

    model = CustomUserProfile
    fields = ['user_icon',
              'comment',
              'locate',
              'birth_day',
              'gender',
              'sns_id_twitter',
              'sns_id_facebook',
              'sns_id_instagram',
              'sns_id_linkedin',
              'sns_id_github',
              'sns_id_kaggle',
              ]
    factory_kwargs = {
        'can_delete': False,
    }

class AccountId_UserProfile_UpDataView(LoginRequiredMixin, UpdateWithInlinesView):

    model = User
    form_class = AccountIdUpdateWithInlinesForm
    inlines = [ UserProfileUpdateInline, ]
    template_name = 'user_profile/UserProfileEdit/user_profile_edit.html'
    success_url = reverse_lazy('accounts:user_profile:user_profile_edit')

    def get_object(self):
        return self.model.objects.get(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'custom_user': get_object_or_404(self.model, id=self.request.user.id),
            'custom_user_profile': get_object_or_404(CustomUserProfile, user_id__id=self.request.user.id),
            'FRONTEND_URL': settings.FRONTEND_URL,
        })
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO,
                             f'Change DONE',
                             )
        return super().form_valid(form)


# ユーザ登録情報の表示
class UserProfileView(ListView):

    model = User
    template_name = 'user_profile/UserProfile/user_profile.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        paginate_by_num_competition = 6
        paginate_by_num_list = 10


        # GETリクエストパラメータの取得
        active_competition_page = self.request.GET.get('active_competition_page')
        close_competition_page = self.request.GET.get('close_competition_page')
        discussions_page = self.request.GET.get('discussions_page')
        notebooks_page = self.request.GET.get('notebooks_page')
        comments_page = self.request.GET.get('comments_page')
        activate_page = self.request.GET.get('activate_page')
        request_sort = self.request.GET.get('sort')
        if request_sort is None:
            request_sort = 'latest'

        unique_account_id = self.kwargs['unique_account_id']

        ###############
        # Competitions
        ###############

        # コンペティションのうち開催中のもの
        competition_data = Competitions.objects.filter(date_close__gt = timezone.now(), is_public=True).all()
        # 参加人数の取得
        competition_data = competition_data.annotate(join_user_count=Count(
                            'related_join_competition_users_competitions__join_user',
                            # distinct=True,
                            )
                        )
        # ユーザが参加しているもの
        competition_data = competition_data.filter(related_join_competition_users_competitions__join_user__unique_account_id=unique_account_id)
        
        User_JOINED_ACTIVE_COMPETITIONS = get_pagenator_object(competition_data, paginate_by_num_competition, active_competition_page)

        # コンペティションのうち終了したもの
        competition_data = Competitions.objects.filter(date_close__lte = timezone.now(), is_public=True).all()
        # 参加人数の取得
        competition_data = competition_data.annotate(join_user_count=Count(
                            'related_join_competition_users_competitions__join_user',
                                distinct=True,
                            )
                        )
        # ユーザが参加しているもの
        competition_data = competition_data.filter(related_join_competition_users_competitions__join_user__unique_account_id=unique_account_id)
        
        User_JOINED_CLOSE_COMPETITIONS = get_pagenator_object(competition_data, paginate_by_num_competition, close_competition_page)

        context.update({
            'custom_user_profile': get_object_or_404(CustomUserProfile, user_id__unique_account_id=unique_account_id, user_id__is_active=True),
            'custom_user_profile_public_settings': get_object_or_404(CustomUserProfilePublicSettings, user_id__unique_account_id=unique_account_id, user_id__is_active=True),
            'User_JOINED_ACTIVE_COMPETITIONS': User_JOINED_ACTIVE_COMPETITIONS,
            'User_JOINED_CLOSE_COMPETITIONS': User_JOINED_CLOSE_COMPETITIONS,
            # Pagination tag
            'use_page_tags': ['active_competition_page','close_competition_page',
                              'discussions_page','notebooks_page','comments_page',
                              'activate_page','sort',],
            'activate_page': activate_page,
        })


        # 参加コンペティションの順位を取得
        User_Competitions_Rank = user_competitions_rank(unique_account_id)
        context.update({
            'User_Competitions_Rank': User_Competitions_Rank,
        })


        ###############
        # Discussion
        ###############

        # Competition is_public=True のみ
        discussion_data = DiscussionThemes.objects.filter(
                                        Q(post_competition_or_none=None) | 
                                        Q(post_competition_or_none__is_public=True)
                          ).distinct()
        
        # Notebooksデータ (CompetitionNotebookはtopにしない)
        discussion_data = discussion_data.annotate(general_top=Case(
                                        When(is_top=True,post_competition_or_none=None,
                                        then=Value(0)),
                                        default=Value(1),
                                        output_field=IntegerField()
                          ))
        
        # コメント数と最終コメント日の取得
        discussion_data = discussion_data.annotate(
                                        latest_comment_date=Max(
                                        'related_comments_count_post_discussion_theme__latest_post_date',
                                        ),
                                        comments_count=Max(
                                        'related_comments_count_post_discussion_theme__count',
                                        ),
                           )

        if request_sort is not None:
            if request_sort == 'latest':
                discussion_data_sort = discussion_data.order_by('-date_create')
            elif request_sort == 'latest_comments':
                discussion_data_sort = discussion_data.order_by('-latest_comment_date')
            elif request_sort == 'number_ot_comments':
                discussion_data_sort = discussion_data.order_by('-comments_count')
            elif request_sort == 'number_ot_votes':
                # Vote多い順
                # UserPageは他と処理が異なるので注意
                discussion_data_ = discussion_data.filter(post_user__unique_account_id=unique_account_id).exclude(use_bot_icon=True)
                sort_id=[]
                discussion_id_list = [ id for id in discussion_data_.values_list('id', flat=True) ]
                votes_sum_more_than_zero_list = list(DiscussionVotes.objects.filter(subject__in=discussion_data_).select_related().values('subject').annotate(votes_sum=Sum('votes')).filter(votes_sum__gt=0).order_by('-votes_sum').values_list('subject', flat=True))
                votes_sum_below_zero_list = list(DiscussionVotes.objects.filter(subject__in=discussion_data_).select_related().values('subject').annotate(votes_sum=Sum('votes')).filter(votes_sum__lte=0).order_by('-votes_sum').values_list('subject', flat=True))
                for id_ in votes_sum_more_than_zero_list:
                    sort_id.append(id_)
                for id_ in list(set(discussion_id_list)-set(votes_sum_more_than_zero_list)-set(votes_sum_below_zero_list)):
                    sort_id.append(id_)
                for id_ in votes_sum_below_zero_list:
                    sort_id.append(id_)
                discussion_data_sort_ = [ discussion_data_.filter(id=id).first() for id in sort_id ]
            else:
                discussion_data_sort = discussion_data.order_by('-date_create')
        else:
            discussion_data_sort = discussion_data.order_by('-date_create')
        
        # user 絞り込み(use_bot_icon = False)
        if request_sort != 'number_ot_votes':
            discussion_data_sort_ = discussion_data_sort.filter(post_user__unique_account_id=unique_account_id).exclude(use_bot_icon=True)
        DISCUSSIONS_DATA = get_pagenator_object(discussion_data_sort_, paginate_by_num_list, discussions_page)

        context.update({
            'DISCUSSIONS_DATA': DISCUSSIONS_DATA,
        })

        ###############
        # Notebook
        ###############

        # Competition is_public=True のみ
        notebook_data = NotebookThemes.objects.filter(
                                    Q(post_competition_or_none=None) | 
                                    Q(post_competition_or_none__is_public=True)
                        ).distinct()
        
        # Notebooksデータ (CompetitionNotebookはtopにしない)
        notebook_data = notebook_data.annotate(general_top=Case(
                                    When(is_top=True,post_competition_or_none=None,
                                    then=Value(0)),
                                    default=Value(1),
                                    output_field=IntegerField()
                        ))
        
        # コメント数と最終コメント日の取得
        notebook_data = notebook_data.annotate(
                                    latest_comment_date=Max(
                                    'related_comments_post_notebook_theme__date_create',
                                    ),
                                    comments_count=Max(
                                    'related_comments_count_post_notebook_theme__count',
                                    ),
                        )

        if request_sort is not None:
            if request_sort == 'latest':
                notebook_data_sote = notebook_data.order_by('-date_create')
            elif request_sort == 'latest_comments':
                notebook_data_sote = notebook_data.order_by('-latest_comment_date')
            elif request_sort == 'number_ot_comments':
                notebook_data_sote = notebook_data.order_by('-comments_count')
            elif request_sort == 'number_ot_votes':
                # Vote多い順
                # UserPageは他と処理が異なるので注意
                notebook_data_ = notebook_data.filter(post_user__unique_account_id=unique_account_id).exclude(use_bot_icon=True)
                sort_id=[]
                notebook_id_list = [ id for id in notebook_data_.values_list('id', flat=True) ]
                votes_sum_more_than_zero_list = list(NotebookVotes.objects.filter(subject__in=notebook_data_).select_related().values('subject').annotate(votes_sum=Sum('votes')).filter(votes_sum__gt=0).order_by('-votes_sum').values_list('subject', flat=True))
                votes_sum_below_zero_list = list(NotebookVotes.objects.filter(subject__in=notebook_data_).select_related().values('subject').annotate(votes_sum=Sum('votes')).filter(votes_sum__lte=0).order_by('-votes_sum').values_list('subject', flat=True))
                for id_ in votes_sum_more_than_zero_list:
                    sort_id.append(id_)
                for id_ in list(set(notebook_id_list)-set(votes_sum_more_than_zero_list)-set(votes_sum_below_zero_list)):
                    sort_id.append(id_)
                for id_ in votes_sum_below_zero_list:
                    sort_id.append(id_)
                notebook_data_sote_ = [ notebook_data_.filter(id=id).first() for id in sort_id ]
            else:
                notebook_data_sote = notebook_data.order_by('-date_create')
        else:
            notebook_data_sote = notebook_data.order_by('-date_create')
        
        # user 絞り込み(use_bot_icon = False)
        if request_sort != 'number_ot_votes':
            notebook_data_sote_ = notebook_data_sote.filter(post_user__unique_account_id=unique_account_id).exclude(use_bot_icon=True)
        NOTEBOOKS_DATA = get_pagenator_object(notebook_data_sote_, paginate_by_num_list, notebooks_page)

        context.update({
            'NOTEBOOKS_DATA': NOTEBOOKS_DATA,
        })


        ###############
        # Comment
        ###############
        comments_data = Comments.objects.filter(post_user__unique_account_id=unique_account_id)
        
        if request_sort is not None:
            if request_sort == 'oldest':
                comments_data = comments_data.order_by('date_create')
            elif request_sort == 'latest':
                comments_data = comments_data.order_by('-date_create')
            elif  request_sort == 'number_ot_votes':
                # Vote多い順
                sort_id=[]
                comment_id_list = [ id for id in comments_data.values_list('id', flat=True) ]
                votes_sum_more_than_zero_list = list(CommentVotes.objects.filter(subject__in=comments_data).select_related().values('subject').annotate(votes_sum=Sum('votes')).filter(votes_sum__gt=0).order_by('-votes_sum').values_list('subject', flat=True))
                votes_sum_below_zero_list = list(CommentVotes.objects.filter(subject__in=comments_data).select_related().values('subject').annotate(votes_sum=Sum('votes')).filter(votes_sum__lte=0).order_by('-votes_sum').values_list('subject', flat=True))
                for id_ in votes_sum_more_than_zero_list:
                    sort_id.append(id_)
                for id_ in list(set(comment_id_list)-set(votes_sum_more_than_zero_list)-set(votes_sum_below_zero_list)):
                    sort_id.append(id_)
                for id_ in votes_sum_below_zero_list:
                    sort_id.append(id_)
                comments_data = [ comments_data.filter(id=id).first() for id in sort_id ]
            else:
                comments_data = comments_data.order_by('-date_create')
        else:
            comments_data = comments_data.order_by('-date_create')
        
        COMMTNTS_DATA = get_pagenator_object(comments_data, paginate_by_num_list, comments_page)

        context.update({
            'COMMTNTS_DATA': COMMTNTS_DATA,
        })

        ###############
        # Bookmark
        ###############
        # Bookmark の取得(閲覧者)
        if self.request.user.is_anonymous:
            BOOKMARK_DISCUSSIONS_ID_LIST = None
            BOOKMARK_NOTEBOOKS_ID_LIST = None
            BOOKMARK_COMMENT_ID_LIST = None
        else:
            BOOKMARK_DISCUSSIONS_ID_LIST = DiscussionBookmarks.objects.filter(user=self.request.user).values_list('subject', flat=True)
            BOOKMARK_NOTEBOOKS_ID_LIST = NotebookBookmarks.objects.filter(user=self.request.user).values_list('subject', flat=True)
            BOOKMARK_COMMENT_ID_LIST = CommentBookmarks.objects.filter(user=self.request.user).values_list('subject', flat=True)

        # Bookmark の取得(表示ユーザ)
        ###############
        # Discussion
        ###############
        discussions_id = DiscussionBookmarks.objects.filter(user__unique_account_id=unique_account_id).values_list('subject', flat=True)
        if request_sort == 'number_ot_votes':
            # Vote多い順
            # UserPageは他と処理が異なるので注意
            data = discussion_data.filter(id__in=discussions_id)
            sort_id=[]
            discussion_id_list = [ id for id in data.values_list('id', flat=True) ]
            votes_sum_more_than_zero_list = list(DiscussionVotes.objects.filter(subject__in=data).select_related().values('subject').annotate(votes_sum=Sum('votes')).filter(votes_sum__gt=0).order_by('-votes_sum').values_list('subject', flat=True))
            votes_sum_below_zero_list = list(DiscussionVotes.objects.filter(subject__in=data).select_related().values('subject').annotate(votes_sum=Sum('votes')).filter(votes_sum__lte=0).order_by('-votes_sum').values_list('subject', flat=True))
            for id_ in votes_sum_more_than_zero_list:
                sort_id.append(id_)
            for id_ in list(set(discussion_id_list)-set(votes_sum_more_than_zero_list)-set(votes_sum_below_zero_list)):
                sort_id.append(id_)
            for id_ in votes_sum_below_zero_list:
                sort_id.append(id_)
            bookmark_discussionks_data = [ data.filter(id=id).first() for id in sort_id ]
        else:
            bookmark_discussionks_data = discussion_data_sort.filter(id__in=discussions_id)
        USER_BOOKMARKS_DISCUSSION_DATA = get_pagenator_object(bookmark_discussionks_data, paginate_by_num_list, discussions_page)


        ###############
        # Notebook
        ###############
        notebooks_id = NotebookBookmarks.objects.filter(user__unique_account_id=unique_account_id).values_list('subject', flat=True)
        if request_sort == 'number_ot_votes':
            # Vote多い順
            # UserPageは他と処理が異なるので注意
            data = notebook_data.filter(id__in=notebooks_id)
            sort_id=[]
            notebook_id_list = [ id for id in data.values_list('id', flat=True) ]
            votes_sum_more_than_zero_list = list(NotebookVotes.objects.filter(subject__in=data).select_related().values('subject').annotate(votes_sum=Sum('votes')).filter(votes_sum__gt=0).order_by('-votes_sum').values_list('subject', flat=True))
            votes_sum_below_zero_list = list(NotebookVotes.objects.filter(subject__in=data).select_related().values('subject').annotate(votes_sum=Sum('votes')).filter(votes_sum__lte=0).order_by('-votes_sum').values_list('subject', flat=True))
            for id_ in votes_sum_more_than_zero_list:
                sort_id.append(id_)
            for id_ in list(set(notebook_id_list)-set(votes_sum_more_than_zero_list)-set(votes_sum_below_zero_list)):
                sort_id.append(id_)
            for id_ in votes_sum_below_zero_list:
                sort_id.append(id_)
            bookmark_notebooks_data = [ data.filter(id=id).first() for id in sort_id ]
        else:
            bookmark_notebooks_data = notebook_data_sote.filter(id__in=notebooks_id)
        USER_BOOKMARKS_NOTEBOOK_DATA = get_pagenator_object(bookmark_notebooks_data, paginate_by_num_list, notebooks_page)
        
        ###############
        # Comment
        ###############
        comments_id = CommentBookmarks.objects.filter(user__unique_account_id=unique_account_id).values_list('subject', flat=True)
        bookmark_comments_data = Comments.objects.filter(id__in=comments_id)

        if request_sort is not None:
            if request_sort == 'oldest':
                comments_data = bookmark_comments_data.order_by('date_create')
            elif request_sort == 'latest':
                comments_data = bookmark_comments_data.order_by('-date_create')
            elif  request_sort == 'number_ot_votes':
                # Vote多い順
                sort_id=[]
                comment_id_list = [ id for id in bookmark_comments_data.values_list('id', flat=True) ]
                votes_sum_more_than_zero_list = list(CommentVotes.objects.filter(subject__in=bookmark_comments_data).select_related().values('subject').annotate(votes_sum=Sum('votes')).filter(votes_sum__gt=0).order_by('-votes_sum').values_list('subject', flat=True))
                votes_sum_below_zero_list = list(CommentVotes.objects.filter(subject__in=bookmark_comments_data).select_related().values('subject').annotate(votes_sum=Sum('votes')).filter(votes_sum__lte=0).order_by('-votes_sum').values_list('subject', flat=True))
                for id_ in votes_sum_more_than_zero_list:
                    sort_id.append(id_)
                for id_ in list(set(comment_id_list)-set(votes_sum_more_than_zero_list)-set(votes_sum_below_zero_list)):
                    sort_id.append(id_)
                for id_ in votes_sum_below_zero_list:
                    sort_id.append(id_)
                comments_data = [ bookmark_comments_data.filter(id=id).first() for id in sort_id ]
            else:
                comments_data = bookmark_comments_data.order_by('-date_create')
        else:
            comments_data = bookmark_comments_data.order_by('-date_create')
        
        USER_BOOKMARKS_COMMENT_DATA = get_pagenator_object(comments_data, paginate_by_num_list, comments_page)

        context.update({
                # ブックマークデータ(閲覧者)
                'BOOKMARK_DISCUSSIONS_ID_LIST': BOOKMARK_DISCUSSIONS_ID_LIST,
                'BOOKMARK_NOTEBOOKS_ID_LIST': BOOKMARK_NOTEBOOKS_ID_LIST,
                'BOOKMARK_COMMENT_ID_LIST': BOOKMARK_COMMENT_ID_LIST,
                # ブックマークデータ(表示ユーザ)
                'USER_BOOKMARKS_DISCUSSION_DATA': USER_BOOKMARKS_DISCUSSION_DATA,
                'USER_BOOKMARKS_NOTEBOOK_DATA': USER_BOOKMARKS_NOTEBOOK_DATA,
                'USER_BOOKMARKS_COMMENT_DATA': USER_BOOKMARKS_COMMENT_DATA,
        })


        context.update({
            # 表示しているソート名
            'SELECT_SORT': str(request_sort),
        })

        return context

    def get_queryset(self):
        return self.model.objects.get(unique_account_id=self.kwargs['unique_account_id'], is_active=True)



def user_competitions_rank(unique_account_id):

    User_Competitions_Rank={}

    join_unique_competition_ids = JoinCompetitionUsers.objects.filter(join_user__unique_account_id=unique_account_id, competition__is_public=True).values_list('competition__unique_competition_id', flat=True).order_by('competition__unique_competition_id').distinct()
    
    # 参加コンペティションごとに順位を算出
    for join_unique_competition_id in join_unique_competition_ids:
        competition = get_object_or_404(Competitions, unique_competition_id=join_unique_competition_id)
        date_close = competition.date_close
        competition_title = competition.title
        Evaluation_Minimize = competition.Evaluation_Minimize
        join_user = JoinCompetitionUsers.objects.filter(competition__unique_competition_id=join_unique_competition_id).values('join_user')
        

        ####################
        # パブリックスコア
        ####################
        public_score_list=[]

        # 評価指標で上位とする条件（最小値、最大値）
        if Evaluation_Minimize:
            # ベストスコアの取得
            qs = SubmissionUser.objects.filter(competition=competition, date_submission__lte=date_close, join_user__in=join_user).exclude(public_score=None).select_related().values('join_user__unique_account_id').annotate(score=Min('public_score')).order_by('score').values(*['join_user__unique_account_id','score'])
            for q in qs:
                # ベストスコアを持つ submit を特定 (提出日でソートするため)
                best_submit_data = SubmissionUser.objects.filter(competition=competition, date_submission__lte=date_close, join_user__unique_account_id=q['join_user__unique_account_id'], public_score=q['score']).order_by('date_submission').first()
                public_score_list.append({ 'unique_account_id': q['join_user__unique_account_id'],
                                            'score': q['score'],
                                            'date_submission':best_submit_data.date_submission })
            public_score_list = sorted(public_score_list, key=lambda x: (x['score'], x['date_submission']))
        else:
            # ベストスコアの取得
            qs = SubmissionUser.objects.filter(competition=competition, date_submission__lte=date_close, join_user__in=join_user).exclude(public_score=None).select_related().values('join_user__unique_account_id').annotate(score=Max('public_score')).order_by('-score').values(*['join_user__unique_account_id','score'])
            for q in qs:
                # ベストスコアを持つ submit を特定 (提出日でソートするため)
                best_submit_data = SubmissionUser.objects.filter(competition=competition, date_submission__lte=date_close, join_user__unique_account_id=q['join_user__unique_account_id'], public_score=q['score']).order_by('date_submission').first()
                public_score_list.append({ 'unique_account_id': q['join_user__unique_account_id'],
                                            'score': q['score'],
                                            'date_submission':best_submit_data.date_submission })
            # 最大化の場合にはソートを降順
            public_score_list = sorted(public_score_list, key=lambda x: (x['score']*-1, x['date_submission']))

        # 参加ユーザのうちユーザの順位を算定
        public_score_rank=1
        for public_score_list_ in public_score_list:
            if public_score_list_['unique_account_id'] == unique_account_id:
                break
            else:
                public_score_rank += 1
        
        # 提出していない、参加ユーザがいない場合の処理
        if public_score_rank > len(public_score_list):
            public_score_rank=None


        ####################
        # プライベートスコア
        ####################
        # コンペ終了後に表示
        if date_close > timezone.now():
            private_score_rank=None
        else:
            private_score_list=[]

            # 評価指標で上位とする条件（最小値、最大値）
            if Evaluation_Minimize:
                # 最終提出物の中からベストスコアの取得
                qs = SubmissionUser.objects.filter(competition=competition, date_submission__lte=date_close, join_user__in=join_user, Final_Evaluation=True).exclude(private_score=None).select_related().values('join_user__unique_account_id').annotate(score=Min('private_score')).order_by('score').values(*['join_user__unique_account_id','score'])
                for q in qs:
                    # ベストスコアを持つ submit を特定 (提出日でソートするため)
                    best_submit_data = SubmissionUser.objects.filter(competition=competition, date_submission__lte=date_close, join_user__unique_account_id=q['join_user__unique_account_id'], private_score=q['score']).order_by('date_submission').first()
                    private_score_list.append({ 'unique_account_id': q['join_user__unique_account_id'],
                                                'score': q['score'],
                                                'date_submission':best_submit_data.date_submission })
                private_score_list = sorted(private_score_list, key=lambda x: (x['score'], x['date_submission']))
            else:
                # 最終提出物の中からベストスコアの取得
                qs = SubmissionUser.objects.filter(competition=competition, date_submission__lte=date_close, join_user__in=join_user, Final_Evaluation=True).exclude(private_score=None).select_related().values('join_user__unique_account_id').annotate(score=Max('private_score')).order_by('-score').values(*['join_user__unique_account_id','score'])
                for q in qs:
                    # ベストスコアを持つ submit を特定 (提出日でソートするため)
                    best_submit_data = SubmissionUser.objects.filter(competition=competition, date_submission__lte=date_close, join_user__unique_account_id=q['join_user__unique_account_id'], private_score=q['score']).order_by('date_submission').first()
                    private_score_list.append({ 'unique_account_id': q['join_user__unique_account_id'],
                                                'score': q['score'],
                                                'date_submission':best_submit_data.date_submission })
                # 最大化の場合にはソートを降順
                private_score_list = sorted(private_score_list, key=lambda x: (x['score']*-1, x['date_submission']))

            # 参加ユーザのうちユーザの順位を算定
            private_score_rank=1
            for private_score_list_ in private_score_list:
                if private_score_list_['unique_account_id'] == unique_account_id:
                    break
                else:
                    private_score_rank += 1
            
            # 提出していない、参加ユーザがいない場合の処理
            if private_score_rank > len(private_score_list):
                private_score_rank=None


        User_Competitions_Rank[f'{join_unique_competition_id}']=[competition_title, public_score_rank, private_score_rank]
    
    return User_Competitions_Rank