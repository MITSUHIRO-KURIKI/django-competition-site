from django.conf import settings
from discussions_and_notebooks.models import (
    NotebookThemes, NotebookThemesMeta,
)
from comments.models import (
    Comments,
)
from bookmark.models import(
    NotebookBookmarks, CommentBookmarks,
)
from vote.models.Vote_models import(
    CommentVotes,
)
from comments.forms import (
    PostCommentForm,
)
from comments.Convert import (
    convert_comment,
)
from django.views.generic import (
    ListView,
)
from django.views.generic.edit import (
    CreateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db.models import (
    Case, When, Value, IntegerField,
    Max, Count, Sum,
)
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import (
    reverse_lazy, reverse,
)
from django.contrib import messages
from django.http import Http404


User = get_user_model()

        
# Notebookページの表示
class NotebookPageView(ListView):

    model = NotebookThemes
    template_name = 'discussions_and_notebooks/notebooks/NotebookPage/notebook_page.html'
    context_object_name = "NOTEBOOK_DATA"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        NOTEBOOK_META_DATA = get_object_or_404(NotebookThemesMeta, object_model__id=self.kwargs['pk'])

        # Bookmark の取得
        if self.request.user.is_anonymous:
            BOOKMARK_NOTEBOOKS_ID_LIST = None
        else:
            BOOKMARK_NOTEBOOKS_ID_LIST = NotebookBookmarks.objects.filter(user=self.request.user).values_list('subject', flat=True)

        context.update({
                'NOTEBOOK_META_DATA': NOTEBOOK_META_DATA,
                # ユーザのブックマークデータ
                'BOOKMARK_NOTEBOOKS_ID_LIST': BOOKMARK_NOTEBOOKS_ID_LIST,
            })

        return context

    def get_queryset(self, **kwargs):

        NOTEBOOK_DATA = self.model.objects.filter(id=self.kwargs['pk'])

        if len(NOTEBOOK_DATA) == 0:
            messages.add_message(self.request, messages.INFO,
                                 f'このNotebookは紐づくコンペティションが公開されていません',)
            raise Http404

        # Competition is_public=True のみ
        NOTEBOOK_DATA = NOTEBOOK_DATA.filter(
                            Q(post_competition_or_none=None) | 
                            Q(post_competition_or_none__is_public=True)
        ).distinct()

        if len(list(NOTEBOOK_DATA)) > 0:
            NOTEBOOK_DATA = NOTEBOOK_DATA.annotate(comments_count=Max(
                                    'related_comments_count_post_notebook_theme__count',
                                    ),
                            )
            return NOTEBOOK_DATA
        else:
            NOTEBOOK_DATA = self.model.objects.filter(id=self.kwargs['pk'])
            NOTEBOOK_DATA = NOTEBOOK_DATA.annotate(comments_count=Max(
                                    'related_comments_count_post_notebook_theme__count',
                                    ),
                            )
            messages.add_message(self.request, messages.INFO,
                                 f'このNotebookは紐づくコンペティションが公開されていません',)
            return NOTEBOOK_DATA


class NotebookFileDataView(ListView):

    model = NotebookThemes
    template_name = 'discussions_and_notebooks/notebooks/NotebookPage/notebook_data.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        NOTEBOOK_DATA = NotebookThemes.objects.filter(id=self.kwargs['pk'])

        if len(NOTEBOOK_DATA) == 0:
            raise Http404
        
        # Competition is_public=True のみ
        NOTEBOOK_DATA = NOTEBOOK_DATA.filter(
                            Q(post_competition_or_none=None) | 
                            Q(post_competition_or_none__is_public=True)
        ).distinct()

        if len(list(NOTEBOOK_DATA)) > 0:
            NOTEBOOK_DATA = NOTEBOOK_DATA.annotate(
                                comments_count=Max('related_comments_count_post_notebook_theme__count',
                                ),
                                join_user_count=Count('post_competition_or_none__related_join_competition_users_competitions__join_user',
                                distinct=True,
                                ),
                            )
        else:
            NOTEBOOK_DATA = NotebookThemes.objects.filter(id=self.kwargs['pk'])
            NOTEBOOK_DATA = NOTEBOOK_DATA.annotate(
                                comments_count=Max('related_comments_count_post_notebook_theme__count',
                                ),
                                join_user_count=Count('post_competition_or_none__related_join_competition_users_competitions__join_user',
                                distinct=True,
                                ),
                            )
            messages.add_message(self.request, messages.INFO,
                                 f'このNotebookは紐づくコンペティションが公開されていません',)

        # Bookmark の取得
        if self.request.user.is_anonymous:
            BOOKMARK_NOTEBOOKS_ID_LIST = None
        else:
            BOOKMARK_NOTEBOOKS_ID_LIST = NotebookBookmarks.objects.filter(user=self.request.user).values_list('subject', flat=True)

        context.update({
                # ノートブックデータ
                'NOTEBOOK_DATA': NOTEBOOK_DATA,
                # ユーザのブックマークデータ
                'BOOKMARK_NOTEBOOKS_ID_LIST': BOOKMARK_NOTEBOOKS_ID_LIST,
            })
        return context


# コメント一覧表示と投稿(ここはログインしていなくても見れるようにしておく)
class NotebookCommentsAndPostCommentView(CreateView):

    model = Comments
    template_name = 'discussions_and_notebooks/notebooks/NotebookPage/notebook_comments.html'
    form_class =  PostCommentForm

    def form_valid(self, form):

        if self.request.user.is_anonymous:
            messages.add_message(self.request, messages.WARNING,
                                f'must be logged in to post comments',)
            return super().form_invalid(form)
        else:
            form.instance.post_user = self.request.user

            # convert text for mention
            convert_text = convert_comment(form.instance.text)
            form.instance.text = convert_text

            post_notebook_theme = get_object_or_404(NotebookThemes, id=self.kwargs['pk'])
            if post_notebook_theme is None:
                form.instance.post_notebook_theme=None
            else:
                form.instance.post_notebook_theme=post_notebook_theme
            
            form.instance.post_discussion_theme=None

            messages.add_message(self.request, messages.INFO,
                                f'POSTED!',)
            return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        NOTEBOOK_DATA = NotebookThemes.objects.filter(id=self.kwargs['pk'])

        if len(NOTEBOOK_DATA) == 0:
            raise Http404

        # Competition is_public=True のみ
        NOTEBOOK_DATA = NOTEBOOK_DATA.filter(
                            Q(post_competition_or_none=None) | 
                            Q(post_competition_or_none__is_public=True)
        ).distinct()

        if len(list(NOTEBOOK_DATA)) > 0:
            NOTEBOOK_DATA = NOTEBOOK_DATA.annotate(comments_count=Max(
                                    'related_comments_count_post_notebook_theme__count',
                                    ),
                            )
        else:
            NOTEBOOK_DATA = NotebookThemes.objects.filter(id=self.kwargs['pk'])
            NOTEBOOK_DATA = NOTEBOOK_DATA.annotate(comments_count=Max(
                                    'related_comments_count_post_notebook_theme__count',
                                    ),
                            )
            messages.add_message(self.request, messages.INFO,
                                 f'このNotebookは紐づくコンペティションが公開されていません',)
        # Comment
        # GETリクエストパラメータの取得
        request_sort = self.request.GET.get('sort')
        if request_sort is None:
            request_sort = 'oldest'
        
        comments_data = Comments.objects.filter(post_notebook_theme__id=self.kwargs['pk'])
        
        if request_sort is not None:
            if request_sort == 'oldest':
                COMMTNTS_DATA = comments_data.order_by('date_create')
            elif request_sort == 'latest':
                COMMTNTS_DATA = comments_data.order_by('-date_create')
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
                COMMTNTS_DATA = [ comments_data.filter(id=id).first() for id in sort_id ]
            else:
                COMMTNTS_DATA = comments_data.order_by('date_create')
        else:
            COMMTNTS_DATA = comments_data.order_by('date_create')

        # summernote
        summernote_add_js = settings.SUMMERNOTE_CONFIG['js']
        summernote_add_css = settings.SUMMERNOTE_CONFIG['css']

        ALL_USER_NAME_LIST = list(User.objects.filter(is_active=True).values_list('username', flat=True))

        # Bookmark の取得
        if self.request.user.is_anonymous:
            BOOKMARK_NOTEBOOKS_ID_LIST = None
            BOOKMARK_COMMENT_ID_LIST = None
        else:
            BOOKMARK_NOTEBOOKS_ID_LIST = NotebookBookmarks.objects.filter(user=self.request.user).values_list('subject', flat=True)
            BOOKMARK_COMMENT_ID_LIST = CommentBookmarks.objects.filter(user=self.request.user).values_list('subject', flat=True)

        context.update({
                # ノートブックデータ
                'NOTEBOOK_DATA': NOTEBOOK_DATA,
                # コメント一覧
                'COMMTNTS_DATA': COMMTNTS_DATA,
                # 表示しているソート名
                'SELECT_SORT': str(request_sort),
                # Pagination tag
                'use_page_tags': ['sort',],
                # summernote_add_js and summernote_add_css
                'summernote_add_js': list(summernote_add_js),
                'summernote_add_css': list(summernote_add_css),
                # ALL_USER_NAME_LIST for mention
                'ALL_USER_NAME_LIST': ALL_USER_NAME_LIST,
                # ユーザのブックマークデータ
                'BOOKMARK_NOTEBOOKS_ID_LIST': BOOKMARK_NOTEBOOKS_ID_LIST,
                'BOOKMARK_COMMENT_ID_LIST': BOOKMARK_COMMENT_ID_LIST,
        })
        return context

    def get_success_url(self):
        return reverse_lazy('notebooks:notebook_page_comments', kwargs={'pk' : self.kwargs['pk']})