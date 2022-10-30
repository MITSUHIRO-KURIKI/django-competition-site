from discussions_and_notebooks.models import (
    NotebookThemes,
)
from competitions.models import (
    Competitions, JoinCompetitionUsers,
)
from django.views.generic.edit import (
    CreateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import (
    reverse_lazy,
)
from django.contrib import messages


class NotebookCreateView(LoginRequiredMixin, CreateView):

    template_name = 'discussions_and_notebooks/notebooks/NotebookCreate/notebook_create.html'
    model = NotebookThemes
    fields = ['title',
              'tags_or_none',
              'notebook_file',
              'notebook_data_file',
              'is_top',
              'use_bot_icon',
              ]
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        
        # GETリクエストパラメータの取得
        redirect_competition_id = self.request.GET.get('redirect_competition_id')
        
        if redirect_competition_id != None:
            competition = get_object_or_404(Competitions, unique_competition_id=redirect_competition_id)
            
            if Competitions.objects.filter(related_join_competition_users_competitions__competition=competition, related_join_competition_users_competitions__join_user = self.request.user).exists():
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

        context.update({
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
        return reverse_lazy('notebooks:notebook_page', kwargs={'pk': self.object.id})