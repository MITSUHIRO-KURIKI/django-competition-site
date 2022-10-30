from django.conf import settings
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    UpdateView,
)
from user_settings.models import (
    CustomUserMailSettings, CustomUserProfilePublicSettings, 
)



# ユーザ登録情報の編集
class UserSettingsEmailEditView(LoginRequiredMixin, UpdateView):

    model = CustomUserMailSettings
    template_name = 'user_settings/Edit/user_settings_email_edit.html'
    if settings.USE_EMAIL_NOTIFICATION:
        fields = ['email_receipt_permission_all',
                  'email_receipt_permission_important_notice',
                  'email_receipt_user_competition_notice',
                  'email_receipt_user_discussion_comment_notice',
                  'email_receipt_user_notebook_comment_notice',
                  ]
    else:
        fields = ['email_receipt_permission_all',
                  'email_receipt_permission_important_notice',
                  ]
    
    success_url = reverse_lazy('accounts:user_settings:user_settings_email_edit')

    def get_object(self):
        return self.model.objects.get(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'USE_EMAIL_NOTIFICATION': settings.USE_EMAIL_NOTIFICATION,
            'custom_user_settings': get_object_or_404(self.model, user_id__id=self.request.user.id),
        })
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO,
                             f'Update Done',
                             )
        return super().form_valid(form)


class UserSettingsProfileEditView(LoginRequiredMixin, UpdateView):

    model = CustomUserProfilePublicSettings
    template_name = 'user_settings/Edit/user_settings_profile_edit.html'
    fields = ['user_profile_is_authenticated_only',
              'user_profile_is_all_public',
              'search_robot_public',
            #   'username_public',
              'comment_public',
            #   'user_icon_public',
              'locate_public',
              'birth_day_public',
              'gender_public',
              'sns_id_public',
              ]

    success_url = reverse_lazy('accounts:user_settings:user_settings_profile_edit')

    def get_object(self):
        return self.model.objects.get(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'custom_user_settings': get_object_or_404(self.model, user_id__id=self.request.user.id),
        })
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO,
                             f'Update Done',
                             )
        return super().form_valid(form)