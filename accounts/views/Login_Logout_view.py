from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from accounts.forms import (
  LogInForm, 
)


# ログイン
class LogInView(LoginView):
    
    authentication_form = LogInForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/LogIn_LogOut/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['USE_SOCIAL_LOGIN'] = settings.USE_SOCIAL_LOGIN
        return context

    def form_valid(self, form):
        # ログイン状態の保持機能
        login_remenber = form.cleaned_data['login_remenber']
        if login_remenber:
            self.request.session.set_expiry(60*60*24*5)
        return super().form_valid(form)

# ログアウト
class LogoutView(LogoutView):
    
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(self.request, messages.INFO,
                             f'Log out DONE',)
        return response