from django import forms
from comments.models import (
    Comments,
)
from django_summernote.widgets import (
    SummernoteInplaceWidget,
)

# コメント投稿フォーム
class PostCommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ('text',)
        widgets = {'text': SummernoteInplaceWidget(),}