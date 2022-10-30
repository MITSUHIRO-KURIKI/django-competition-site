from django import forms


# コメントの削除
class DeleteCommentForm(forms.Form):
    check_text = forms.CharField(label="確認",
                                 help_text='削除するには「delete」と入力してボタンを押してください')