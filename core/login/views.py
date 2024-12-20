
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.translation import gettext, gettext_lazy as _
import config.settings


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Las credenciales no son correctas",
        'inactive': "Esta cuenta está inactiva",
    }


class LoginFormView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomAuthenticationForm
    success_url = reverse_lazy(config.settings.LOGIN_REDIRECT_URL)

    # sobreescribimos el método get_context_data para añadir info al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        return context

