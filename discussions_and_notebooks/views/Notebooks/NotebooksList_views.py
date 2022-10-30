from django.conf import settings
from discussions_and_notebooks.models import (
    NotebookTags, NotebookThemes,
)
from bookmark.models import(
    NotebookBookmarks,
)
from competitions.models import (
    Competitions,
)
from vote.models import(
    DiscussionVotes, NotebookVotes,
)
from django.views.generic import (
    ListView,
)
from django.views.generic.edit import (
    CreateView,
)
from common_scripts import (
    get_pagenator_object,
)
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db.models import (
    Case, When, Value, IntegerField,
    Max, Count, Sum,
)
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()


# Notebook一覧の表示
class NotebooksView(ListView):

    model = NotebookThemes
    template_name = 'discussions_and_notebooks/notebooks/NotebooksList/notebooks_list.html'
    context_object_name = "NOTEBOOKS_DATA"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # GETリクエストパラメータの取得
        request_tag = self.request.GET.get('tag')
        request_sort = self.request.GET.get('sort')
        if request_sort is None:
            request_sort = 'latest'

        # Bookmark の取得
        if self.request.user.is_anonymous:
            BOOKMARK_NOTEBOOKS_ID_LIST = None
        else:
            BOOKMARK_NOTEBOOKS_ID_LIST = NotebookBookmarks.objects.filter(user=self.request.user).values_list('subject', flat=True)

        context.update({
                # InfoModal(Tagは不要)
                'DiscussionNotebookTags': True,
                # 登録タグ一覧
                'TAGS': NotebookTags.objects.all(),
                # Pagination tag
                'use_page_tags': ['tag','sort','notebooks_page', ],
                # 表示しているタグ名
                'SELECT_TAG': request_tag,
                # 表示しているソート名
                'SELECT_SORT': request_sort,
                # ユーザのブックマークデータ
                'BOOKMARK_NOTEBOOKS_ID_LIST': BOOKMARK_NOTEBOOKS_ID_LIST,
            })
        
        return context

    def get_queryset(self, **kwargs):

        paginate_by_num = 10

        # GETリクエストパラメータの取得
        tag=None
        request_tag = self.request.GET.get('tag')
        request_sort = self.request.GET.get('sort')
        notebooks_page = self.request.GET.get('notebooks_page')

        if request_tag is not None:
            tag = get_object_or_404(NotebookTags, name=request_tag)

        # Competition is_public=True のみ
        data = self.model.objects.filter(
                    Q(post_competition_or_none=None) | 
                    Q(post_competition_or_none__is_public=True)
        )
        
        if tag is not None:
            # タグと一致するNotebooksデータ (CompetitionNotebookはtopにしない)
            data = data.filter(tags_or_none=tag).annotate(general_top=Case(
                            When(is_top=True, post_competition_or_none=None,
                            then=Value(0)),
                            default=Value(1),
                            output_field=IntegerField()
                            ))
        else:
            # Notebooksデータ (CompetitionNotebookはtopにしない)
            data = data.annotate(general_top=Case(
                            When(is_top=True,post_competition_or_none=None,
                            then=Value(0)),
                            default=Value(1),
                            output_field=IntegerField()
                            ))
        
        # コメント数と最終コメント日の取得
        data = data.annotate(
                    latest_comment_date=Max(
                        'related_comments_count_post_notebook_theme__latest_post_date',
                    ),
                    comments_count=Max(
                        'related_comments_count_post_notebook_theme__count',
                    ),
                )
        
        if request_sort is not None:
            if request_sort == 'latest':
                notebooks_data = data.order_by('general_top', '-date_create')
            elif request_sort == 'latest_comments':
                notebooks_data = data.order_by('-latest_comment_date')
            elif request_sort == 'number_ot_comments':
                notebooks_data = data.order_by('-comments_count')
            elif  request_sort == 'number_ot_votes':
                # Vote多い順
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
                notebooks_data = [ data.filter(id=id).first() for id in sort_id ]
            else:
                notebooks_data = data.order_by('general_top', '-date_create')
        else:
            notebooks_data = data.order_by('general_top', '-date_create')

        NOTEBOOKS_DATA = get_pagenator_object(notebooks_data, paginate_by_num, notebooks_page)
            
        return NOTEBOOKS_DATA



# Notebook一覧の表示(General)
class GeneralNotebooksView(ListView):

    model = NotebookThemes
    template_name = 'discussions_and_notebooks/notebooks/NotebooksList/general_notebooks_list.html'
    context_object_name = "NOTEBOOKS_DATA"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # GETリクエストパラメータの取得
        request_tag = self.request.GET.get('tag')
        request_sort = self.request.GET.get('sort')
        if request_sort is None:
            request_sort = 'latest'

        # Bookmark の取得
        if self.request.user.is_anonymous:
            BOOKMARK_NOTEBOOKS_ID_LIST = None
        else:
            BOOKMARK_NOTEBOOKS_ID_LIST = NotebookBookmarks.objects.filter(user=self.request.user).values_list('subject', flat=True)

        context.update({
                # InfoModal(Tagは不要)
                'DiscussionNotebookTags': True,
                # 登録タグ一覧
                'TAGS': NotebookTags.objects.all(),
                # Pagination tag
                'use_page_tags': ['tag','sort','notebooks_page', ],
                # 表示しているタグ名
                'SELECT_TAG': request_tag,
                # 表示しているソート名
                'SELECT_SORT': str(request_sort),
                # ユーザのブックマークデータ
                'BOOKMARK_NOTEBOOKS_ID_LIST': BOOKMARK_NOTEBOOKS_ID_LIST,
            })
        return context

    def get_queryset(self, **kwargs):

        paginate_by_num = 10

        # GETリクエストパラメータの取得
        tag=None
        request_tag = self.request.GET.get('tag')
        request_sort = self.request.GET.get('sort')
        notebooks_page = self.request.GET.get('notebooks_page')

        if request_tag is not None:
            tag = get_object_or_404(NotebookTags, name=request_tag)

        if tag is not None:
            # タグと一致するNotebooksデータ
            data = self.model.objects.filter(post_competition_or_none=None, tags_or_none=tag).all()
        else:
            # Notebooksデータ
            data = self.model.objects.filter(post_competition_or_none=None).all()
        
        # コメント数と最終コメント日の取得
        data = data.annotate(
                    latest_comment_date=Max(
                        'related_comments_count_post_notebook_theme__latest_post_date',
                    ),
                    comments_count=Max(
                        'related_comments_count_post_notebook_theme__count',
                    ),
                )

        if request_sort is not None:
            if request_sort == 'latest':
                notebooks_data = data.order_by('-is_top', '-date_create')
            elif request_sort == 'latest_comments':
                notebooks_data = data.order_by('-latest_comment_date')
            elif request_sort == 'number_ot_comments':
                notebooks_data = data.order_by('-comments_count')
            elif  request_sort == 'number_ot_votes':
                # Vote多い順
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
                notebooks_data = [ data.filter(id=id).first() for id in sort_id ]
            else:
                notebooks_data = data.order_by('-is_top', '-date_create')
        else:
            notebooks_data = data.order_by('-is_top', '-date_create')

        NOTEBOOKS_DATA = get_pagenator_object(notebooks_data, paginate_by_num, notebooks_page)
            
        return NOTEBOOKS_DATA


# Notebook一覧の表示(Competition)
class CompetitionNotebooksView(ListView):

    model = NotebookThemes
    template_name = 'discussions_and_notebooks/notebooks/NotebooksList/competition_notebooks_list.html'
    context_object_name = "NOTEBOOKS_DATA"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        
        # GETリクエストパラメータの取得
        request_tag = self.request.GET.get('tag')
        request_sort = self.request.GET.get('sort')
        if request_sort is None:
            request_sort = 'latest'

        unique_competition_id = self.kwargs['unique_competition_id']
        
        competition = get_object_or_404(Competitions, unique_competition_id=unique_competition_id)

        if self.request.user.is_anonymous:
            context.update({
                    # ユーザ登録状況
                    'IS_USER_COMPETITION_JOINED': False,
                })
        else:
            if Competitions.objects.filter(unique_competition_id=unique_competition_id, related_join_competition_users_competitions__join_user = self.request.user).exists():
                IS_USER_COMPETITION_JOINED=True
            else:
                IS_USER_COMPETITION_JOINED=False
            context.update({
                    # ユーザ登録状況
                    'IS_USER_COMPETITION_JOINED': IS_USER_COMPETITION_JOINED,
                })

        # Bookmark の取得
        if self.request.user.is_anonymous:
            BOOKMARK_NOTEBOOKS_ID_LIST = None
        else:
            BOOKMARK_NOTEBOOKS_ID_LIST = NotebookBookmarks.objects.filter(user=self.request.user).values_list('subject', flat=True)

        context.update({
                # InfoModal(Tagは不要)
                'DiscussionNotebookTags': False,
                # 登録タグ一覧
                'TAGS': NotebookTags.objects.all(),
                # Pagination tag
                'use_page_tags': ['tag','sort','notebooks_page', ],
                # 表示しているタグ名
                'SELECT_TAG': request_tag,
                # 表示しているソート名
                'SELECT_SORT': request_sort,
                # コンペティションデータ
                'COMPETITION_DATA': get_object_or_404(Competitions, unique_competition_id=unique_competition_id),
                # 参加ユーザ数
                'User_JOINED_COUNT': Competitions.objects.filter(related_join_competition_users_competitions__competition=competition).count(),
                # ユーザのブックマークデータ
                'BOOKMARK_NOTEBOOKS_ID_LIST': BOOKMARK_NOTEBOOKS_ID_LIST,
            })

        return context

    def get_queryset(self, **kwargs):

        unique_competition_id = self.kwargs['unique_competition_id']

        if self.request.user.is_superuser or self.request.user.is_staff:
            competition = get_object_or_404(Competitions, unique_competition_id=unique_competition_id)
            if not competition.is_public:
                messages.add_message(self.request, messages.INFO,
                                        f'このコンペティションは公開されていません',)
        else:
            competition = get_object_or_404(Competitions, unique_competition_id=unique_competition_id, is_public=True)

        paginate_by_num = 10

        # GETリクエストパラメータの取得
        tag=None
        request_tag = self.request.GET.get('tag')
        request_sort = self.request.GET.get('sort')
        notebooks_page = self.request.GET.get('notebooks_page')

        if request_tag is not None:
            tag = get_object_or_404(NotebookTags, name=request_tag)
        
        if tag is not None:
            # タグと一致するNotebooksデータ
            data = self.model.objects.filter(post_competition_or_none=competition, tags_or_none=tag).all()
        else:
            # Notebooksデータ
            data = self.model.objects.filter(post_competition_or_none=competition).all()

        # コメント数と最終コメント日の取得
        data = data.annotate(
                    latest_comment_date=Max(
                        'related_comments_count_post_notebook_theme__latest_post_date',
                    ),
                    comments_count=Max(
                        'related_comments_count_post_notebook_theme__count',
                    ),
                )

        if request_sort is not None:
            if request_sort == 'latest':
                notebooks_data = data.order_by('-is_top', '-date_create')
            elif request_sort == 'latest_comments':
                notebooks_data = data.order_by('-latest_comment_date')
            elif request_sort == 'number_ot_comments':
                notebooks_data = data.order_by('-comments_count')
            elif  request_sort == 'number_ot_votes':
                # Vote多い順
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
                notebooks_data = [ data.filter(id=id).first() for id in sort_id ]
            else:
                notebooks_data = data.order_by('-is_top', '-date_create')
        else:
            notebooks_data = data.order_by('-is_top', '-date_create')

        NOTEBOOKS_DATA = get_pagenator_object(notebooks_data, paginate_by_num, notebooks_page)

        return NOTEBOOKS_DATA