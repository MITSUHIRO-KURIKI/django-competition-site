from competitions.models.Competition_models import (
    CompetitionsTags,
)
from discussions_and_notebooks.models import (
    DiscussionTags, NotebookTags,
)
from django.forms import ModelForm
from django import forms


class CompetitionModelForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False

    class Meta:
        model = CompetitionsTags
        fields = ['name',]

    def add_prefix(self, field_name):
        field_name = {'name': 'new_competition_tags_name'}.get(field_name, field_name)
        return super().add_prefix(field_name)


class DiscussionModelForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False

    class Meta:
        model = DiscussionTags
        fields = ['name',]

    def add_prefix(self, field_name):
        field_name = {'name': 'new_discussion_tags_name'}.get(field_name, field_name)
        return super().add_prefix(field_name)


class NotebookModelForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False

    class Meta:
        model = NotebookTags
        fields = ['name',]
        
    def add_prefix(self, field_name):
        field_name = {'name': 'new_notebook_tags_name'}.get(field_name, field_name)
        return super().add_prefix(field_name)