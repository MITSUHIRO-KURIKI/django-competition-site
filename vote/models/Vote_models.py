from django.contrib.auth import get_user_model
from django.db import models
from discussions_and_notebooks.models import(
    DiscussionThemes, NotebookThemes,
)
from comments.models import (
    Comments,
)
from django.core.validators import (
    MinValueValidator, MaxValueValidator,
)

User = get_user_model()


class DiscussionVotes(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='related_discussion_votes_user',)
    subject = models.ForeignKey(DiscussionThemes, on_delete=models.CASCADE, blank=False, null=False,
                                         related_name='related_discussion_votes_discussion_subject',)
    votes = models.IntegerField(blank=False, null=False, default=0,
                                validators=[MinValueValidator(-1), MaxValueValidator(1)])

    class Meta:
        db_table = 'discussion_votes_model'
        verbose_name=verbose_name_plural='Votes_Discussion'


class NotebookVotes(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='related_notebook_votes_user',)
    subject = models.ForeignKey(NotebookThemes, on_delete=models.CASCADE, blank=False, null=False,
                                related_name='related_notebook_votes_notebook_subject',)
    votes = models.IntegerField(blank=False, null=False, default=0,
                                validators=[MinValueValidator(-1), MaxValueValidator(1)])

    class Meta:
        db_table = 'notebook_votes_model'
        verbose_name=verbose_name_plural='Votes_Notebook'


class CommentVotes(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='related_comment_votes_user',)
    subject = models.ForeignKey(Comments, on_delete=models.CASCADE, blank=False, null=False,
                                related_name='related_comment_votes_subject',)
    votes = models.IntegerField(blank=False, null=False, default=0,
                                validators=[MinValueValidator(-1), MaxValueValidator(1)])

    class Meta:
        db_table = 'comment_votes_model'
        verbose_name=verbose_name_plural='Votes_Comment'