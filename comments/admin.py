from django.contrib import admin
from comments.models import(
    Comments,
    DiscussionCommentsCount, NotebookCommentsCount,
)

from django_summernote.admin import SummernoteModelAdmin


class CommentsAdmin(SummernoteModelAdmin):

    summernote_fields = 'text'

    list_display_ = ('post_discussion_theme',
                     'post_notebook_theme',
                     'post_user',
                     'date_create',
                     )
    list_display = list_display_
    list_display_links = list_display_

    # 表示項目
    fieldsets = (
        ('投稿者', {'fields': (
            'post_user',
            'date_create',
            )}),
        ('関連情報', {'fields': (
            'post_discussion_theme',
            'post_notebook_theme',
            )}),
        ('投稿内容', {'fields': (
            'text',
            )}),
    )

    list_filter = ['post_discussion_theme',
                   'post_notebook_theme',
                   'post_user',
                   'date_create',
                   ]
    search_fields = ('post_discussion_theme__title',
                     'post_notebook_theme__title',
                     'post_user__email',
                     'post_user__username',
                     )
    ordering = ('post_notebook_theme', 'post_discussion_theme')


admin.site.register(Comments, CommentsAdmin)
admin.site.register(DiscussionCommentsCount)
admin.site.register(NotebookCommentsCount)