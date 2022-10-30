from django import forms
from competitions.models import (
    Competitions,
)
from django_summernote.widgets import (
    SummernoteInplaceWidget,
)
from django.forms import SplitDateTimeField
from django.contrib.admin.widgets import AdminSplitDateTime


# コンペティションの作成
class CreateCompetitionForm(forms.ModelForm):

    date_open = SplitDateTimeField(widget=AdminSplitDateTime())
    date_close = SplitDateTimeField(widget=AdminSplitDateTime())

    class Meta:
        model = Competitions
        fields = ('unique_competition_id',
                  'overall',
                  'title',
                  'subtitle',
                  'tags',
                  'overview_text',
                  'evaluation_text',
                  'metrics',
                  'Evaluation_Minimize',
                  'rule_text',
                  'data_text',
                  'data_file',
                  'answer_file',
                  'target_cols_name',
                  'Submission_Daily_Limit',
                  'Final_Evaluation_Limit',
                  'is_public',
                  'date_open',
                  'date_close',
                  'create_initial_discussion',
                  )
        widgets = {#'date_open': AdminSplitDateTime(),
                   #'date_close': AdminSplitDateTime(),
                   'overview_text': SummernoteInplaceWidget(),
                   'evaluation_text': SummernoteInplaceWidget(),
                   'rule_text': SummernoteInplaceWidget(),
                   'data_text': SummernoteInplaceWidget(),
                   }



