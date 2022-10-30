from django.conf import settings
from user_inquiry.models import (
    UserInquiry,
)
from discussions_and_notebooks.models import (
    DiscussionThemes, 
)
from discussions_and_notebooks.models import (
    NotebookThemes,
)
from comments.models import (
    Comments,
)
from bookmark.models.Bookmark_models import(
    NotebookBookmarks, CommentBookmarks,
)
from django.views.generic.edit import (
    CreateView,
)
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import Http404
from django.utils import timezone
from django.db.models import (
    Case, When, Value, IntegerField,
    Max, Count,
)
if settings.USE_RECAPTCHA:
    from common_scripts import (
        grecaptcha_request,
    )

class UserInquiryCreateView(CreateView):
    
    template_name = 'user_inquiry/Inquiry/user_inquiry.html'
    model = UserInquiry
    fields = ['email', 'fixed_subject', 'subject_text']

    # reCaptcha_token の検証
    def post(self, request, *args, **kwargs):
        if settings.USE_RECAPTCHA:
            recaptcha_token = self.request.POST.get('g-recaptcha-response')
            if recaptcha_token is None or recaptcha_token == '':
                messages.add_message(self.request, messages.WARNING,
                                    f'不正なPOSTです - reCaptcha ERROR',
                                    )
                return redirect('home')
            else:
                res = grecaptcha_request(recaptcha_token)
                if res:
                    return super().post(request, *args, **kwargs) # SUCCESS
                else:
                    messages.add_message(self.request, messages.WARNING,
                                    f'不正なPOSTです - reCaptcha ERROR',
                                    )
                    return redirect('home')
        else:
            return super().post(request, *args, **kwargs) # SUCCESS

    def form_valid(self, form):
        
        form.instance.date_create = timezone.now()

        # 問い合わせ者
        if self.request.user.is_anonymous:
            form.instance.inquirer_user = None
        else:
            form.instance.inquirer_user = self.request.user

        # GETリクエストパラメータの取得
        comment_pk = self.request.GET.get('comment_pk')
        discussion_pk = self.request.GET.get('discussion_pk')
        notebook_pk = self.request.GET.get('notebook_pk')

        if comment_pk:
            subject_comment = get_object_or_404(Comments, pk=comment_pk)
            form.instance.subject_comment = subject_comment
            if form.instance.fixed_subject == 90 and form.instance.subject_text == '':
                messages.add_message(self.request, messages.WARNING,
                                    f'その他を選択した場合には内容を記載してください',)
                return super().form_invalid(form)
        elif discussion_pk:
            subject_discussion = get_object_or_404(DiscussionThemes, pk=discussion_pk)
            form.instance.subject_discussion = subject_discussion
            if form.instance.fixed_subject == 90 and form.instance.subject_text == '':
                messages.add_message(self.request, messages.WARNING,
                                    f'その他を選択した場合には内容を記載してください',)
                return super().form_invalid(form)
        elif notebook_pk:
            subject_notebook = get_object_or_404(NotebookThemes, pk=notebook_pk)
            form.instance.subject_notebook = subject_notebook
            if form.instance.fixed_subject == 90 and form.instance.subject_text == '':
                messages.add_message(self.request, messages.WARNING,
                                    f'その他を選択した場合には内容を記載してください',)
                return super().form_invalid(form)
        else:
            pass

        return super().form_valid(form)
            

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # GETリクエストパラメータの取得
        notebook_pk = self.request.GET.get('notebook_pk')
        discussion_pk = self.request.GET.get('discussion_pk')
        comment_pk = self.request.GET.get('comment_pk')

        if comment_pk:
            SUBJECT_DATA = get_object_or_404(Comments, pk=comment_pk)
        elif discussion_pk:
            SUBJECT_DATA = get_object_or_404(DiscussionThemes, pk=discussion_pk)
        elif notebook_pk:
            SUBJECT_DATA = NotebookThemes.objects.filter(id=notebook_pk)

            if len(SUBJECT_DATA) == 0:
                raise Http404
 
            # コメント数と最終コメント日の取得
            SUBJECT_DATA = SUBJECT_DATA.annotate(
                                latest_comment_date=Max(
                                    'related_comments_post_notebook_theme__date_create',
                                ),
                                comments_count=Count(
                                   'related_comments_post_notebook_theme',
                                    distinct=True,
                                ),
                           )
        else:
            SUBJECT_DATA = None


        # Bookmark の取得
        if self.request.user.is_anonymous:
            BOOKMARK_NOTEBOOKS_ID_LIST = None
            BOOKMARK_COMMENT_ID_LIST = None
        else:
            BOOKMARK_NOTEBOOKS_ID_LIST = NotebookBookmarks.objects.filter(user=self.request.user).values_list('subject', flat=True)
            BOOKMARK_COMMENT_ID_LIST = CommentBookmarks.objects.filter(user=self.request.user).values_list('subject', flat=True)


        context.update({
                # redirect
                'comment_pk': comment_pk,
                'discussion_pk': discussion_pk,
                'notebook_pk': notebook_pk,
                # SUBJECT_DATA
                'SUBJECT_DATA': SUBJECT_DATA,
                # ユーザのブックマークデータ
                'BOOKMARK_NOTEBOOKS_ID_LIST': BOOKMARK_NOTEBOOKS_ID_LIST,
                'BOOKMARK_COMMENT_ID_LIST': BOOKMARK_COMMENT_ID_LIST,
                # Use recaptcha
                'USE_RECAPTCHA': settings.USE_RECAPTCHA,
        })

        if settings.USE_RECAPTCHA:
            context['RECAPTCHA_PUBLIC_KEY'] = settings.RECAPTCHA_PUBLIC_KEY

        return context

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO,
                             f'お問い合わせを受け付けました',)
        return reverse_lazy('home')