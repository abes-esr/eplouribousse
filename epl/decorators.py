"""
Ici se trouvent les décorateurs que j'ai créés.
"""

from .models import *
from .proj_models import *
from django.utils.translation import ugettext as _

#ce que j'ajoute :
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages

import os.path
from django.http import HttpResponseRedirect

def edmode1(func):
    """
    Authentification requise si le mode consultation privée est activé.
    """
    def mod_func(request, bdd, lid, sort):
        """
        Vérification de l'existence du projet (crucial) :
        """
        if os.path.isfile("{}.db".format(bdd)):
            a =1 # just to continue
        else:
            messages.info(request, _("Veuillez choisir parmi les projets disponibles."))
            return HttpResponseRedirect(".")
        """
        fin de la vérification
        """
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
        """
        Vérification de l'existence du projet (crucial) :
        """
        if os.path.isfile("{}.db".format(bdd)):
            a =1 # just to continue
        else:
            messages.info(request, _("Veuillez choisir parmi les projets disponibles."))
            return HttpResponseRedirect(".")
        """
        fin de la vérification
        """
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
        """
        Vérification de l'existence du projet (crucial) :
        """
        if os.path.isfile("{}.db".format(bdd)):
            a =1 # just to continue
        else:
            messages.info(request, _("Veuillez choisir parmi les projets disponibles."))
            return HttpResponseRedirect(".")
        """
        fin de la vérification
        """
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
        """
        Vérification de l'existence du projet (crucial) :
        """
        if os.path.isfile("{}.db".format(bdd)):
            a =1 # just to continue
        else:
            messages.info(request, _("Veuillez choisir parmi les projets disponibles."))
            return HttpResponseRedirect(".")
        """
        fin de la vérification
        """
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
        """
        Vérification de l'existence du projet (crucial) :
        """
        if os.path.isfile("{}.db".format(bdd)):
            a =1 # just to continue
        else:
            messages.info(request, _("Veuillez choisir parmi les projets disponibles."))
            return HttpResponseRedirect(".")
        """
        fin de la vérification
        """
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
        """
        Vérification de l'existence du projet (crucial) :
        """
        if os.path.isfile("{}.db".format(bdd)):
            a =1 # just to continue
        else:
            messages.info(request, _("Veuillez choisir parmi les projets disponibles."))
            return HttpResponseRedirect(".")
        """
        fin de la vérification
        """
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
        """
        Vérification de l'existence du projet (crucial) :
        """
        if os.path.isfile("{}.db".format(bdd)):
            a =1 # just to continue
        else:
            messages.info(request, _("Veuillez choisir parmi les projets disponibles."))
            return HttpResponseRedirect(".")
        """
        fin de la vérification
        """
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
        """
        Vérification de l'existence du projet (crucial) :
        """
        if os.path.isfile("{}.db".format(bdd)):
            a =1 # just to continue
        else:
            messages.info(request, _("Veuillez choisir parmi les projets disponibles."))
            return HttpResponseRedirect(".")
        """
        fin de la vérification
        """
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


def edmode9(func):
    """
    Authentification requise si le mode consultation privée est activé.
    """
    def mod_func(request, bdd, lid, xlid, recset, sort):
        """
        Vérification de l'existence du projet (crucial) :
        """
        if os.path.isfile("{}.db".format(bdd)):
            a =1 # just to continue
        else:
            messages.info(request, _("Veuillez choisir parmi les projets disponibles."))
            return HttpResponseRedirect(".")
        """
        fin de la vérification
        """
        suffixe = "@" + str(bdd)
        if Proj_setting.objects.using(bdd)[0].prv:
            if request.user.username and request.user.username[-3:] ==suffixe:
                return func(request, bdd, lid, xlid, recset, sort)
            else:
                messages.info(request, _("Votre projet est en mode d'édition privé ; vous devez d'abord vous connecter."))
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            return func(request, bdd, lid, xlid, recset, sort)

    return mod_func
