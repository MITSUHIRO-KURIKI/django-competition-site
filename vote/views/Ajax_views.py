from vote.models import(
    DiscussionVotes, NotebookVotes, CommentVotes,
)
from discussions_and_notebooks.models import(
    DiscussionThemes, NotebookThemes,
)
from comments.models import (
    Comments,
)
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


def vote_post(request):

    object_type=None
    object_id=None
    vote_action=None
    situation=None
    votes_sum=None

    if request.method == 'POST':
        if request.user.is_authenticated:
            object_type = request.POST.get('object_type')
            object_id = request.POST.get('object_id')
            vote_action = request.POST.get('vote_action')
            votes_sum = int(request.POST.get('votes_sum'))
            user = request.user

            if object_type == 'discussion':
                subject = get_object_or_404(DiscussionThemes, id=object_id)
                user_votes = DiscussionVotes.objects.filter(user=user,subject=subject).all()
            elif object_type == 'notebook':
                subject = get_object_or_404(NotebookThemes, id=object_id)
                user_votes = NotebookVotes.objects.filter(user=user,subject=subject).all()
            elif object_type == 'comment':
                subject = get_object_or_404(Comments, id=object_id)
                user_votes = CommentVotes.objects.filter(user=user,subject=subject).all()
            else:
                pass

            if user_votes.exists():      
                if vote_action == 'up_vote':
                    if user_votes[0].votes == 1:
                        situation='up'
                    elif user_votes[0].votes == 0:
                        user_votes.update(user=user,subject=subject,votes=1)
                        votes_sum += 1
                        situation='up'
                    else: # user_votes.votes == -1:
                        user_votes.update(user=user,subject=subject,votes=0)
                        votes_sum += 1
                        situation='initial'
                if vote_action == 'down_vote':
                    if user_votes[0].votes == 1:
                        user_votes.update(user=user,subject=subject,votes=0)
                        votes_sum -= 1
                        situation='initial'
                    elif user_votes[0].votes == 0:
                        user_votes.update(user=user,subject=subject,votes=-1)
                        votes_sum -= 1
                        situation='down'
                    else: # votes.votes == -1:
                        situation='down'
            else:
                if vote_action == 'up_vote':
                    user_votes.create(user=user,subject=subject,votes=1)
                    votes_sum += 1
                    situation='up'
                if vote_action == 'down_vote':
                    user_votes.create(user=user,subject=subject,votes=-1)
                    votes_sum -= 1
                    situation='down'

    context={
        'object_type':object_type,
        'object_id':object_id,
        'situation':situation,
        'votes_sum':votes_sum,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(context)
