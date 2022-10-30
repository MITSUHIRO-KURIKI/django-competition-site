from django.conf import settings
from competitions.models.Competition_models import (
    CompetitionsTags,
)
from discussions_and_notebooks.models import (
    DiscussionTags, NotebookTags,
)
from django.forms import (
    modelformset_factory,
)
from extra_views import (
    ModelFormSetView, FormSetView,
)
from django.views.generic import (
    DeleteView,
)
from django.views.generic.edit import (
    FormMixin,
)
from management.forms import (
    CompetitionModelForm, DiscussionModelForm, NotebookModelForm,
    DeleteTagForm,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect

class TagsUpdateView(LoginRequiredMixin, ModelFormSetView):

    model = CompetitionsTags
    template_name = 'management/tags/tags_list.html'
    fields = ('name',)
    factory_kwargs = {'extra': 0}
    success_url = reverse_lazy('management:tags_list')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        
        DiscussionTagsFormSet = modelformset_factory(model=DiscussionTags, fields=('name',), extra=0)
        discussion_formset = DiscussionTagsFormSet(queryset=DiscussionTags.objects.all(), prefix='discussionform')

        NotebookTagsFormSet = modelformset_factory(model=NotebookTags, fields=('name',), extra=0)
        notebook_formset = NotebookTagsFormSet(queryset=NotebookTags.objects.all(), prefix='notebookform')

        create_tag_competition = CompetitionModelForm()
        create_tag_discussion = DiscussionModelForm() 
        create_tag_notebook = NotebookModelForm() 

        context.update({'discussion_formset': discussion_formset,
                        'notebook_formset': notebook_formset,
                        'create_tag_competition': create_tag_competition,
                        'create_tag_discussion': create_tag_discussion,
                        'create_tag_notebook': create_tag_notebook,
                        })

        IS_DEBUG = settings.DEBUG
        context.update({'IS_DEBUG': IS_DEBUG,
                        })
        
        return context

    def post(self, request, *args, **kwargs):

        CompetitionsTagsFormSet = modelformset_factory(model=CompetitionsTags, fields=('name',), extra=0)
        competition_formset = CompetitionsTagsFormSet(request.POST or None, prefix='form')

        DiscussionTagsFormSet = modelformset_factory(model=DiscussionTags, fields=('name',), extra=0)
        discussion_formset = DiscussionTagsFormSet(request.POST or None, prefix='discussionform')

        NotebookTagsFormSet = modelformset_factory(model=NotebookTags, fields=('name',), extra=0)
        notebook_formset = NotebookTagsFormSet(request.POST or None, prefix='notebookform')

        # ADD NEW TAG
        create_tag_competition = CompetitionModelForm(request.POST)
        create_tag_discussion = DiscussionModelForm(request.POST)
        create_tag_notebook = NotebookModelForm(request.POST)

        if request.POST['new_competition_tags_name'] != '':
            if create_tag_competition.is_valid():
                create_tag_competition.save()
            else:
                errors_list=[]
                for error in create_tag_competition.errors.as_data()['name']:
                    errors_list.append(error)
                messages.add_message(self.request, messages.WARNING,
                                        f'Competition Add New Tags ERROR:{errors_list}',
                                        )

        if request.POST['new_discussion_tags_name'] != '':
            if create_tag_discussion.is_valid():
                create_tag_discussion.save()
            else:
                errors_list=[]
                for error in create_tag_discussion.errors.as_data()['name']:
                    errors_list.append(error)
                messages.add_message(self.request, messages.WARNING,
                                        f'Discussion Add New Tags ERROR:{errors_list}',
                                        )

        if request.POST['new_notebook_tags_name'] != '':
            if create_tag_notebook.is_valid():
                create_tag_notebook.save()
            else:
                errors_list=[]
                for error in create_tag_notebook.errors.as_data()['name']:
                    errors_list.append(error)
                messages.add_message(self.request, messages.WARNING,
                                        f'Notebook Add New Tags ERROR:{errors_list}',
                                        )

        # UPDATE
        if discussion_formset.is_valid() and notebook_formset.is_valid():
            discussion_formset.save()
            notebook_formset.save()
            return super().post(request, *args, **kwargs)
        elif discussion_formset.is_valid():
            discussion_formset.save()
            messages.add_message(self.request, messages.WARNING,
                f'NotebookTags ERROR',
                )
            if competition_formset.is_valid():
                competition_formset.save()
            else:
                messages.add_message(self.request, messages.WARNING,
                                     f'CompetitionsTags ERROR',
                                     )
            return render(request, self.template_name, {
                          'formset': competition_formset,
                          'discussion_formset': discussion_formset,
                          'notebook_formset': notebook_formset,
                          'create_tag_competition':create_tag_competition,
                          })

        elif notebook_formset.is_valid():
            notebook_formset.save()
            messages.add_message(self.request, messages.WARNING,
                f'DiscussionTags ERROR',
                )
            if competition_formset.is_valid():
                competition_formset.save()
            else:
                messages.add_message(self.request, messages.WARNING,
                                     f'CompetitionsTags ERROR',
                                     )
            return render(request, self.template_name, {
                          'formset': competition_formset,
                          'discussion_formset': discussion_formset,
                          'notebook_formset': notebook_formset,
                          'create_tag_competition':create_tag_competition,
                          })

        else:
            messages.add_message(self.request, messages.WARNING,
                f'DiscussionTags ERROR',
                )
            messages.add_message(self.request, messages.WARNING,
                f'NotebookTags ERROR',
                )
            if competition_formset.is_valid():
                competition_formset.save()
            else:
                messages.add_message(self.request, messages.WARNING,
                                     f'CompetitionsTags ERROR',
                                     )
            return render(request, self.template_name, {
                          'formset': competition_formset,
                          'discussion_formset': discussion_formset,
                          'notebook_formset': notebook_formset,
                          'create_tag_competition':create_tag_competition,
                          })

    def formset_valid(self, formset):
        return super().formset_valid(formset)

    def formset_invalid(self, formset):
        messages.add_message(self.request, messages.WARNING,
                f'CompetitionsTags ERROR',
                )
        return super().formset_invalid(formset)


class CompetitionTagsDeleteView(LoginRequiredMixin, FormMixin, DeleteView):

    template_name = 'management/tags/tags_delete.html'
    model = CompetitionsTags
    form_class = DeleteTagForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
                'OBJECT_TYPE': 'Competition',
            })
        return context

    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        form = self.get_form()
        
        check_text = request.POST['check_text']

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
        return reverse_lazy('management:tags_list')


class DiscussionTagsDeleteView(LoginRequiredMixin, FormMixin, DeleteView):

    template_name = 'management/tags/tags_delete.html'
    model = DiscussionTags
    form_class = DeleteTagForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
                'OBJECT_TYPE': 'Discussion',
            })
        return context

    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        form = self.get_form()
        
        check_text = request.POST['check_text']

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
        return reverse_lazy('management:tags_list')


class NotebookTagsDeleteView(LoginRequiredMixin, FormMixin, DeleteView):

    template_name = 'management/tags/tags_delete.html'
    model = NotebookTags
    form_class = DeleteTagForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
                'OBJECT_TYPE': 'Notebook',
            })
        return context

    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        form = self.get_form()
        
        check_text = request.POST['check_text']

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
        return reverse_lazy('management:tags_list')