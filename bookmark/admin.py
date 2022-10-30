from django.contrib import admin
from bookmark.models import(
    DiscussionBookmarks, NotebookBookmarks, CommentBookmarks,
)



class DiscussionBookmarksAdmin(admin.ModelAdmin):

    list_display_ = ('user',
                     'subject',
                     )
    list_display = list_display_
    list_display_links = list_display_

    list_filter = ['user',
                   'subject',
                   ]
    search_fields = ('subject__title',
                     'user__email',
                     'user__username',
                     )


class NotebookBookmarksAdmin(admin.ModelAdmin):

    list_display_ = ('user',
                     'subject',
                     )
    list_display = list_display_
    list_display_links = list_display_

    list_filter = ['user',
                   'subject',
                   ]
    search_fields = ('subject__title',
                     'user__email',
                     'user__username',
                     )


class CommentBookmarksAdmin(admin.ModelAdmin):

    list_display_ = ('user',
                     'subject',
                     )
    list_display = list_display_
    list_display_links = list_display_

    list_filter = ['user',
                   'subject',
                   ]
    search_fields = ('user__email',
                     'user__username',
                     )

admin.site.register(DiscussionBookmarks, DiscussionBookmarksAdmin)
admin.site.register(NotebookBookmarks, NotebookBookmarksAdmin)
admin.site.register(CommentBookmarks, CommentBookmarksAdmin)