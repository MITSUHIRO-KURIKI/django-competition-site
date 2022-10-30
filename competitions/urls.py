from django.urls import include, path
from competitions.views import (
    CompetitionsView, CompetitionDetailView,
    LeaderboardView,
    JoinUserCreateView, JoinUserDeleteView,
    CompetitionCreateView, CompetitionUpdateView,
)


app_name = 'competitions'

urlpatterns = [
    # コンペティション一覧
    path('', CompetitionsView.as_view(), name='home'),
    # コンペティション詳細ページ
    path('<str:unique_competition_id>', CompetitionDetailView.as_view(), name='competition_detail'),
    # コンペティションリーダーボード
    path('<str:unique_competition_id>/leaderboard/', LeaderboardView.as_view(), name='competition_leaderboard'),
    # コンペティションへの参加
    path('<str:unique_competition_id>/join/', JoinUserCreateView.as_view(), name='join_competitions'),
    # コンペティションリタイヤ
    path('<str:unique_competition_id>/retirement/', JoinUserDeleteView.as_view(), name='retirement_competitions'),
    # コンペティション作成
    path('create/new', CompetitionCreateView.as_view(), name='create_competitions'),
    # コンペティション編集
    path('<str:unique_competition_id>/edit/', CompetitionUpdateView.as_view(), name='edit_competitions'),
]