from django.conf import settings
from discussions_and_notebooks.models import (
    DiscussionThemes,
)
from bookmark.models import(
    DiscussionBookmarks,
)
from discussions_and_notebooks.forms import (
    DeleteDiscussionForm,
)
from discussions_and_notebooks.forms import (
    PostDiscussionForm,
)
from django.views.generic import (
    UpdateView, DeleteView,
)
from django.views.generic.edit import (
    FormMixin,
)
from comments.Convert import (
    convert_comment, del_image,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

User = get_user_model()


class DiscussionUpdateView(LoginRequiredMixin, UpdateView):

    template_name = 'discussions_and_notebooks/discussions/DiscussionEdit/discussion_edit.html'
    model = DiscussionThemes
    form_class = PostDiscussionForm

    def form_valid(self, form):
        # 削除された画像を消去
        try:
            pre_post = get_object_or_404(self.model, pk=form.instance.pk)
            del_image(pre_post.text, form.instance.text)
        except: pass

        # convert text for mention
        convert_text = convert_comment(form.instance.text)
        form.instance.text = convert_text

        if self.request.user.is_superuser or self.request.user.is_staff:
            pass
        else:
            form.instance.is_top = False
            form.instance.use_bot_icon = False
        
        if form.instance.post_user != self.request.user:
            messages.add_message(self.request, messages.WARNING,
                                f'他人のNotebookは編集できません',)
            return super().form_invalid(form)
        else:
            messages.add_message(self.request, messages.INFO,
                        f'CHANGE DONE!',)
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        summernote_add_js = settings.SUMMERNOTE_CONFIG['js']
        summernote_add_css = settings.SUMMERNOTE_CONFIG['css']

        ALL_USER_NAME_LIST = list(User.objects.filter(is_active=True).values_list('username', flat=True))

        # Bookmark の取得
        BOOKMARK_DISCUSSIONS_ID_LIST = DiscussionBookmarks.objects.filter(user=self.request.user).values_list('subject', flat=True)

        context.update({
                # summernote_add_js and summernote_add_css
                'summernote_add_js': list(summernote_add_js),
                'summernote_add_css': list(summernote_add_css),
                # ALL_USER_NAME_LIST for mention
                'ALL_USER_NAME_LIST': ALL_USER_NAME_LIST,
                # ユーザのブックマークデータ
                'BOOKMARK_DISCUSSIONS_ID_LIST': BOOKMARK_DISCUSSIONS_ID_LIST,
        })
        return context

    def get_success_url(self):
        return reverse_lazy('discussions:discussion_page', kwargs={'pk': self.object.id})


class DiscussionDeleteView(LoginRequiredMixin, FormMixin, DeleteView):

    template_name = 'discussions_and_notebooks/discussions/DiscussionEdit/discussion_delete.html'
    model = DiscussionThemes
    form_class = DeleteDiscussionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Bookmark の取得
        BOOKMARK_DISCUSSIONS_ID_LIST = DiscussionBookmarks.objects.filter(user=self.request.user).values_list('subject', flat=True)

        context.update({
                # ユーザのブックマークデータ
                'BOOKMARK_DISCUSSIONS_ID_LIST': BOOKMARK_DISCUSSIONS_ID_LIST,
        })

        return context

    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        form = self.get_form()
        
        check_text = request.POST['check_text']


        if self.object.post_user != self.request.user:
            messages.add_message(self.request, messages.WARNING,
                                f'他人のNotebookは削除できません',)
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


    def get_success_url(self):

        # GETリクエストパラメータの取得
        redirect_competition_pk = self.request.GET.get('redirect_competition_pk')

        if redirect_competition_pk:
            return reverse_lazy('discussions:competition_discussions', kwargs={'unique_competition_id' : redirect_competition_pk})
        else:
            return reverse_lazy('discussions:discussions')