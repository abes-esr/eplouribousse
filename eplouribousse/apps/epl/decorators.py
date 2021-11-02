"""
Ici se trouvent les décorateurs que j'ai créés.
"""

from .models import *
from django.utils.translation import ugettext as _

#ce que j'ajoute :
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages

def edmode1(func):
    """
    Authentification requise si le mode consultation privée est activé.
    """
    def mod_func(request, bdd, lid, sort):
        suffixe = "@" + str(bdd)
        if Proj_setting.objects.using(bdd)[0].prv:
            if request.user.username and request.user.username[-3:] ==suffixe:
                return func(request, bdd, lid, sort)
            else:
                messages.info(request, _("Votre projet est en mode d'édition privé ; vous devez d'abord vous connecter."))
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            return func(request, bdd, lid, sort)

    return mod_func


def edmode2(func):
    """
    Authentification requise si le mode consultation privée est activé.
    """
    def mod_func(request, bdd, lid, xlid, sort):
        suffixe = "@" + str(bdd)
        if Proj_setting.objects.using(bdd)[0].prv:
            if request.user.username and request.user.username[-3:] ==suffixe:
                return func(request, bdd, lid, xlid, sort)
            else:
                messages.info(request, _("Votre projet est en mode d'édition privé ; vous devez d'abord vous connecter."))
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            return func(request, bdd, lid, xlid, sort)

    return mod_func


def edmode3(func):
    """
    Authentification requise si le mode consultation privée est activé.
    """
    def mod_func(request, bdd):
        suffixe = "@" + str(bdd)
        if Proj_setting.objects.using(bdd)[0].prv:
            if request.user.username and request.user.username[-3:] ==suffixe:
                return func(request, bdd)
            else:
                messages.info(request, _("Votre projet est en mode d'édition privé ; vous devez d'abord vous connecter."))
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            return func(request, bdd)

    return mod_func


def edmode4(func):
    """
    Authentification requise si le mode consultation privée est activé.
    """
    def mod_func(request, bdd, lid):
        suffixe = "@" + str(bdd)
        if Proj_setting.objects.using(bdd)[0].prv:
            if request.user.username and request.user.username[-3:] ==suffixe:
                return func(request, bdd, lid)
            else:
                messages.info(request, _("Votre projet est en mode d'édition privé ; vous devez d'abord vous connecter."))
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            return func(request, bdd, lid)

    return mod_func


def edmode5(func):
    """
    Authentification requise si le mode consultation privée est activé.
    """
    def mod_func(request, bdd, sid, lid):
        suffixe = "@" + str(bdd)
        if Proj_setting.objects.using(bdd)[0].prv:
            if request.user.username and request.user.username[-3:] ==suffixe:
                return func(request, bdd, sid, lid)
            else:
                messages.info(request, _("Votre projet est en mode d'édition privé ; vous devez d'abord vous connecter."))
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            return func(request, bdd, sid, lid)

    return mod_func


def edmode6(func):
    """
    Authentification requise si le mode consultation privée est activé.
    """
    def mod_func(request, bdd, coll_set):
        suffixe = "@" + str(bdd)
        if Proj_setting.objects.using(bdd)[0].prv:
            if request.user.username and request.user.username[-3:] ==suffixe:
                return func(request, bdd, coll_set)
            else:
                messages.info(request, _("Votre projet est en mode d'édition privé ; vous devez d'abord vous connecter."))
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            return func(request, bdd, coll_set)

    return mod_func


def edmode7(func):
    """
    Authentification requise si le mode consultation privée est activé.
    """
    def mod_func(request, bdd, lid, xlid, recset, what, length):
        suffixe = "@" + str(bdd)
        if Proj_setting.objects.using(bdd)[0].prv:
            if request.user.username and request.user.username[-3:] ==suffixe:
                return func(request, bdd, lid, xlid, recset, what, length)
            else:
                messages.info(request, _("Votre projet est en mode d'édition privé ; vous devez d'abord vous connecter."))
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            return func(request, bdd, lid, xlid, recset, what, length)

    return mod_func


def edmode8(func):
    """
    Authentification requise si le mode consultation privée est activé.
    """
    def mod_func(request, bdd, lid, xlid):
        suffixe = "@" + str(bdd)
        if Proj_setting.objects.using(bdd)[0].prv:
            if request.user.username and request.user.username[-3:] ==suffixe:
                return func(request, bdd, lid, xlid)
            else:
                messages.info(request, _("Votre projet est en mode d'édition privé ; vous devez d'abord vous connecter."))
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            return func(request, bdd, lid, xlid)

    return mod_func
