from django.conf import settings
from discussions_and_notebooks.models import (
    DiscussionThemes,
)
from competitions.models import (
    Competitions, JoinCompetitionUsers,
)
from discussions_and_notebooks.forms import (
    PostDiscussionForm,
)
from django.views.generic.edit import (
    CreateView,
)
from comments.Convert import (
    convert_comment,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import (
    reverse_lazy,
)
from django.contrib import messages

User = get_user_model()


class DiscussionCreateView(LoginRequiredMixin, CreateView):

    template_name = 'discussions_and_notebooks/discussions/DiscussionCreate/discussion_create.html'
    model = DiscussionThemes
    form_class = PostDiscussionForm
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        
        # GETリクエストパラメータの取得
        redirect_competition_id = self.request.GET.get('redirect_competition_id')
        
        if redirect_competition_id != None:
            competition = get_object_or_404(Competitions, unique_competition_id=redirect_competition_id)
            
            if Competitions.objects.filter(related_join_competition_users_competitions__competition=competition, related_join_competition_users_competitions__join_user=self.request.user).exists():
                IS_USER_COMPETITION_JOINED=True
            else:
                IS_USER_COMPETITION_JOINED=False

            context.update({
                    # ユーザ登録状況
                    'IS_USER_COMPETITION_JOINED': IS_USER_COMPETITION_JOINED,
                    # コンペティションデータ
                    'COMPETITION_DATA': competition,
                    # 参加ユーザ数
                    'User_JOINED_COUNT': Competitions.objects.filter(related_join_competition_users_competitions__competition=competition).count(),
                })

        summernote_add_js = settings.SUMMERNOTE_CONFIG['js']
        summernote_add_css = settings.SUMMERNOTE_CONFIG['css']

        ALL_USER_NAME_LIST = list(User.objects.filter(is_active=True).values_list('username', flat=True))

        context.update({
                # summernote_add_js and summernote_add_css
                'summernote_add_js': list(summernote_add_js),
                'summernote_add_css': list(summernote_add_css),
                # ALL_USER_NAME_LIST for mention
                'ALL_USER_NAME_LIST': ALL_USER_NAME_LIST,
                # 登録タグ一覧
                'redirect_competition_id': redirect_competition_id,
            })

        return context

    def form_valid(self, form):

        form.instance.post_user = self.request.user

        if self.request.user.is_superuser or self.request.user.is_staff:
            pass
        else:
            form.instance.is_top = False
            form.instance.use_bot_icon = False

        # convert text for mention
        convert_text = convert_comment(form.instance.text)
        form.instance.text = convert_text

        # GETリクエストパラメータの取得
        redirect_competition_id = self.request.GET.get('redirect_competition_id')

        if redirect_competition_id != None:
            if self.request.user.is_superuser or self.request.user.is_staff:
                competition = get_object_or_404(Competitions, unique_competition_id=redirect_competition_id)
                if not competition.is_public:
                    messages.add_message(self.request, messages.INFO,
                                         f'このコンペティションは公開されていません',)
            else:
                competition = get_object_or_404(Competitions, unique_competition_id=redirect_competition_id, is_public=True)
            
            post_user_is_join = JoinCompetitionUsers.objects.filter(competition=competition, join_user=self.request.user).count()
            if self.request.user.is_superuser or self.request.user.is_staff:
                form.instance.post_competition_or_none = competition
                messages.add_message(self.request, messages.INFO,
                                    f'SUCSESS!',)
                return super().form_valid(form)
            elif post_user_is_join == 0:
                messages.add_message(self.request, messages.WARNING,
                                    f'参加していないコンペティションの Notebook には投稿できません',)
                return super().form_invalid(form)
            else:
                form.instance.post_competition_or_none = competition
                messages.add_message(self.request, messages.INFO,
                                    f'SUCSESS!',)
                return super().form_valid(form)
        else:
            messages.add_message(self.request, messages.INFO,
                                f'SUCSESS!',)
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('discussions:discussion_page', kwargs={'pk': self.object.id})