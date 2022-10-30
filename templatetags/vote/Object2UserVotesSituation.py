from vote.models import(
    DiscussionVotes, NotebookVotes, CommentVotes,
)
from discussions_and_notebooks.models import(
    DiscussionThemes, NotebookThemes,
)
from comments.models import (
    Comments,
)
from django import template
from django.shortcuts import get_object_or_404

register = template.Library()


@register.simple_tag
def object2uer_votes_situation(object_id, object_type, user_id):

    if user_id != None:
        try:
            if object_type == 'discussion':
                subject = get_object_or_404(DiscussionThemes, id=object_id)
                user_votes = DiscussionVotes.objects.filter(user__id=user_id,subject=subject).first()
            elif object_type == 'notebook':
                subject = get_object_or_404(NotebookThemes, id=object_id)
                user_votes = NotebookVotes.objects.filter(user__id=user_id,subject=subject).first()
            elif object_type == 'comment':
                subject = get_object_or_404(Comments, id=object_id)
                user_votes = CommentVotes.objects.filter(user__id=user_id,subject=subject).first()
            else:
                pass
            
            if user_votes.votes > 0:
                situation='up_vote'
            elif user_votes.votes < 0:
                situation='down_vote'
            else:
                situation='initial'
        except:
            situation='initial'
    else:
        situation='initial'

    return situation