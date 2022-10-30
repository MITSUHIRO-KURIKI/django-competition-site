from django.contrib import admin
from vote.models import(
    DiscussionVotes, NotebookVotes, CommentVotes,
)



class DiscussionVotesAdmin(admin.ModelAdmin):

    list_display_ = ('user',
                     'subject',
                     'votes',
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


class NotebookVotesAdmin(admin.ModelAdmin):

    list_display_ = ('user',
                     'subject',
                     'votes',
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


class CommentVotesAdmin(admin.ModelAdmin):

    list_display_ = ('user',
                     'subject',
                     'votes',
                     )
    list_display = list_display_
    list_display_links = list_display_

    list_filter = ['user',
                   'subject',
                   ]
    search_fields = ('user__email',
                     'user__username',
                     )

admin.site.register(DiscussionVotes, DiscussionVotesAdmin)
admin.site.register(NotebookVotes, NotebookVotesAdmin)
admin.site.register(CommentVotes, CommentVotesAdmin)