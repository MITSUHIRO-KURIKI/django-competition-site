from django.contrib import admin
from competitions.models import(
    Competitions, JoinCompetitionUsers, CompetitionsTags,
)
from django_summernote.admin import SummernoteModelAdmin
from django.utils import timezone

class CompetitionsAdmin(SummernoteModelAdmin):

    summernote_fields = ('overview_text',
                         'evaluation_text',
                         'rule_text',
                         'data_text',)

    # コンペ開催中、終了の判定
    def Competition_active(self, obj):
        now = timezone.now()
        close = obj.date_close
        return close >= now
    Competition_active.short_description = 'Active'
    # 表示する文字数の制限
    def character_limit_title(self, obj):
        limit=20
        character = obj.title
        if len(character)>limit:
            character=character[:limit]+'...'
        return character
    def character_limit_unique_competition_id(self, obj):
        limit=20
        character = obj.unique_competition_id
        if len(character)>limit:
            character=character[:limit]+'...'
        return character

    # 紐付いている外部のテーブルを参照
    def External_Reference_active_users(self, obj):
        return obj.related_join_competition_users_competitions.all().count()
    External_Reference_active_users.short_description = 'active_users'

    list_display_ = ('character_limit_title',
                     'date_open',
                     'date_close',
                     'Competition_active',
                     'External_Reference_active_users',
                     'is_public',
                     'create_initial_discussion',
                     'unique_competition_id',
                     'create_user',
                     )
    list_display = list_display_
    list_display_links = list_display_

    # 表示項目
    fieldsets = (
        ('コンペティション設定', {'fields': (
            'unique_competition_id',
            'is_public',
            'create_initial_discussion',
            'create_user',
            )}),
        ('スケジュール', {'fields': (
            'date_open',
            'date_close',
            )}),
        ('コンペティション基本情報', {'fields': (
            'title',
            'subtitle',
            'tags',
            'overall',
            )}),
        ('概要', {'fields': (
            'overview_text',
            )}),
        ('評価', {'fields': (
            'evaluation_text',
            'metrics',
            'Evaluation_Minimize',
            )}),
        ('ルール', {'fields': (
            'rule_text',
            )}),
        ('提供データ', {'fields': (
            'data_text',
            'data_file',
            )}),
        ('正解データ', {'fields': (
            'answer_file',
            'target_cols_name',
            )}),
        ('Submit制約', {'fields': (
            'Submission_Daily_Limit',
            'Final_Evaluation_Limit',
            )}),
    )

    list_filter = ['date_open',
                   'date_close',
                   'is_public',
                   ]
    search_fields = ('title',
                     'unique_competition_id',
                     )
    ordering = ('pk',)

class JoinCompetitionUsersAdmin(admin.ModelAdmin):
    
    list_display_ = ('join_user',
                     'competition',
                     'date_joined',
                     )
    list_display = list_display_
    list_display_links = list_display_

    list_filter = ['join_user',
                   'date_joined',
                   ]
    search_fields = ('join_user__email',
                     'join_user__username',
                     'competition__title',
                     'competition__unique_competition_id',
                     )
    ordering = ('join_user', 'competition')


class CompetitionsTagsAdmin(admin.ModelAdmin):
    list_display_ = ('name',
                     )
    list_display = list_display_
    list_display_links = list_display_

    list_filter = ['name',
                   ]
    search_fields = ('name',
                     )
    ordering = ('name',)


admin.site.register(Competitions, CompetitionsAdmin)
admin.site.register(JoinCompetitionUsers, JoinCompetitionUsersAdmin)
admin.site.register(CompetitionsTags, CompetitionsTagsAdmin)