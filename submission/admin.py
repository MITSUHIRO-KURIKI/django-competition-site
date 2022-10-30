from django.contrib import admin
from submission.models import(
    SubmissionUser
)

class SubmissionUserAdmin(admin.ModelAdmin):

    list_display_ = ('join_user',
                     'competition',
                     'public_score',
                     'private_score',
                     'Final_Evaluation',
                     'date_submission',
                     )
    list_display = list_display_
    list_display_links = list_display_

    # 表示項目
    fieldsets = (
        ('ユーザ', {'fields': (
            'join_user',
            )}),
        ('コンペティション', {'fields': (
            'competition',
            )}),
        ('スコア', {'fields': (
            'public_score',
            'private_score',
            )}),
        ('最終評価対象', {'fields': (
            'Final_Evaluation',
            )}),
        ('提出日', {'fields': (
            'date_submission',
            )}),
    )

    list_filter = ['join_user',
                   'competition',
                   'Final_Evaluation',
                   'date_submission',
                   ]
    search_fields = ('join_user__email',
                     'join_user__username',
                     'competition__title',
                     'competition__unique_competition_id',
                     )
    ordering = ('competition',)


admin.site.register(SubmissionUser, SubmissionUserAdmin)