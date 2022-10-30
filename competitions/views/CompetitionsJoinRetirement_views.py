from competitions.models import (
    Competitions, JoinCompetitionUsers,
)
from django.views.generic import (
    DeleteView,
)
from django.views.generic.edit import (
    CreateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404


# Competitionへの参加
class JoinUserCreateView(LoginRequiredMixin, CreateView):
    fields = []
    model = JoinCompetitionUsers
    template_name = 'competitions/CompetitionPage/join.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        unique_competition_id = self.kwargs['unique_competition_id']

        competition = get_object_or_404(Competitions, unique_competition_id=unique_competition_id, is_public=True)
        
        if Competitions.objects.filter(unique_competition_id=unique_competition_id, related_join_competition_users_competitions__join_user = self.request.user).exists():
            IS_USER_COMPETITION_JOINED=True
        else:
            IS_USER_COMPETITION_JOINED=False
        
        context.update({
                # ユーザ登録状況
                'IS_USER_COMPETITION_JOINED': IS_USER_COMPETITION_JOINED,
                # コンペティションデータ
                'COMPETITION_DATA': get_object_or_404(Competitions, unique_competition_id=unique_competition_id),
                # 参加ユーザ数
                'User_JOINED_COUNT': Competitions.objects.filter(related_join_competition_users_competitions__competition = competition).count(),
            })
        return context

    def form_valid(self, form):

        unique_competition_id = self.kwargs['unique_competition_id']

        competition = get_object_or_404(Competitions, unique_competition_id=unique_competition_id, is_public=True)
        user_count = self.model.objects.filter(competition = competition, join_user = self.request.user).count()
        
        if user_count > 0:
            messages.add_message(self.request, messages.WARNING,
                                 f'既に登録済みです',)
            return super().form_invalid(form)
        else:
            form.instance.join_user = self.request.user
            form.instance.competition = competition
            messages.add_message(self.request, messages.INFO,
                                f'Join Competition',)
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('competitions:competition_detail', kwargs={'unique_competition_id' : self.kwargs['unique_competition_id']})


# Competitionからのリタイア
class JoinUserDeleteView(LoginRequiredMixin, DeleteView):
    model = JoinCompetitionUsers
    template_name = 'competitions/CompetitionPage/retirement.html'

    def get_object(self):
        competition = get_object_or_404(Competitions, unique_competition_id = self.kwargs['unique_competition_id'], is_public=True)
        return get_object_or_404(self.model, competition = competition, join_user = self.request.user)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        unique_competition_id = self.kwargs['unique_competition_id']

        competition = get_object_or_404(Competitions, unique_competition_id=unique_competition_id)
        
        if Competitions.objects.filter(unique_competition_id=unique_competition_id, related_join_competition_users_competitions__join_user = self.request.user).exists():
            IS_USER_COMPETITION_JOINED=True
        else:
            IS_USER_COMPETITION_JOINED=False
        
        context.update({
                # ユーザ登録状況
                'IS_USER_COMPETITION_JOINED': IS_USER_COMPETITION_JOINED,
                # コンペティションデータ
                'COMPETITION_DATA': get_object_or_404(Competitions, unique_competition_id=unique_competition_id),
                # 参加ユーザ数
                'User_JOINED_COUNT': Competitions.objects.filter(related_join_competition_users_competitions__competition = competition).count(),
                # 現在時刻
                'DATE_NOW': timezone.now(), 
            })
        return context

    def form_valid(self, form):

        date_close = self.object.competition.date_close
        if date_close > timezone.now():
            self.object.delete()
            messages.add_message(self.request, messages.INFO,
                                f'Completed retirement from this competition',)
        else:
            messages.add_message(self.request, messages.WARNING,
                                f'コンペティション終了後のリタイヤは不可です',)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('competitions:competition_detail', kwargs={'unique_competition_id' : self.kwargs['unique_competition_id']})