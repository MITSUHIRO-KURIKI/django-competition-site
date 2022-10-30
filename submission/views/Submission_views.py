from submission.models import (
    SubmissionUser,
)
from competitions.models import (
    Competitions,
)
from django.views.generic.edit import (
    CreateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils import timezone
import datetime

from submission.evaluation import (
    Evaluation,
)


class SubmissionCreateView(LoginRequiredMixin, CreateView):
    
    template_name = 'submission/Submission/submission.html'
    model = SubmissionUser
    fields = ['submission_file', 'submission_file_description']


    def get_form(self):
        form = super(SubmissionCreateView, self).get_form()
        form.fields['submission_file_description'].required = False
        return form

    def form_valid(self, form):

        unique_competition_id = self.kwargs['unique_competition_id']

        competition = get_object_or_404(Competitions, unique_competition_id=unique_competition_id)
        
        form.instance.competition = competition
        form.instance.join_user = self.request.user

        ago = timezone.now() - datetime.timedelta(hours=24)
        submissions_period_count = self.model.objects.filter(competition=competition, join_user=self.request.user, date_submission__gte=ago).count()
        Submission_Daily_Limit = get_object_or_404(Competitions, unique_competition_id=unique_competition_id).Submission_Daily_Limit

        # 提出ファイルの処理
        public_score = None
        private_score = None

        # 24時間あたりの提出上限の判定
        if Submission_Daily_Limit <= submissions_period_count:
            messages.add_message(self.request, messages.WARNING,
                                 f'1日あたりのサブミット数を超えています(上限: {Submission_Daily_Limit})',)
            return super().form_invalid(form)

        # 開始前の提出は受け付けない
        if competition.date_open < timezone.now():
            if self.request.FILES['submission_file']:

                # 提出ファイル、正解ファイル、評価指標の読み取り
                submit_file = self.request.FILES['submission_file']
                answer_file = competition.answer_file
                metrics = competition.metrics
                target_cols_name = competition.target_cols_name

                if answer_file == '' or metrics == '' or target_cols_name == '' or answer_file is None or metrics is None or target_cols_name is None:
                    messages.add_message(self.request, messages.WARNING,
                                        f'コンペティションの設定にエラーが発生しています。運営者へ問い合わせてください。',)
                    return super().form_invalid(form)

                try:
                    # スコアを算出
                    public_score, private_score = Evaluation(submit_file, answer_file, metrics, target_cols_name)
                except:
                    messages.add_message(self.request, messages.WARNING,
                                         f'提出ファイルにエラーが発生しています',)
                    return super().form_invalid(form)

            form.instance.public_score = public_score
            form.instance.private_score = private_score

            messages.add_message(self.request, messages.INFO,
                                 f'Submittion Completed!',)
            return super().form_valid(form)
        else:
            messages.add_message(self.request, messages.WARNING,
                                 f'コンペティション開始前の提出はできません',)
            return super().form_invalid(form)
            

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
                'User_JOINED_COUNT': Competitions.objects.filter(related_join_competition_users_competitions__competition=competition).count(),
            })

        return context

    def get_success_url(self):
        return reverse_lazy('competitions:competition_leaderboard', kwargs={'unique_competition_id' : self.kwargs['unique_competition_id']})