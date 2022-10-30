from submission.models import (
    SubmissionUser,
)
from competitions.models import (
    Competitions,
)
from extra_views import (
    ModelFormSetView,
)
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin


class SubmissionSelectUpdateView(LoginRequiredMixin, ModelFormSetView):

    model = SubmissionUser
    template_name = 'submission/UserSubmission/user_submissions.html'
    fields = ('submission_file_description', 'Final_Evaluation',)
    factory_kwargs = {'extra': 0}


    def get_queryset(self):
        competition = get_object_or_404(Competitions, unique_competition_id = self.kwargs['unique_competition_id'], is_public=True)
        return self.model.objects.filter(competition=competition, join_user=self.request.user).order_by('-date_submission')

    def formset_valid(self, formset):
        
        formset.save(commit=False)

        Final_Evaluation_Limit = get_object_or_404(Competitions, unique_competition_id = self.kwargs['unique_competition_id']).Final_Evaluation_Limit
        date_close = get_object_or_404(Competitions, unique_competition_id = self.kwargs['unique_competition_id']).date_close

        # コンペティション終了後の最終提出不可の判定
        if date_close < timezone.now():
            messages.add_message(self.request, messages.WARNING,
                                 f'コンペティション終了後の最終提出の変更はできません',
                                 )
            return self.render_to_response(self.get_context_data(formset=formset))
        
        # コンペティション最終提出数上限判定
        count=0
        for form in formset:
            # 登録する Final_Evaluation 数をカウント
            if form.instance.Final_Evaluation:
                count += 1
        if count > Final_Evaluation_Limit:
            messages.add_message(self.request, messages.WARNING,
                                 f'最終提出数が上限を超えています（上限: {Final_Evaluation_Limit}）',
                                 )
            return self.render_to_response(self.get_context_data(formset=formset))

        messages.add_message(self.request, messages.INFO,
                             f'Change DONE',
                             )
        return super().formset_valid(formset)

    def get_context_data(self, **kwargs):
        
        context = super(SubmissionSelectUpdateView, self).get_context_data(**kwargs)
        
        unique_competition_id = self.kwargs['unique_competition_id']

        competition = get_object_or_404(Competitions, unique_competition_id=unique_competition_id)

        if Competitions.objects.filter(related_join_competition_users_competitions__competition=competition, related_join_competition_users_competitions__join_user = self.request.user).exists():
            IS_USER_COMPETITION_JOINED=True
        else:
            IS_USER_COMPETITION_JOINED=False

        # 開催中のコンペを表示している場合、かつ最終評価対象を今まで1つも選択していない場合チュートリアル表示
        now = timezone.localtime(timezone.now())
        date_close = timezone.localtime(competition.date_close)
        if (now < date_close) and not SubmissionUser.objects.filter(join_user=self.request.user, Final_Evaluation=True).exists():
            IS_TUTORIAL = True
        else:
            IS_TUTORIAL = False

        context.update({
                # ユーザ登録状況
                'IS_USER_COMPETITION_JOINED': IS_USER_COMPETITION_JOINED,
                # コンペティションデータ
                'COMPETITION_DATA': get_object_or_404(Competitions, unique_competition_id=unique_competition_id),
                # 参加ユーザ数
                'User_JOINED_COUNT': Competitions.objects.filter(related_join_competition_users_competitions__competition=competition).count(),
                # 更新しないモデルの object の引き渡し ( self.get_queryset と同じ順で並び替えること ）
                'object_list': self.model.objects.filter(competition=competition, join_user=self.request.user).order_by('-date_submission'),
                # チュートリアルの表示
                'IS_TUTORIAL': IS_TUTORIAL,
                # 現在時刻
                'DATE_NOW': timezone.now(), 
            })
        
        return context

    def get_success_url(self):
        return reverse_lazy('submission:user_submissions', kwargs={'unique_competition_id' : self.kwargs['unique_competition_id']})
