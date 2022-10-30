from django.conf import settings
from comments.models import (
    Comments,
)
from bookmark.models.Bookmark_models import(
    CommentBookmarks,
)
from comments.forms import (
    PostCommentForm, DeleteCommentForm,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    UpdateView, DeleteView,
)
from comments.Convert import (
    convert_comment, del_image,
)
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

User = get_user_model()


class CommentUpdateView(LoginRequiredMixin, UpdateView):

    template_name = 'comments/CommentEdit/comment_edit.html'
    model = Comments
    form_class = PostCommentForm

    def form_valid(self, form):
        # 削除された画像を消去
        try:
            pre_post = get_object_or_404(self.model, pk=form.instance.pk)
            del_image(pre_post.text, form.instance.text)
        except: pass

        # convert text for mention
        convert_text = convert_comment(form.instance.text)
        form.instance.text = convert_text

        if form.instance.post_user != self.request.user:
            messages.add_message(self.request, messages.WARNING,
                                f'他人のコメントは編集できません',)
            return super().form_invalid(form)
        else:
            messages.add_message(self.request, messages.INFO,
                        f'CHANGE DONE!',)
            return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # GETリクエストパラメータの取得
        redirect_notebook_pk = self.request.GET.get('redirect_notebook_pk')
        redirect_discussion_pk = self.request.GET.get('redirect_discussion_pk')

        summernote_add_js = settings.SUMMERNOTE_CONFIG['js']
        summernote_add_css = settings.SUMMERNOTE_CONFIG['css']

        ALL_USER_NAME_LIST = list(User.objects.filter(is_active=True).values_list('username', flat=True))

        context.update({
                # redirect
                'redirect_notebook_pk': redirect_notebook_pk,
                'redirect_discussion_pk': redirect_discussion_pk,
                # summernote_add_js and summernote_add_css
                'summernote_add_js': list(summernote_add_js),
                'summernote_add_css': list(summernote_add_css),
                # ALL_USER_NAME_LIST for mention
                'ALL_USER_NAME_LIST': ALL_USER_NAME_LIST,
        })
        return context

    def get_success_url(self):

        # GETリクエストパラメータの取得
        redirect_notebook_pk = self.request.GET.get('redirect_notebook_pk')
        redirect_discussion_pk = self.request.GET.get('redirect_discussion_pk')

        if redirect_notebook_pk:
            return reverse_lazy('notebooks:notebook_page_comments', kwargs={'pk' : redirect_notebook_pk})
        elif redirect_discussion_pk:
            return reverse_lazy('discussions:discussion_page', kwargs={'pk' : redirect_discussion_pk})
        else:
            return reverse_lazy('home')


class CommentDeleteView(LoginRequiredMixin, DeleteView):

    template_name = 'comments/CommentEdit/comment_delete.html'
    model = Comments
    form_class = DeleteCommentForm

    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        form = self.get_form()
        
        # GETリクエストパラメータの取得
        check_text = request.POST['check_text']

        if self.object.post_user != self.request.user:
            messages.add_message(self.request, messages.WARNING,
                                f'他人のコメントは削除できません',)
            return redirect(self.get_success_url())
        else:
            if check_text=='delete':
                if form.is_valid():
                    return self.form_valid(form)
                else:
                    return self.form_invalid(form)
            else:
                messages.add_message(self.request, messages.WARNING,
                                    f'False',)
                return self.form_invalid(form)

    def form_valid(self, form):
        self.object.delete()
        messages.add_message(self.request, messages.INFO,
                            f'Delete Sucsess',)
        return redirect(self.get_success_url())


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # GETリクエストパラメータの取得
        redirect_notebook_pk = self.request.GET.get('redirect_notebook_pk')
        redirect_discussion_pk = self.request.GET.get('redirect_discussion_pk')

        COMMTNT_DATA = get_object_or_404(self.model, id=self.kwargs['pk'])

        # Bookmark の取得
        BOOKMARK_COMMENT_ID_LIST = CommentBookmarks.objects.filter(user=self.request.user).values_list('subject', flat=True)

        context.update({
                # コメントデータ
                'COMMTNT_DATA': COMMTNT_DATA,
                # redirect
                'redirect_notebook_pk': redirect_notebook_pk,
                'redirect_discussion_pk': redirect_discussion_pk,
                # ユーザのブックマークデータ
                'BOOKMARK_COMMENT_ID_LIST': BOOKMARK_COMMENT_ID_LIST,
        })
        
        return context

    def get_success_url(self):

        # GETリクエストパラメータの取得
        redirect_notebook_pk = self.request.GET.get('redirect_notebook_pk')
        redirect_discussion_pk = self.request.GET.get('redirect_discussion_pk')

        if redirect_notebook_pk:
            return reverse_lazy('notebooks:notebook_page_comments', kwargs={'pk' : redirect_notebook_pk})
        elif redirect_discussion_pk:
            return reverse_lazy('discussions:discussion_page', kwargs={'pk' : redirect_discussion_pk})
        else:
            return reverse_lazy('home')