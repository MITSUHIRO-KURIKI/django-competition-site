from django.conf import settings
from django.contrib.auth import login
from django.views.generic import CreateView
from accounts.models import (
    UserActivateTokens, 
)
from accounts.forms import (
    SignUpForm,
)
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from urllib import request
if settings.USE_RECAPTCHA:
    from common_scripts import (
        grecaptcha_request,
    )

# サインアップ
class SignUpView(CreateView):
    
    form_class = SignUpForm
    # メール認証する場合としない場合のサインアップ後のページ遷移の分岐
    if settings.USE_EMAIL_CERTIFICATION:
        success_url = reverse_lazy('accounts:temp_active_user')
    else:
        success_url = reverse_lazy('home')
    template_name = 'accounts/SignUp/signup.html'

    # reCaptcha_token の検証
    def post(self, request, *args, **kwargs):
        if settings.USE_RECAPTCHA:
            recaptcha_token = self.request.POST.get('g-recaptcha-response')
            if recaptcha_token is None or recaptcha_token == '':
                messages.add_message(self.request, messages.WARNING,
                                    f'不正なPOSTです - reCaptcha ERROR',
                                    )
                return redirect('accounts:signup')
            else:
                res = grecaptcha_request(recaptcha_token)
                if res:
                    return super().post(request, *args, **kwargs) # SUCCESS
                else:
                    messages.add_message(self.request, messages.WARNING,
                                    f'不正なPOSTです - reCaptcha ERROR',
                                    )
                    return redirect('accounts:signup')
        else:
            return super().post(request, *args, **kwargs) # SUCCESS

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['USE_SOCIAL_LOGIN'] = settings.USE_SOCIAL_LOGIN
        context['USE_RECAPTCHA'] = settings.USE_RECAPTCHA
        if settings.USE_RECAPTCHA:
            context['RECAPTCHA_PUBLIC_KEY'] = settings.RECAPTCHA_PUBLIC_KEY
        
        return context

    def form_valid(self, form):
        # self.object に save() されたユーザーオブジェクトが格納される
        valid = super().form_valid(form)
        # ADD social-auth-app-django Required 'backend='
        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')
        if settings.USE_EMAIL_CERTIFICATION is False:
            messages.add_message(self.request, messages.INFO,
                                f'Registration completed',
                                )
        return valid

def ActivateUserView(request, token):
    token_res = UserActivateTokens.objects.activate_user_by_token(token)
    messages.add_message(request, messages.INFO,
                         f'Registration completed')
    return redirect('home')