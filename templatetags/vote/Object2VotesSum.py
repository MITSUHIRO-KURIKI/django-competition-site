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
from django.db.models import (
    Sum,
)

register = template.Library()


@register.simple_tag
def object2votes_sum(object_id, object_type):

    try:
        if object_type == 'discussion':
            subject = get_object_or_404(DiscussionThemes, id=object_id)
            votes_sum = DiscussionVotes.objects.filter(subject=subject).aggregate(votes_sum=Sum('votes'))
        elif object_type == 'notebook':
            subject = get_object_or_404(NotebookThemes, id=object_id)
            votes_sum = NotebookVotes.objects.filter(subject=subject).aggregate(votes_sum=Sum('votes'))
        elif object_type == 'comment':
            subject = get_object_or_404(Comments, id=object_id)
            votes_sum = CommentVotes.objects.filter(subject=subject).aggregate(votes_sum=Sum('votes'))
        else:
            pass
        
        if votes_sum['votes_sum'] is None:
            votes_sum['votes_sum'] = 0
    except:
        votes_sum['votes_sum'] = 0

    return votes_sum['votes_sum']