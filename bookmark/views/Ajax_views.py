from bookmark.models import(
    DiscussionBookmarks, NotebookBookmarks, CommentBookmarks,
)
from discussions_and_notebooks.models import(
    DiscussionThemes, NotebookThemes,
)
from comments.models import (
    Comments,
)
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


def bookmark_post(request):

    object_type=None
    object_id=None
    process=None

    if request.method == 'POST':
        if request.user.is_authenticated:
            object_type = request.POST.get('object_type')
            object_id = request.POST.get('object_id')
            user = request.user

            if object_type == 'discussion':
                subject = get_object_or_404(DiscussionThemes, id=object_id)
                bookmarks = DiscussionBookmarks.objects.filter(user=user,subject=subject).all()
            elif object_type == 'notebook':
                subject = get_object_or_404(NotebookThemes, id=object_id)
                bookmarks = NotebookBookmarks.objects.filter(user=user,subject=subject).all()
            elif object_type == 'comment':
                subject = get_object_or_404(Comments, id=object_id)
                bookmarks = CommentBookmarks.objects.filter(user=user,subject=subject).all()
            else:
                pass
            

            if bookmarks.exists():
                process='delete'
                bookmarks.delete()
            else:
                process='create'
                bookmarks.create(user=user,subject=subject)

    context={
        'object_type':object_type,
        'object_id':object_id,
        'process':process,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(context)
