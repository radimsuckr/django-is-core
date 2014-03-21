from __future__ import unicode_literals

from class_based_auth_views.views import LoginView

from is_core.generic_views.auth_views import LogoutView
from is_core.auth_token import login, logout
from is_core.auth_token.forms import TokenAuthenticationForm


class TokenLoginView(LoginView):

    form_class = TokenAuthenticationForm

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        can check the test cookie stuff and log him in.
        """
        self.check_and_delete_test_cookie()
        login(self.request, form.get_user(), not form.is_permanent())
        return super(TokenLoginView, self).form_valid(form)


class TokenLogoutView(LogoutView):

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            logout(self.request)
        return super(LogoutView, self).get(*args, **kwargs)
