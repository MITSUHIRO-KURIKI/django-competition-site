from django.contrib import admin
from discussions_and_notebooks.models import(
    DiscussionTags, DiscussionThemes,
    NotebookTags, NotebookThemes, NotebookThemesMeta,
)
from discussions_and_notebooks.models.DummyImage_models import (
    DummyImageUpload,
)

from django_summernote.admin import SummernoteModelAdmin


class DiscussionThemesAdmin(SummernoteModelAdmin):

    summernote_fields = 'text'

    # 紐付いている外部のテーブルを参照
    def External_Reference_comments(self, obj):
        return obj.related_comments_post_discussion_theme.all().count()
    External_Reference_comments.short_description = 'comments'

    list_display_ = ('post_competition_or_none',
                     'title',
                     'post_user',
                     'date_create',
                     'External_Reference_comments',
                     'is_top',
                     'use_bot_icon',
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
            'post_competition_or_none',
            'tags_or_none',
            'is_top',
            'use_bot_icon',
            )}),
        ('投稿内容', {'fields': (
            'title',
            'text',
            )}),
    )

    list_filter = ['post_competition_or_none',
                   'post_user',
                   'date_create',
                   'is_top',
                   ]
    search_fields = ('post_competition_or_none__unique_competition_id',
                     'post_competition_or_none__title',
                     'title',
                     'post_user__email',
                     'post_user__username',
                     )
    ordering = ('post_competition_or_none', )


class NotebookThemesAdmin(admin.ModelAdmin):

    # 紐付いている外部のテーブルを参照
    def External_Reference_comments(self, obj):
        return obj.related_comments_post_notebook_theme.all().count()
    External_Reference_comments.short_description = 'comments'


    list_display_ = ('post_competition_or_none',
                     'title',
                     'post_user',
                     'date_create',
                     'External_Reference_comments',
                     'is_top',
                     'use_bot_icon',
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
            'post_competition_or_none',
            'tags_or_none',
            'is_top',
            'use_bot_icon',
            )}),
        ('投稿内容', {'fields': (
            'title',
            'notebook_file',
            'notebook_data_file',
            )}),
        # ('オブジェクト', {'fields': (
        #     'notebook_style',
        #     'notebook_body',
        #     )}),
    )

    list_filter = ['post_competition_or_none',
                   'post_user',
                   'date_create',
                   'is_top',
                   ]
    search_fields = ('post_competition_or_none__unique_competition_id',
                     'post_competition_or_none__title',
                     'title',
                     'post_user__email',
                     'post_user__username',
                     )
    ordering = ('post_competition_or_none', )



admin.site.register(DiscussionTags)
admin.site.register(DiscussionThemes, DiscussionThemesAdmin)
admin.site.register(DummyImageUpload)
admin.site.register(NotebookTags)
admin.site.register(NotebookThemes, NotebookThemesAdmin)
admin.site.register(NotebookThemesMeta)