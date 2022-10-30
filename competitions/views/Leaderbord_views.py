from submission.models import (
    SubmissionUser,
)
from competitions.models import (
    Competitions, JoinCompetitionUsers,
)
from django.views.generic import (
    ListView,
)
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import (
    Max, Min,
)

# Leaderboardの表示
class LeaderboardView(ListView):

    model = SubmissionUser
    template_name = 'competitions/CompetitionLeaderboard/competition_leaderboard.html'
    context_object_name = "public_score_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        unique_competition_id = self.kwargs['unique_competition_id']

        public_score_list, private_score_list = get_competition_rank(unique_competition_id)

        context.update({
                'public_score_list': public_score_list,
                'private_score_list': private_score_list,
            })

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

        competition = get_object_or_404(Competitions, unique_competition_id=unique_competition_id, is_public=True)

        # 開催中のコンペを表示している場合、かついづれかのコンペでSubmitを1回だけ、かつ最終評価対象を今まで1つも選択していない場合チュートリアル表示
        now = timezone.localtime(timezone.now())
        date_close = timezone.localtime(competition.date_close)

        if self.request.user.is_anonymous:
            IS_TUTORIAL = False
        elif (now < date_close) and SubmissionUser.objects.filter(join_user=self.request.user).count() == 1 and not SubmissionUser.objects.filter(join_user=self.request.user, Final_Evaluation=True).exists():
            IS_TUTORIAL = True
        else:
            IS_TUTORIAL = False

        context.update({
                # チュートリアルの表示
                'IS_TUTORIAL': IS_TUTORIAL,
                # コンペティションデータ
                'COMPETITION_DATA': get_object_or_404(Competitions, unique_competition_id=unique_competition_id),
                # 参加ユーザ数
                'User_JOINED_COUNT': Competitions.objects.filter(related_join_competition_users_competitions__competition = competition).count(),
            })
        return context

    def get_queryset(self, **kwargs):
        return None


def get_competition_rank(unique_competition_id):

    competition = get_object_or_404(Competitions, unique_competition_id=unique_competition_id, is_public=True)
    date_close = competition.date_close
    Evaluation_Minimize = competition.Evaluation_Minimize
    join_user = JoinCompetitionUsers.objects.filter(competition__unique_competition_id=unique_competition_id).values('join_user')


    ####################
    # パブリックスコア
    ####################
    # 評価指標で上位とする条件（最小値、最大値）
    public_score_list=[]
    if Evaluation_Minimize:
        # ベストスコアの取得
        qs = SubmissionUser.objects.filter(competition=competition, date_submission__lte=date_close, join_user__in=join_user).exclude(public_score=None).select_related().values('join_user__unique_account_id').annotate(score=Min('public_score'), date_submission_latest=Max('date_submission')).order_by('score').values(*['join_user__unique_account_id','join_user__username','score','date_submission_latest'])
        for q in qs:
            # ベストスコアを持つ submit を特定 (提出日でソートするため)
            best_submit_data = SubmissionUser.objects.filter(competition=competition, date_submission__lte = date_close, join_user__unique_account_id=q['join_user__unique_account_id'], public_score=q['score']).order_by('date_submission').first()
            public_score_list.append({ 'unique_account_id': q['join_user__unique_account_id'],
                                        'username': q['join_user__username'],
                                        'score': q['score'],
                                        'date_submission_latest':q['date_submission_latest'],
                                        'date_submission':best_submit_data.date_submission })
        # コンペティションの終了日前に Submit されたデータのうち、各ユーザで最小のパブリックスコア
        public_score_list = sorted(public_score_list, key=lambda x: (x['score'], x['date_submission']))
    else:
        # ベストスコアの取得
        qs = SubmissionUser.objects.filter(competition=competition, date_submission__lte=date_close, join_user__in=join_user).exclude(public_score=None).select_related().values('join_user__unique_account_id').annotate(score=Max('public_score'), date_submission_latest=Max('date_submission')).order_by('-score').values(*['join_user__unique_account_id','join_user__username','score','date_submission_latest'])
        for q in qs:
            # ベストスコアを持つ submit を特定 (提出日でソートするため)
            best_submit_data = SubmissionUser.objects.filter(competition=competition, date_submission__lte=date_close, join_user__unique_account_id=q['join_user__unique_account_id'], public_score=q['score']).order_by('date_submission').first()
            public_score_list.append({ 'unique_account_id': q['join_user__unique_account_id'],
                                        'username': q['join_user__username'],
                                        'score': q['score'],
                                        'date_submission_latest':q['date_submission_latest'],
                                        'date_submission':best_submit_data.date_submission })
        # 最大化の場合にはソートを降順
        # コンペティションの終了日前に Submit されたデータのうち、各ユーザで最大のパブリックスコア
        public_score_list = sorted(public_score_list, key=lambda x: (x['score']*-1, x['date_submission']))


    ####################
    # プライベートスコア
    ####################
    # コンペ終了後に表示
    if date_close > timezone.now():
        private_score_list = None
    else:
        private_score_list=[]
        # 評価指標で上位とする条件（最小値、最大値）
        if Evaluation_Minimize:
            # ベストスコアの取得
            qs = SubmissionUser.objects.filter(competition=competition, date_submission__lte=date_close, join_user__in=join_user, Final_Evaluation=True).exclude(private_score=None).select_related().values('join_user__unique_account_id').annotate(score=Min('private_score'), date_submission_latest=Max('date_submission')).order_by('score').values(*['join_user__unique_account_id','join_user__username','score','date_submission_latest'])
            for q in qs:
                # ベストスコアを持つ submit を特定 (提出日でソートするため)
                best_submit_data = SubmissionUser.objects.filter(competition=competition, date_submission__lte=date_close, join_user__unique_account_id=q['join_user__unique_account_id'], private_score=q['score']).order_by('date_submission').first()
                private_score_list.append({ 'unique_account_id': q['join_user__unique_account_id'],
                                            'username': q['join_user__username'],
                                            'score': q['score'],
                                            'date_submission_latest':q['date_submission_latest'],
                                            'date_submission':best_submit_data.date_submission })
            # コンペティションの終了日前に Submit されたデータのうち、最終評価対象として各ユーザで最小のプライベートスコア
            private_score_list = sorted(private_score_list, key=lambda x: (x['score'], x['date_submission']))
        else:
            # ベストスコアの取得
            qs = SubmissionUser.objects.filter(competition=competition, date_submission__lte=date_close, join_user__in=join_user, Final_Evaluation=True).exclude(private_score=None).select_related().values('join_user__unique_account_id').annotate(score=Max('private_score'), date_submission_latest=Max('date_submission')).order_by('-score').values(*['join_user__unique_account_id','join_user__username','score','date_submission_latest'])
            for q in qs:
                # ベストスコアを持つ submit を特定 (提出日でソートするため)
                best_submit_data = SubmissionUser.objects.filter(competition=competition, date_submission__lte=date_close, join_user__unique_account_id=q['join_user__unique_account_id'], private_score=q['score']).order_by('date_submission').first()
                private_score_list.append({ 'unique_account_id': q['join_user__unique_account_id'],
                                            'username': q['join_user__username'],
                                            'score': q['score'],
                                            'date_submission_latest':q['date_submission_latest'],
                                            'date_submission':best_submit_data.date_submission })
            # 最大化の場合にはソートを降順
            # コンペティションの終了日前に Submit されたデータのうち、最終評価対象として各ユーザで最大のプライベートスコア
            private_score_list = sorted(private_score_list, key=lambda x: (x['score']*-1, x['date_submission']))

    return public_score_list, private_score_list