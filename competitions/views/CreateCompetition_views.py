from django.conf import settings
from competitions.models import (
    Competitions,
)
from discussions_and_notebooks.models import (
    DiscussionThemes,
)
from django.views.generic.edit import (
    CreateView,
)
from competitions.forms import (
    CreateCompetitionForm,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from comments.Convert import (
    convert_comment,
)
from django.http import Http404

# Competitionの作成
class CompetitionCreateView(LoginRequiredMixin, CreateView):

    template_name = 'competitions/CreateCompetition/create_competition.html'
    model = Competitions
    form_class = CreateCompetitionForm
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return super().get(request, *args, **kwargs)
        else:
            raise Http404


    def form_valid(self, form):

        if self.request.user.is_superuser or self.request.user.is_staff:
            form.instance.create_user_id = self.request.user.id

            # convert text
            convert_text = convert_comment(form.instance.overview_text)
            form.instance.overview_text = convert_text
            convert_text = convert_comment(form.instance.evaluation_text)
            form.instance.evaluation_text = convert_text
            convert_text = convert_comment(form.instance.rule_text)
            form.instance.rule_text = convert_text
            convert_text = convert_comment(form.instance.data_text)
            form.instance.data_text = convert_text

            messages.add_message(self.request, messages.INFO,
                                f'Create!',)
            return super().form_valid(form)
        else:
            messages.add_message(self.request, messages.WARNING,
                                f'作成権限がありません',)
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # GETリクエストパラメータの取得
        redirect = self.request.GET.get('redirect')

        summernote_add_js = settings.SUMMERNOTE_CONFIG['js']
        summernote_add_css = settings.SUMMERNOTE_CONFIG['css']

        context.update({
                'redirect': redirect,
                # summernote_add_js and summernote_add_css
                'summernote_add_js': list(summernote_add_js),
                'summernote_add_css': list(summernote_add_css),
                # USE scrollspy
                'SCROLLSPY_TARGET': 'list-create-competition',
            })

        return context

    def get_success_url(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            if self.object.create_initial_discussion:
                DiscussionThemes.objects.create(post_user=self.request.user,
                                                post_competition_or_none=self.object,
                                                title='主催者への質問受付',
                                                text='このコンペティションに関してコンペティション主催者への質問はこちらに投稿ください',
                                                is_top=True,
                                                use_bot_icon=True,
                                                )
        return reverse_lazy('competitions:competition_detail', kwargs={'unique_competition_id': self.object.unique_competition_id})