from discussions_and_notebooks.models import (
    NotebookThemes,
)
from bookmark.models import(
    NotebookBookmarks,
)
from discussions_and_notebooks.forms import (
    DeleteNotebookForm,
)
from django.views.generic import (
    UpdateView, DeleteView,
)
from django.views.generic.edit import (
    FormMixin,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy


class NotebookUpdateView(LoginRequiredMixin, UpdateView):

    template_name = 'discussions_and_notebooks/notebooks/NotebookEdit/notebook_edit.html'
    model = NotebookThemes
    fields = ['title',
              'tags_or_none',
              'notebook_file',
              'notebook_data_file',
              'is_top',
              'use_bot_icon',
              ]

    def form_valid(self, form):

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

        # Bookmark の取得
        BOOKMARK_NOTEBOOKS_ID_LIST = NotebookBookmarks.objects.filter(user=self.request.user).values_list('subject', flat=True)

        context.update({
                # ユーザのブックマークデータ
                'BOOKMARK_NOTEBOOKS_ID_LIST': BOOKMARK_NOTEBOOKS_ID_LIST,
        })

        return context

    def get_success_url(self):
        return reverse_lazy('notebooks:notebook_page', kwargs={'pk': self.object.id})


class NotebookDeleteView(LoginRequiredMixin, FormMixin, DeleteView):

    template_name = 'discussions_and_notebooks/notebooks/NotebookEdit/notebook_delete.html'
    model = NotebookThemes
    form_class = DeleteNotebookForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Bookmark の取得
        BOOKMARK_NOTEBOOKS_ID_LIST = NotebookBookmarks.objects.filter(user=self.request.user).values_list('subject', flat=True)

        context.update({
                # ユーザのブックマークデータ
                'BOOKMARK_NOTEBOOKS_ID_LIST': BOOKMARK_NOTEBOOKS_ID_LIST,
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
            if check_text == 'delete':
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
            return reverse_lazy('notebooks:competition_notebooks', kwargs={'unique_competition_id' : redirect_competition_pk})
        else:
            return reverse_lazy('notebooks:notebooks')