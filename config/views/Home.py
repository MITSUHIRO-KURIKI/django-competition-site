from django.views.generic import TemplateView
from competitions.models.Competition_models import (
    Competitions, JoinCompetitionUsers,
)
from discussions_and_notebooks.models import (
    DiscussionThemes, NotebookThemes,
)
from submission.models.Submission_models import (
    SubmissionUser,
)
from comments.models.Comments_models import (
    Comments,
)
from bookmark.models import(
    DiscussionBookmarks, NotebookBookmarks, CommentBookmarks,
)
from vote.models import(
    DiscussionVotes, NotebookVotes, CommentVotes,
)
from django.contrib.auth import get_user_model
User = get_user_model()

class HomeView(TemplateView):

    template_name = 'home/home.html'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        USER_COUNT = User.objects.count()
        COMPETITION_COUNT = Competitions.objects.filter(is_public=True).count()
        DISCUSSION_COUNT = DiscussionThemes.objects.count()
        NOTEBOOK_COUNT = NotebookThemes.objects.count()

        context.update({
                'USER_COUNT': USER_COUNT,
                'COMPETITION_COUNT': COMPETITION_COUNT,
                'DISCUSSION_COUNT': DISCUSSION_COUNT,
                'NOTEBOOK_COUNT': NOTEBOOK_COUNT,
                'IS_PAGE_HOME': True,
            })

        if self.request.user.is_anonymous:
            context.update({
                'USER_IS_ANONYMOUS': True,
            })
        else:
            USER_JOIN_COMPETITION_COUNT = JoinCompetitionUsers.objects.filter(join_user=self.request.user, competition__is_public=True).count()
            USER_SUBMISSION_COUNT = SubmissionUser.objects.filter(join_user=self.request.user).count()
            USER_POST_DISCUSSION_COUNT = DiscussionThemes.objects.filter(post_user=self.request.user).count()
            USER_POST_NOTEBOOK_COUNT = NotebookThemes.objects.filter(post_user=self.request.user).count()
            USER_POST_COMMENT_COUNT = Comments.objects.filter(post_user=self.request.user).count()
            USER_VOTE_LIKE_DISCUSSION = DiscussionVotes.objects.filter(user=self.request.user, votes=1).count()
            USER_VOTE_LIKE_NOTEBOOK = NotebookVotes.objects.filter(user=self.request.user, votes=1).count()
            USER_VOTE_LIKE_COMMENT = CommentVotes.objects.filter(user=self.request.user, votes=1).count()
            USER_VOTE_LIKE_COUNT = USER_VOTE_LIKE_DISCUSSION+USER_VOTE_LIKE_NOTEBOOK+USER_VOTE_LIKE_COMMENT
            USER_BOOKMARK_DISCUSSION = DiscussionBookmarks.objects.filter(user=self.request.user).count()
            USER_BOOKMARK_NOTEBOOK = NotebookBookmarks.objects.filter(user=self.request.user).count()
            USER_BOOKMARK_COMMENT = CommentBookmarks.objects.filter(user=self.request.user).count()
            USER_BOOKMARK_COUNT = USER_BOOKMARK_DISCUSSION+USER_BOOKMARK_NOTEBOOK+USER_BOOKMARK_COMMENT
            
            context.update({
                    'USER_JOIN_COMPETITION_COUNT': USER_JOIN_COMPETITION_COUNT,
                    'USER_SUBMISSION_COUNT': USER_SUBMISSION_COUNT,
                    'USER_POST_DISCUSSION_COUNT': USER_POST_DISCUSSION_COUNT,
                    'USER_POST_NOTEBOOK_COUNT': USER_POST_NOTEBOOK_COUNT,
                    'USER_POST_COMMENT_COUNT': USER_POST_COMMENT_COUNT,
                    'USER_VOTE_LIKE_COUNT': USER_VOTE_LIKE_COUNT,
                    'USER_BOOKMARK_COUNT': USER_BOOKMARK_COUNT,
                })
        return context
