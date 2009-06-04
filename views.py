from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import render_to_response
from django import forms
from django.utils.translation import ugettext_lazy as _

from django.template import RequestContext
from meteora import Meteora

class MeteoraAuthenticationForm(AuthenticationForm):
    def __init__(self,request = None, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'required'
        self.fields['password'].widget.attrs['class'] = 'required'
        


def login(request, template_name='meteora/login.html', redirect_field_name=REDIRECT_FIELD_NAME):
    "Displays the login form and handles the login action."
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if request.method == "POST":
        form = MeteoraAuthenticationForm(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            from django.contrib.auth import login
            login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            m = Meteora()
            m.redirecTo(redirect_to)
            return m.json_response()
        else:
            m = Meteora(False, _("Invalid Form"))
            m.form_invalid("table-login",form)
            return m.json_response()
    else:
        form = MeteoraAuthenticationForm(request)
    request.session.set_test_cookie()
    return render_to_response(template_name, {
        'form': form,
        redirect_field_name: redirect_to
    }, context_instance=RequestContext(request))
login = never_cache(login)