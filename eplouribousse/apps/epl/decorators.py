"""
Ici se trouvent les décorateurs que j'ai créés.
"""

from django.shortcuts import render

from .models import *

from .forms import *

from django.core.mail import send_mail

from django.db.models.functions import Now

from django.utils.translation import ugettext as _

from django.contrib.auth.models import User

from django.contrib.auth import logout
# , login, authenticate

from django.http import HttpResponseRedirect, HttpResponse
import os

from django.contrib import messages

#ce que j'ajoute :
from django.contrib.auth.decorators import login_required
# from .views import *

def edmode(func):
    """
    Authentification requise si le mode consultation privée est activé.
    """
    def mod_func(request, bdd, lid, sort):
        suffixe = "@" + str(bdd)
        if request.user.username and request.user.username[-3:] ==suffixe:
            return HttpResponse("kjgamg")
        else:
            @login_required
            def my_view(request):
                return func(request, bdd, lid, sort)
            return my_view
            # return HttpResponseRedirect('/account/login')
            # return HttpResponse(_("us is empty"))
    return mod_func
