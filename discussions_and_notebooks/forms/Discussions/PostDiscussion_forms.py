from django import forms
from discussions_and_notebooks.models import (
    DiscussionThemes, 
)
from django_summernote.widgets import (
    SummernoteInplaceWidget,
)

# コメント投稿フォーム
class PostDiscussionForm(forms.ModelForm):

    class Meta:
        model = DiscussionThemes
        fields = ('title','text','tags_or_none','is_top','use_bot_icon')
        widgets = {'text': SummernoteInplaceWidget(),}