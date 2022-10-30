from django.contrib.auth import get_user_model
from django.db import models
from discussions_and_notebooks.models import(
    DiscussionThemes, NotebookThemes,
)
from comments.models import (
    Comments,
)

User = get_user_model()


class DiscussionBookmarks(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='related_discussion_bookmarks_user',)
    subject = models.ForeignKey(DiscussionThemes, on_delete=models.CASCADE, db_index=True, blank=False, null=False,
                                         related_name='related_discussion_bookmarks_discussion_subject',)

    class Meta:
        db_table = 'discussion_bookmarks_model'
        verbose_name=verbose_name_plural='Bookmarks_Discussion'


class NotebookBookmarks(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='related_notebook_bookmarks_user',)
    subject = models.ForeignKey(NotebookThemes, on_delete=models.CASCADE, db_index=True, blank=False, null=False,
                                related_name='related_notebook_bookmarks_notebook_subject',)
    
    class Meta:
        db_table = 'notebook_bookmarks_model'
        verbose_name=verbose_name_plural='Bookmarks_Notebook'


class CommentBookmarks(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='related_comment_bookmarks_user',)
    subject = models.ForeignKey(Comments, on_delete=models.CASCADE, db_index=True, blank=False, null=False,
                                related_name='related_comment_bookmarks_subject',)
    
    class Meta:
        db_table = 'comment_bookmarks_model'
        verbose_name=verbose_name_plural='Bookmarks_Comment'