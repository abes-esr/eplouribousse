epl_version ="v2.11.114 (Judith)"
date_version ="May 02, 2024"
# Mise au niveau de :
#epl_version ="v2.11.115 (~Irmingard)"
#date_version ="May 02, 2024"


from django.shortcuts import render, redirect

from .models import *

from .proj_models import *

from .forms import *

from django.core.mail import send_mail, BadHeaderError, EmailMessage

from django.db.models.functions import Now

from django.contrib.auth.decorators import login_required

from django.utils.translation import ugettext as _

from django.contrib.auth.models import User

from django.contrib.auth import logout

from django.http import HttpResponseRedirect, HttpResponse
import os

from django.contrib import messages

from .decorators import *

from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from django.utils.encoding import iri_to_uri
from urllib.parse import quote

## Following is for graphics (made blinffolded from : https://youtu.be/jrT6NiM46jk amended with https://medium.com/@mdhv.kothari99/matplotlib-into-django-template-5def2e159997 for working)
import matplotlib.pyplot as plt
import numpy as np
import urllib, base64
from io import BytesIO
from matplotlib.ticker import MaxNLocator

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format ='png')
    buffer.seek(0)
    image_png =buffer.getvalue()
    graph = urllib.parse.quote(base64.b64encode(image_png))
    buffer.close()
    return graph

def get_plot(x, y, titre, absc, ordo):
    plt.switch_backend('AGG')
    plt.figure(figsize=(3, 3))
    plt.plot(x, y, color ="red")
    plt.xticks(rotation=45)
    plt.ymin(0)
    plt.title(titre)
    plt.xlabel(absc)
    plt.ylabel(ordo)
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_scatter(x, y, titre, absc, ordo):
    plt.switch_backend('AGG')
    plt.figure(figsize=(8, 5))
    plt.scatter(x, y, color ="red")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.title(titre)
    plt.xlabel(absc)
    plt.ylabel(ordo)
    plt.tight_layout()
    graph = get_graph()
    return graph

def multipleplot(x, y1, y3, y13, titre1, titre3, titre13, absc, ordo, titre):
    # Note that even in the OO-style, we use `.pyplot.figure` to create the Figure.
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(x, y1, label=titre1)  # Plot some data on the axes.
    ax.scatter(x, y3, label=titre3)  # Plot more data on the axes...
    ax.scatter(x, y13, label=titre13)  # ... and some more.
    ax.set_xlabel(absc)  # Add an x-label to the axes.
    ax.set_ylabel(ordo)  # Add a y-label to the axes.
    ax.set_title(titre)  # Add a title to the axes.
    ax.legend()  # Add a legend.
    ax.grid(True)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    graph = get_graph()
    return graph

def get_pie(x, titre, **kwargs):
    plt.switch_backend('AGG')
    plt.figure(figsize=(8, 5))
    plt.pie(x, autopct='%1.1f%%')
    plt.legend(fontsize = 'small', bbox_to_anchor=(1, 0, 0.5, 1), **kwargs)
    plt.title(titre)
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_bar(x, y, titre, **kwargs):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 2))
    plt.bar(x, y, 2, **kwargs)
    plt.title(titre)
    plt.tight_layout()
    graph = get_graph()
    return graph
# end of stuff for graphics 


import random
alphalist = [_("zéro"), _("un"), _("deux"), _("trois"), _("cinq"), _("six"), _("huit"), _("treize"), _("vingt-et-un"), _("vingt-quatre"), _("vingt-huit"), _("trente-quatre"), _("cinquante-cinq"), _("quatre-vingt-neuf"), _("cent-vingt"), _("cent-quarante-quatre"), _("deux-cent-trente-trois"), _("trois-cent-soixante-dix-sept"), _("quatre-cent-quatre-vingt-seize"), _("six-cent-dix"), _("sept-cent-vingt"), _("neuf-cent-quatre-vingt-sept"), _("neuf-cent-quatre-vingt-dix-neuf")]
numberlist = ["0", "1", "2", "3", "5", "6", "8", "13", "21", "24", "28", "34", "55", "89", "120", "144", "233", "377", "496", "610", "720", "987", "999"]
# bornes (0 et 999) + nombres de Fibonacci + nombres parfaits + factorielles d'entiers

lastrked =None
webmaster =ReplyMail.objects.all().order_by('pk')[1].sendermail
replymail =ReplyMail.objects.all().order_by('pk')[0].sendermail # = no-reply mail

def serial_title(e):
    """sorting by title"""
    return e.title
def serial_id(e):
    """sorting by sid"""
    return e.sid
def coll_cn(e):
    """sorting by cn, title"""
    return (e.cn, e.title)

############################################

def user_suppr(request, bdd, login):
    """Mail d'info lors de la suppression d'un compte"""
    host = str(request.get_host())
    subject = _("eplouribousse (Projet : ") + Project.objects.using(bdd).all().order_by('pk')[0].name + \
    ")" + _(" > Suppression d'un compte")
    message = _("Le compte {} à été fermé".format(login)) + \
    "\n" + _("Cela peut faire suite à un changement du compte ou à son inutilité ou encore à une demande de suppression pure et simple.") \
    + " " + _("Votre email a été supprimé de la liste de diffusion.") \
    + "\n" + _("Si vous pensez qu'il s'agit d'une erreur, veuillez contacter le responsable de projet concerné :") + "\n" + \
    "http://" + host + "/" + bdd + "/projectmaster" + "\n" + "\n" + _("Merci d'utiliser eplouribousse !")
    dest =[User.objects.get(username =login).email]
    send_mail(subject, message, replymail, dest, fail_silently=True, )

def usermail_mod(request, bdd, login, mail):
    """Mail d'info lors de la modification d'un compte (email)"""
    host = str(request.get_host())
    subject = _("eplouribousse (Projet : ") + Project.objects.using(bdd).all().order_by('pk')[0].name + \
    ")" + _(" > Modification de votre email")
    message = _("L'adresse mail associée à l'identifiant {} à été modifiée et la liste de diffusion a été mise à jour.".format(login)) + "\n" + \
    _("(Vous recevez le présent message à votre nouvelle adresse.)") + "\n" + "\n" + _("Merci d'utiliser eplouribousse !")
    dest =[mail]
    send_mail(subject, message, replymail, dest, fail_silently=True, )

def userid_mod(request, bdd, login, mail):
    """Mail d'info lors de la modification d'un compte (identifiant)"""
    host = str(request.get_host())
    subject = _("eplouribousse (Projet : ") + Project.objects.using(bdd).all().order_by('pk')[0].name + \
    ")" + _(" > Modification de votre identifiant")
    message = _("L'identifiant associé à l'adresse {} à été modifié.".format(mail)) + "\n" + \
    _("Votre nouvel identifiant est : {}.".format(login)) + "\n" + _("(Votre mot de passe reste inchangé)") + "\n" + "\n" + \
    _("Si vous pensez qu'il s'agit d'une erreur, veuillez contacter le responsable de projet concerné :") + "\n" + \
    "http://" + host + "/" + bdd + "/projectmaster" + "\n" + "\n" + _("Merci d'utiliser eplouribousse !")
    dest =[User.objects.get(username =login).email]
    send_mail(subject, message, replymail, dest, fail_silently=True, )

def diffajupdate(request, bdd, mel):
    prj = Project.objects.using(bdd).all().order_by('pk')[0]
    list_diff =prj.descr.split(", ")
    if mel not in list_diff:
        list_diff.append(mel)
    list_diff.sort()
    prj.descr =""
    for elmt in list_diff:
        if elmt:
            prj.descr += elmt + ", "
    prj.save(using =bdd)

def diffsupupdate(request, bdd, mel):
    prj = Project.objects.using(bdd).all().order_by('pk')[0]
    list_diff =prj.descr.split(", ")
    if mel in list_diff:
        list_diff.remove(mel)
    prj.descr =""
    for elmt in list_diff:
        if elmt:
            prj.descr += elmt + ", "
    prj.save(using =bdd)

def newestfeat(request, bdd, libname, feature):
    try:
        newestfeature = Feature.objects.using(bdd).get(libname = libname)
        newestfeature.feaname = feature
        newestfeature.save(using=bdd)
    except:
        newestfeature =Feature(libname =libname, feaname =feature)
        newestfeature.save(using=bdd)

def xnewestfeat(request, bdd, libname, feature, xlid):
    try:
        newestfeature = Feature.objects.using(bdd).get(libname = libname)
        newestfeature.feaname = feature + "$" + str(xlid)
        newestfeature.save(using=bdd)
    except:
        fea =feature + "$" + str(xlid)
        newestfeature =Feature(libname =libname, feaname =fea)
        newestfeature.save(using=bdd)
############################################


def selectbdd(request):

    k =logstatus(request)
    version =epl_version
    
    BDD_CHOICES =('',_('Sélectionnez votre projet')),
    
#########################(Cette partie est reproduite de la même vue dans 'home' et 'globadm')######################
    """
    Création (dans la base de données principale) des users non encore enregistrés pour toutes les bases projets !
    """
    for i in [n for n in range(100)]:
        if os.path.isfile('{:02d}.db'.format(i)):
            for j in Utilisateur.objects.using('{:02d}'.format(i)).all():
                try:
                    usr =User.objects.get(username =j.username)
                except:
                    nwuser =User(is_superuser =0, username =j.username, email =j.mail, is_staff =0, is_active =1)
                    nwuser.save()
            try:
                p = Project.objects.using('{:02d}'.format(i)).all().order_by('pk')[0].name
                BDD_CHOICES += ('{:02d}'.format(i), '{:02d}'.format(i) + " - " + p),
            except:
                pass
####################################################(fin)###########################################################
  
    if request.user.is_authenticated:
        try:
            suffix =request.user.username[-3:]
            if suffix[0] =="@":
                db =suffix[1:3]
                u_name =Utilisateur.objects.using(db).get(username =request.user.username)
                return home(request, db)
        except:
            a =1

    if len(BDD_CHOICES) ==2:
        return HttpResponseRedirect(BDD_CHOICES[1][0])
        # return home(request, BDD_CHOICES[1][0])
    else:
        class BddSel_Form(forms.Form):
            bddname = forms.ChoiceField(required = True, widget=forms.Select, choices=BDD_CHOICES)

        f = BddSel_Form(request.POST or None)

        if f.is_valid():
            bdd = f.cleaned_data['bddname']
            return HttpResponseRedirect(bdd)
            # return home(request, bdd)

    #abstract :
    librnbr =0
    itemrecnbr =0
    instrnbr =0
    usernbr =len(User.objects.all())
    projnbr =len(BDD_CHOICES) -1
    totcand =0
    for bdd in BDD_CHOICES[1:]:
        librnbr +=len(Library.objects.using(bdd[0]).all())

    librnbr =librnbr - projnbr #checkers are not libraries ! (one checker per project)

    return render(request, 'epl/selectbdd.html', locals())


def logstatus(request):
    if request.user.is_authenticated:
        k = request.user.get_username()
    else:
        k =0
    return k

@edmode3
def home(request, bdd):

    "Homepage"

    k =logstatus(request)
    version =epl_version
    asanemptychain ="~"
    
    """
    Suppression (dans la base de données du projet et dans la bdd centrale) des utilisateurs "inutiles"
    """
    
    """
        Suppression dans la base de données du projet : "
    """
    
    u_list =[]
    for u_libmt in Library.objects.using(bdd).all():
        if u_libmt.contact not in u_list:
            u_list.append(u_libmt.contact)
        if u_libmt.contact_bis not in u_list:
            u_list.append(u_libmt.contact_bis)
        if u_libmt.contact_ter not in u_list:
            u_list.append(u_libmt.contact_ter)
    for adm_lmt in BddAdmin.objects.using(bdd).all():
        if adm_lmt.contact not in u_list:
            u_list.append(adm_lmt.contact)
    for ulmt in Utilisateur.objects.using(bdd).all():
        if ulmt.mail not in u_list and Proj_setting.objects.using(bdd)[0].prv ==0:
            ulmt.delete(using =bdd)
            if not User.objects.get(username =ulmt.username).is_superuser:
                User.objects.get(username =ulmt.username).delete()
                
    """
        Suppression dans la base de données centrale : "
    """
    for j in User.objects.all():
        if j.username[-2:] ==bdd and not Utilisateur.objects.using(bdd).filter(username =j.username):
            if not User.objects.get(username =j.username).is_superuser:
                j.delete()
                
            
#########################(Cette partie est reproduite dans les vues 'selectbdd' et 'globadm')#######################
    """Création (dans la base de données principale) des users non encore enregistrés pour toutes les bases projets
    et non seulement pour celle considérée dans la présente vue !"""
    for i in [n for n in range(100)]:
        if os.path.isfile('{:02d}.db'.format(i)):
            for j in Utilisateur.objects.using('{:02d}'.format(i)).all():
                try:
                    usr =User.objects.get(username =j.username)
                except:
                    nwuser =User(is_superuser =0, username =j.username, email =j.mail, is_staff =0, is_active =1)
                    nwuser.save()
####################################################(fin)###########################################################

    project = Project.objects.using(bdd).all().order_by('pk')[0].name
    to = Project.objects.using(bdd).all().order_by('pk')[0].descr.split(", ")

    LIBRARY_CHOICES = ('', 'Choisissez votre bibliothèque'),('checker','checker'),
    if Library.objects.using(bdd).all().exclude(name ='checker'):
        for l in Library.objects.using(bdd).all().exclude(name ='checker').order_by('name'):
            LIBRARY_CHOICES += (l.name, l.name),

    class FeatureForm(forms.ModelForm):
        class Meta:
            model = Feature
            fields = ('libname', 'feaname',)
            widgets = {
                'libname' : forms.Select(choices=LIBRARY_CHOICES),
                'feaname' : forms.RadioSelect(choices=FEATURE_CHOICES),
            }

    #Feature input :
    i = Feature()

    form = FeatureForm(request.POST, instance =i)

    if form.is_valid():
        lid = Library.objects.using(bdd).get(name =i.libname).lid
        feature =i.feaname
        libname =i.libname
        newestfeat(request, bdd, libname, feature)

        if lid =="999999999":
            if feature =='30':
                return instrtodo(request, bdd, lid, 'title')
            else:
                return checkinstr(request, bdd)
        else:
            if feature =='10':
                return ranktotake(request, bdd, lid, 'title')
            elif feature =='20':
                return arbitration(request, bdd, lid, 'title')
            elif feature =='30':
                return instrtodo(request, bdd, lid, 'title')
            elif feature =='40':
                return tobeedited(request, bdd, lid, 'title')
            elif feature =='70':
                return listall(request, bdd, lid, 'status')

    #abstract :
    usernbr =len(Utilisateur.objects.using(bdd).all())
    librnbr =len(Library.objects.using(bdd).all()) -1  #checkers are not libraries ! (one checker per project)
    itemrecnbr =len(ItemRecord.objects.using(bdd).all())
    cand =[]
    for e in ItemRecord.objects.using(bdd).all():
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid)) >1 and not e.sid in cand:
            cand.append(e.sid)
    totcand =len(cand)

    return render(request, 'epl/home.html', locals())

@login_required
def adminbase(request, bdd):

    #contrôle d'accès ici
    suffixe = "@" + str(bdd)
    if not request.user.username[-3:] ==suffixe:
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)
    if not len(BddAdmin.objects.using(bdd).filter(contact =request.user.email)):
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)

    k =logstatus(request)
    version =epl_version
    url ="/" + bdd + "/adminbase"
    private =Proj_setting.objects.using(bdd)[0].prv
    
    # gestion des fiches erronnées
    faulty_list =ItemRecord.objects.using(bdd).filter(rank =1, status =6)
    faulty =len(faulty_list)

    # gestion des alertes (début)
    current_alerts =[] #initialzing
    if Proj_setting.objects.using(bdd)[0].rkg:
        current_alerts.append(_("positionnement"))
    if Proj_setting.objects.using(bdd)[0].arb:
        current_alerts.append(_("arbitrages"))
    if Proj_setting.objects.using(bdd)[0].ins:
        current_alerts.append(_("instructions"))
    if Proj_setting.objects.using(bdd)[0].edi:
        current_alerts.append(_("résultantes"))
    if len(current_alerts):
        al =1
    else:
        al =0
    if Proj_setting.objects.using(bdd)[0].prv:
        priv_mode = _("activé")
    else:
        priv_mode = _("désactivé")
    # gestion des alertes (fin)

    EXCLUSION_CHOICES = ('', ''),
    for e in Exclusion.objects.using(bdd).all().order_by('label'):
        EXCLUSION_CHOICES += (e.label, e.label),
    EXCLUSION_CHOICES += ("Autre (Commenter)", _("Autre (Commenter)")),
    exclnbr =len(EXCLUSION_CHOICES) -1
    project = Project.objects.using(bdd).all().order_by('pk')[0].name
    list_diff =Project.objects.using(bdd).all().order_by('pk')[0].descr.split(", ")
    list_diff.sort()
    extractdate =Project.objects.using(bdd).all().order_by('pk')[0].date

    #Stuff about libraries
    LIBRARY_CHOICES = ('', _('Sélectionnez la bibliothèque')), ('checker', 'checker'),
    if Library.objects.using(bdd).all().exclude(name ='checker'):
        for l in Library.objects.using(bdd).all().exclude(name ='checker').order_by('name'):
            LIBRARY_CHOICES += (l.name, l.name),

    liblist =Library.objects.using(bdd).exclude(name ='checker')
    sizelib =len(liblist)
    try:
        bis = Utilisateur.objects.using(bdd).get(mail =Library.objects.using(bdd).get(name ='checker').contact_bis)
    except:
        bis =None
    try:
        ter = Utilisateur.objects.using(bdd).get(mail =Library.objects.using(bdd).get(name ='checker').contact_ter)
    except:
        ter =None

    libtuple =(Library.objects.using(bdd).get(name ='checker'), Utilisateur.objects.using(bdd).get(mail =Library.objects.using(bdd).get(name ='checker').contact), bis, ter),
    for libelmt in liblist:
        try:
            bis = Utilisateur.objects.using(bdd).get(mail =Library.objects.using(bdd).get(name =libelmt.name).contact_bis)
        except:
            bis =None
        try:
            ter = Utilisateur.objects.using(bdd).get(mail =Library.objects.using(bdd).get(name =libelmt.name).contact_ter)
        except:
            ter =None
        libtuple +=(Library.objects.using(bdd).get(name =libelmt.name), Utilisateur.objects.using(bdd).get(mail =Library.objects.using(bdd).get(name =libelmt.name).contact), bis, ter),

    #Stuff about bddadministrators
    admintuple =('', "Sélectionnez l'administrateur"),
    for b in BddAdmin.objects.using(bdd).all():
        admintuple +=(b.contact, Utilisateur.objects.using(bdd).get(mail =BddAdmin.objects.using(bdd).get(contact =b.contact).contact)),
    admintup =admintuple[1:]
    sizeadm =len(BddAdmin.objects.using(bdd).all())

    #Stuff about instructors :
    sizeuters =len(Utilisateur.objects.using(bdd).all())

    #Début stuff about other authorized users
    otherauthtuple =('', "Sélectionnez l'utilisateur"),
    ft =0

    for elmt in Utilisateur.objects.using(bdd).all():
        if not BddAdmin.objects.using(bdd).filter(contact =elmt.mail) and not \
        Library.objects.using(bdd).filter(contact =elmt.mail) and not \
        Library.objects.using(bdd).filter(contact_bis =elmt.mail) and not \
        Library.objects.using(bdd).filter(contact_ter =elmt.mail):
            if elmt.username[-3:] ==suffixe:
                otherauthtuple +=(elmt.mail, Utilisateur.objects.using(bdd).get(mail =elmt.mail)),
                ft +=1
    sizeotherus =ft
    otherauthtup =otherauthtuple[1:]
    
    # Suppression des utilisateurs orphelins (n'ayant plus aucun rôle) quand le projet est en mode public (début) :
    if not private:
        mailist =[]
        for lib in Library.objects.using(bdd).all():
            if lib.contact not in mailist:
                mailist.append(lib.contact)
            if lib.contact_bis and lib.contact_bis not in mailist:
                mailist.append(lib.contact_bis)
            if lib.contact_ter and lib.contact_ter not in mailist:
                mailist.append(lib.contact_ter)
        for adm in BddAdmin.objects.using(bdd).all():
            if adm.contact not in mailist:
                mailist.append(adm.contact)
        for utmt in Utilisateur.objects.using(bdd).all():
            if utmt.mail not in mailist:
                user_suppr(request, bdd, utmt.username)
                diffsupupdate(request, bdd, utmt.mail)
                messages.info(request, _("Le compte {} a été supprimé et la liste de diffusion mise à jour en conséquence.".format(utmt.username)))
                messages.info(request, _("L'utilisateur {} n'avait plus aucun rôle dans le projet.".format(utmt.username)))
                utmt.delete(using =bdd)
                User.objects.get(username =utmt.username).delete()
    # Suppression des utilisateurs orphelins (n'ayant plus aucun rôle) quand le projet est en mode public (fin) :

    return render(request, 'epl/adminbase.html', locals())


@login_required
def excl_adm(request, bdd):

    #contrôle d'accès ici
    suffixe = "@" + str(bdd)
    if not request.user.username[-3:] ==suffixe:
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)
    if not len(BddAdmin.objects.using(bdd).filter(contact =request.user.email)):
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)

    k =logstatus(request)
    version =epl_version
    url ="/" + bdd + "/adminbase"
    private =Proj_setting.objects.using(bdd)[0].prv


    EXCLUSION_CHOICES = ('', ''),
    for e in Exclusion.objects.using(bdd).all().order_by('label'):
        EXCLUSION_CHOICES += (e.label, e.label),
    EXCLUSION_CHOICES += ("Autre (Commenter)", _("Autre (Commenter)")),
    exclnbr =len(EXCLUSION_CHOICES) -1
    project = Project.objects.using(bdd).all().order_by('pk')[0].name

    #Stuff about exclusions
    class ExcluForm(forms.Form):
        exclusup = forms.CharField(required =True, widget=forms.TextInput(attrs={'size': '30'}), max_length=30, label =_("exclusion suppl"))
    exclform =ExcluForm(request.POST or None)
    class ExcluSupprForm(forms.Form):
        exclreason = forms.ChoiceField(required = True, widget=forms.Select, choices=EXCLUSION_CHOICES[:-1], label =_("Motif d'exclusion à supprimer"))
        exclmod = forms.CharField(required =False, widget=forms.TextInput(attrs={'size': '30'}), max_length=30, label =_("exclusion modifiée"))
        suppr = forms.BooleanField(required=False)
    exclsupprform =ExcluSupprForm(request.POST or None)

    if exclform.is_valid():
        try:
            op =Exclusion.objects.using(bdd).get(label =exclform.cleaned_data['exclusup'])
            messages.info(request, _('Cette exclusion existe déjà'))
            # return HttpResponseRedirect(url)
        except:
            newexcl =Exclusion()
            newexcl.label =exclform.cleaned_data['exclusup']
            newexcl.save(using =bdd)
            messages.info(request, _('Exclusion ajoutée avec succès'))
            # return HttpResponseRedirect(url)
    if exclsupprform.is_valid():
        op =Exclusion.objects.using(bdd).get(label =exclsupprform.cleaned_data['exclreason'])
        if exclsupprform.cleaned_data['suppr'] ==True:
            if len(ItemRecord.objects.using(bdd).filter(excl =exclsupprform.cleaned_data['exclreason'])):
                messages.info(request, _('Suppression impossible : Cete exclusion a déjà servi (vous pouvez éventuellement modifier son intitulé)'))
            else:
                op.delete(using =bdd)
                messages.info(request, _('Exclusion supprimée avec succès'))
        else:
            try:
                xc =Exclusion.objects.using(bdd).get(label =exclsupprform.cleaned_data['exclmod'])
                messages.info(request, _("Modification non autorisée : Le nouvel intitulé d'exclusion est déjà utilisé"))
            except:
                if exclsupprform.cleaned_data['exclmod']:
                    for it in ItemRecord.objects.using(bdd).filter(excl =exclsupprform.cleaned_data['exclreason']):
                        if it.excl ==exclsupprform.cleaned_data['exclreason']:
                            it.excl =exclsupprform.cleaned_data['exclmod']
                            it.save(using =bdd)
                    op.label =exclsupprform.cleaned_data['exclmod']
                    op.save(using =bdd)
                    messages.info(request, _('Exclusion modifiée avec succès'))
                else:
                    messages.info(request, _("Vous n'avez pas complété le formulaire correctement"))

    if request.method =="POST":
        return HttpResponseRedirect(url)

    return render(request, 'epl/admzexcl.html', locals())


@login_required
def projinfos_adm(request, bdd):

    #contrôle d'accès ici
    suffixe = "@" + str(bdd)
    if not request.user.username[-3:] ==suffixe:
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)
    if not len(BddAdmin.objects.using(bdd).filter(contact =request.user.email)):
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)

    k =logstatus(request)
    version =epl_version
    url ="/" + bdd + "/adminbase"
        
    project = Project.objects.using(bdd).all().order_by('pk')[0].name
    extractdate =Project.objects.using(bdd).all().order_by('pk')[0].date

    #Stuff about project
    class ProjNameForm(forms.Form):
        projname = forms.CharField(required =True, widget=forms.TextInput(attrs={'size': '30'}), max_length=30, label =_("project code name"))
    projnamform = ProjNameForm(request.POST or None)
    if projnamform.is_valid():
        prj =Project.objects.using(bdd).all().order_by('pk')[0]
        prj.name =projnamform.cleaned_data['projname']
        prj.save(using =bdd)
        messages.info(request, _("Le nom du projet a été modifié avec succès"))
        # return HttpResponseRedirect(url)
        
    class ProjDateForm(forms.Form):
        projdate =forms.CharField(required =True, widget=forms.TextInput(attrs={'size': '30'}), max_length=50, label =_("database extraction date"))
    projdateform = ProjDateForm(request.POST or None)
    if projdateform.is_valid():
        prj =Project.objects.using(bdd).all().order_by('pk')[0]
        prj.date =projdateform.cleaned_data['projdate']
        prj.save(using =bdd)
        messages.info(request, _("La date d'extraction de la base a été modifiée avec succès"))
        # return HttpResponseRedirect(url)

    prj =Project.objects.using(bdd).all().order_by('pk')[0]
    baselist =[em.mail for em in Utilisateur.objects.using(bdd).all()]
    diff_list =prj.descr.split(", ")
    diff_list.sort()
    for t in baselist:
        if t not in diff_list:
            diff_list.append(t)
    diff_list.sort()
    prj.descr =""
    for elmt in diff_list:
        if elmt:
            prj.descr += elmt + ", "
    prj.save(using =bdd)

    class DiffAjForm(forms.Form):
        aj_email = forms.EmailField(required =True, label ='email')
    projajemail = DiffAjForm(request.POST or None)
    if projajemail.is_valid():
        prj =Project.objects.using(bdd).all().order_by('pk')[0]
        if projajemail.cleaned_data['aj_email'] not in diff_list:
            diff_list.append(projajemail.cleaned_data['aj_email'])
            diff_list.sort()
            prj.descr =""
            for elmt in diff_list:
                prj.descr +=", " + elmt
            prj.save(using =bdd)
            host = str(request.get_host())
            subject = _("eplouribousse (Projet : ") + Project.objects.using(bdd).all().order_by('pk')[0].name + \
            ")" + _(" > Ajout à la liste de diffusion")
            message = _("Votre email vient d'être ajouté à la liste de diffusion.") + "\n" + \
            _("L'utilisation du site suppose que vous consentez aux règles de confidentialité et aux conditions générales d'utilisation :") + \
            "\n" + "http://" + host + "/default/cgu" + "\n" + "http://" + host + "/default/confidentialite" + "\n" + "\n" + \
            _("Si vous pensez qu'il s'agit d'une erreur, veuillez contacter le responsable de projet concerné :") + "\n" + \
            "http://" + host + "/" + bdd + "/projectmaster" + "\n" + "\n" + \
            _("Merci d'utiliser eplouribousse !")
            dest =[projajemail.cleaned_data['aj_email']]
            send_mail(subject, message, replymail, dest, fail_silently=True, )
            messages.info(request, _("Un message d'information a été envoyé à cet email (pour info d'ajout)."))
        else:
            messages.info(request, _("Ce mail est déjà dans la liste."))

    SUPP_CHOICES = ("",""),
    for f in diff_list:
        if f not in baselist and not f =="":
            SUPP_CHOICES +=(f, f),
    class SupprForm(forms.Form):
        suppremail = forms.ChoiceField(required = True, widget=forms.Select, choices=SUPP_CHOICES, label =_("email"))
        supprconfirm = forms.BooleanField(required=True)
    suppremail = SupprForm(request.POST or None)
    if suppremail.is_valid():
        diff_list.remove(suppremail.cleaned_data['suppremail'])
        prj.descr =""
        for elmt in diff_list:
            prj.descr += elmt + ", "        
        prj.save(using =bdd)
        host = str(request.get_host())
        subject = _("eplouribousse (Projet : ") + Project.objects.using(bdd).all().order_by('pk')[0].name + \
        ")" + _(" > Suppression de la liste de diffusion")
        message = _("Votre email vient d'être supprimé de la liste de diffusion.") + "\n" + \
        _("Cette suppression fait normalement suite à une demande de votre part.") + "\n" + \
        _("Si vous pensez qu'il s'agit d'une erreur, veuillez contacter le responsable de projet concerné :") + "\n" + \
        "http://" + host + "/" + bdd + "/projectmaster" + "\n" + "\n" + _("Merci d'utiliser eplouribousse !")
        dest =[suppremail.cleaned_data['suppremail']]
        send_mail(subject, message, replymail, dest, fail_silently=True, )
        messages.info(request, _("Un message d'information a été envoyé à cet email (pour info de suppression)."))
    else:
        for elmt in diff_list:
            if not "@" in elmt and not "." in elmt:
                diff_list.remove(elmt)
        prj.descr =""
        for elmt in diff_list:
            prj.descr += elmt + ", "        
        prj.save(using =bdd)  

    if request.method =="POST":
        return HttpResponseRedirect(url)

    return render(request, 'epl/admzprojinfos.html', locals())


@login_required
def lib_adm(request, bdd):

    #contrôle d'accès ici
    suffixe = "@" + str(bdd)
    if not request.user.username[-3:] ==suffixe:
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)
    if not len(BddAdmin.objects.using(bdd).filter(contact =request.user.email)):
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)

    k =logstatus(request)
    version =epl_version
    url ="/" + bdd + "/adminbase"
    private =Proj_setting.objects.using(bdd)[0].prv

    project = Project.objects.using(bdd).all().order_by('pk')[0].name

    #Stuff about libraries
    LIBRARY_CHOICES = ('', _('Sélectionnez la bibliothèque')), ('checker', 'checker'),
    if Library.objects.using(bdd).all().exclude(name ='checker'):
        for l in Library.objects.using(bdd).all().exclude(name ='checker').order_by('name'):
            LIBRARY_CHOICES += (l.name, l.name),

    CONTACT_CHOICE =('', _('Contact')), ('1', '1'), ('2', '2'), ('3', '3'),

    class LibrMCurNameForm(forms.Form):
        curname = forms.ChoiceField(required = True, widget=forms.Select, choices=LIBRARY_CHOICES, label =_("bibliothèque"))
        # curname = forms.CharField(required =True, widget=forms.TextInput(attrs={'size': '30'}), max_length=30, label =_("nom de la bib"))
    class LibrMNewNameForm(forms.Form):
        newlibrname = forms.CharField(required =True, widget=forms.TextInput(attrs={'size': '30', 'title': _("Action rétroactive applicable à l'ensemble des instructions")}), max_length=30, label =_("nom de la bib"))
    class LibrMCtcForm(forms.Form):
        name = forms.ChoiceField(required = True, widget=forms.Select, choices=LIBRARY_CHOICES, label =_("bibliothèque"))
        # name = forms.CharField(required =True, widget=forms.TextInput(attrs={'size': '30'}), max_length=30, label =_("nom de la bib"))
        contactnbr =forms.ChoiceField(required = True, widget=forms.Select, choices=CONTACT_CHOICE)
        contact = forms.EmailField(required =False, label ='email 1')
        ident = forms.CharField(required =False, widget=forms.TextInput(attrs=\
        {'placeholder': "Oriane@" + bdd, 'title': _("Suffixe obligatoire") + \
        ' : ' + '@' + bdd + '. ' + \
        _("Saisissez un nom d'utilisateur valide. Il ne peut contenir que des lettres, des nombres ou les caractères « @ », « . », « + », « - » et « _ ».")}), \
        max_length=30, label =_("identifiant 1"))
        suppr = forms.BooleanField(required=False)

    liblist =Library.objects.using(bdd).exclude(name ='checker')
    sizelib =len(liblist)
    try:
        bis = Utilisateur.objects.using(bdd).get(mail =Library.objects.using(bdd).get(name ='checker').contact_bis)
    except:
        bis =None
    try:
        ter = Utilisateur.objects.using(bdd).get(mail =Library.objects.using(bdd).get(name ='checker').contact_ter)
    except:
        ter =None

    libtuple =(Library.objects.using(bdd).get(name ='checker'), Utilisateur.objects.using(bdd).get(mail =Library.objects.using(bdd).get(name ='checker').contact), bis, ter),
    for libelmt in liblist:
        try:
            bis = Utilisateur.objects.using(bdd).get(mail =Library.objects.using(bdd).get(name =libelmt.name).contact_bis)
        except:
            bis =None
        try:
            ter = Utilisateur.objects.using(bdd).get(mail =Library.objects.using(bdd).get(name =libelmt.name).contact_ter)
        except:
            ter =None
        libtuple +=(Library.objects.using(bdd).get(name =libelmt.name), Utilisateur.objects.using(bdd).get(mail =Library.objects.using(bdd).get(name =libelmt.name).contact), bis, ter),

    formlibname = LibrMCurNameForm(request.POST or None)
    formnewlibname = LibrMNewNameForm(request.POST or None)
    formlibct = LibrMCtcForm(request.POST or None)

    if formlibname.is_valid() and formnewlibname.is_valid():
        if not formlibname.cleaned_data['curname'] ==formnewlibname.cleaned_data['newlibrname']:
            if formlibname.cleaned_data['curname'] =='checker' or formnewlibname.cleaned_data['newlibrname'] =='checker':
                messages.info(request, _("'checker' est un nom réservé"))
                # return HttpResponseRedirect(url)
            else:
                try:
                    bibliot =Library.objects.using(bdd).get(name =formlibname.cleaned_data['curname'])
                    curname = formlibname.cleaned_data['curname']
                    newname = formnewlibname.cleaned_data['newlibrname']
                    for insn in Instruction.objects.using(bdd).filter(name =curname):
                        insn.name =newname
                        insn.save(using =bdd)
                    for inso in Instruction.objects.using(bdd).filter(oname =curname):
                        inso.oname =newname
                        inso.save(using =bdd)
                    lib = Library.objects.using(bdd).get(name =curname)
                    lib.name =formnewlibname.cleaned_data['newlibrname']
                    lib.save(using =bdd)
                    messages.info(request, _("Nom de la bibliothèque modifié avec succès"))
                    # return HttpResponseRedirect(url)
                except:
                    pass
                    # messages.info(request, _("Pas de bibliothèque au nom que vous avez indiqué"))
                    # return HttpResponseRedirect(url)

    if formlibct.is_valid():
        if not formlibct.cleaned_data['contact'] == formlibct.cleaned_data['contact'].lower():
            messages.info(request, _("échec : l'adresse mail doit être indiquée entièrement en minuscules."))
            return render(request, 'epl/admzlib.html', locals())
        try:
            if Library.objects.using(bdd).get(name =formlibct.cleaned_data['name']) in Library.objects.using(bdd).all():
                lib = Library.objects.using(bdd).get(name =formlibct.cleaned_data['name'])
                if formlibct.cleaned_data['suppr'] ==True:
                    compteura =0
                    if formlibct.cleaned_data['contactnbr'] =='2':
                        for u in Library.objects.using(bdd).all():
                            if u.contact ==lib.contact_bis:
                                compteura +=1
                            if u.contact_bis ==lib.contact_bis:
                                compteura +=1
                            if u.contact_ter ==lib.contact_bis:
                                compteura +=1
                        for v in BddAdmin.objects.using(bdd).all():
                            if v.contact ==lib.contact_bis:
                                compteura +=1
                        if compteura ==1:
                            user =User.objects.get(username =Utilisateur.objects.using(bdd).get(mail =lib.contact_bis).username)
                            uter =Utilisateur.objects.using(bdd).get(mail =lib.contact_bis)
                            user_suppr(request, bdd, User.objects.get(username =Utilisateur.objects.using(bdd).get(mail =lib.contact_bis).username))
                            diffsupupdate(request, bdd, lib.contact_bis)
                            user.delete()
                            uter.delete()
                        if lib.contact_bis ==None:
                            messages.info(request, _("Suppression impossible : Le contact était déjà vacant."))
                        else:
                            lib.contact_bis =None
                            lib.save(using =bdd)
                            messages.info(request, _('Contact supprimé avec succès'))

                    compteurb =0
                    if formlibct.cleaned_data['contactnbr'] =='3':
                        for u in Library.objects.using(bdd).all():
                            if u.contact ==lib.contact_ter:
                                compteurb +=1
                            if u.contact_bis ==lib.contact_ter:
                                compteurb +=1
                            if u.contact_ter ==lib.contact_ter:
                                compteurb +=1
                        for v in BddAdmin.objects.using(bdd).all():
                            if v.contact ==lib.contact_ter:
                                compteurb +=1
                        if compteurb ==1:
                            user =User.objects.get(username =Utilisateur.objects.using(bdd).get(mail =lib.contact_ter).username)
                            uter =Utilisateur.objects.using(bdd).get(mail =lib.contact_ter)
                            user_suppr(request, bdd, User.objects.get(username =Utilisateur.objects.using(bdd).get(mail =lib.contact_ter).username))
                            diffsupupdate(request, bdd, lib.contact_ter)
                            user.delete()
                            uter.delete()
                        if lib.contact_ter ==None:
                            messages.info(request, _("Suppression impossible : Le contact était déjà vacant."))
                        else:
                            lib.contact_ter =None
                            lib.save(using =bdd)
                            messages.info(request, _('Contact supprimé avec succès'))

                        # return HttpResponseRedirect(url)
                    if formlibct.cleaned_data['contactnbr'] =='1':
                        messages.info(request, _('Le contact principal ne peut pas être supprimé'))
                        # return HttpResponseRedirect(url)
                else:#formlibct.cleaned_data['suppr'] ==False
                    if not formlibct.cleaned_data['ident'] and formlibct.cleaned_data['contact']:
                        messages.info(request, _("Echec : Vous avez omis l'identifiant"))
                    elif formlibct.cleaned_data['ident'] and not formlibct.cleaned_data['contact']:
                        messages.info(request, _("Echec : Vous avez omis l'email"))
                    else:#Formulaire complet
                        try:#utilisateur déjà présent dans la base
                            uter =Utilisateur.objects.using(bdd).get(username =formlibct.cleaned_data['ident'], mail =formlibct.cleaned_data['contact'])
                            if formlibct.cleaned_data['contactnbr'] =='1':
                                lib.contact =formlibct.cleaned_data['contact']
                                lib.save(using =bdd)
                            if formlibct.cleaned_data['contactnbr'] =='2':
                                lib.contact_bis =formlibct.cleaned_data['contact']
                                lib.save(using =bdd)
                            if formlibct.cleaned_data['contactnbr'] =='3':
                                lib.contact_ter =formlibct.cleaned_data['contact']
                                lib.save(using =bdd)
                            messages.info(request, _("Modification effectuée avec succès (réemploi d'un utilisateur déjà présent dans la base : {} )".format(uter.username)))
                                # return HttpResponseRedirect(url)
                        except:#utilisateur absent de la base
                            if len(Utilisateur.objects.using(bdd).filter(username =formlibct.cleaned_data['ident'])):
                                messages.info(request, _("Echec : l'identifiant est déjà attribué à un autre utilisateur"))
                            elif len(Utilisateur.objects.using(bdd).filter(mail =formlibct.cleaned_data['contact'])):
                                messages.info(request, _("Echec : l'email est déjà attribué à un autre utilisateur"))
                            else:
                                if str(formlibct.cleaned_data['ident'])[-3:] !=suffixe:
                                    messages.info(request, _("Echec : L'identifiant doit se terminer en {}".format(suffixe)))
                                else:
                                    try:
                                        user =User.objects.create_user(username =formlibct.cleaned_data['ident'], email =formlibct.cleaned_data['contact'], password ="glass onion")
                                        uter =Utilisateur(username =formlibct.cleaned_data['ident'], mail =formlibct.cleaned_data['contact'], \
                                                          rkg =Proj_setting.objects.using(bdd)[0].rkg, \
                                                          arb =Proj_setting.objects.using(bdd)[0].arb, \
                                                          ins =Proj_setting.objects.using(bdd)[0].ins, \
                                                          edi =Proj_setting.objects.using(bdd)[0].edi)
                                        uter.save(using =bdd)
                                        if formlibct.cleaned_data['contactnbr'] =='1':
                                            lib.contact =formlibct.cleaned_data['contact']
                                            lib.save(using =bdd)
                                        if formlibct.cleaned_data['contactnbr'] =='2':
                                            lib.contact_bis =formlibct.cleaned_data['contact']
                                            lib.save(using =bdd)
                                        if formlibct.cleaned_data['contactnbr'] =='3':
                                            lib.contact_ter =formlibct.cleaned_data['contact']
                                            lib.save(using =bdd)
                                        messages.info(request, _("Modification effectuée avec succès (un nouvel utilisateur a été créé et ajouté la liste de diffusion ; les instructions complémentaires lui ont été automatiquement envoyées par mail.)"))
                                        host = str(request.get_host())
                                        subject_a = _("eplouribousse (Projet : ") + Project.objects.using(bdd).all().order_by('pk')[0].name + \
                                        ")" + _(" > Création de votre mot de passe")
                                        message_a = _("Le responsable de projet vient de vous enregistrer comme nouvel utilisateur sous l'identifiant : {}".format(formlibct.cleaned_data['ident'])) + \
                                        "\n" + _("Votre email a été ajouté à la liste de diffusion du projet.") + \
                                        "\n" + _("Pour finaliser votre enregistrement, veuillez créer votre mot de passe :") + "\n" + \
                                        "http://" + host + "/default/password_reset/" +  "\n" + "\n" + \
                                        _("L'utilisation du site suppose que vous consentez aux règles de confidentialité et aux conditions générales d'utilisation :") \
                                        + "\n" + "http://" + host + "/default/cgu" + "\n" + "http://" + host + "/default/confidentialite" + "\n" + "\n" + \
                                        _("Si vous pensez qu'il s'agit d'une erreur, veuillez contacter le responsable de projet concerné :") + "\n" + \
                                        "http://" + host + "/" + bdd + "/projectmaster" + "\n" + "\n" + _("Merci d'utiliser eplouribousse !")
                                        subject_b = _("eplouribousse (Projet : ") + Project.objects.using(bdd).all().order_by('pk')[0].name + \
                                        ")" + _(" > Infos complémentaires")
                                        message_b = _("Ce message en complète un autre relatif à la création de votre mot de passe.") + \
                                        "\n" + _("Pour connaître le réglage des alertes par mail au niveau du projet et éventuellement les restreindre à votre niveau :") + \
                                        "\n" + "http://" + host + "/" + bdd + "/alerts_user" + \
                                        "\n" + _("Vous pouvez ignorer ce message si vous vous en remettez aux alertes activées au niveau du projet (recommandé).") + \
                                        "\n" + _("Notez que dans tous les cas, vous devez d'abord créer votre mot de passe (voir autre message).")
                                        dest = [uter.mail]
                                        send_mail(subject_a, message_a, replymail, dest, fail_silently=True, )
                                        send_mail(subject_b, message_b, replymail, dest, fail_silently=True, )
                                        diffajupdate(request, bdd, uter.mail)
                                    except:
                                        messages.info(request, _("L'identifiant ne respecte pas le format prescrit"))
        except:
            pass

    if request.method =="POST":
        return HttpResponseRedirect(url)
    else:#request.method =="GET
    #La partie de code ci-dessous est reproduite dans la vue home(request, bdd) = Synchronisation de la base locale (utilisateurs) avec la base générale (users)
        for e in Utilisateur.objects.using(bdd).all():#1/2 création d'éventuels nouveaux users dans la base générale
            try:
                user =User.objects.get(username =e.username)
            except:
                user =User.objects.create_user(username =e.username, email =e.mail, password ="glass onion")

        #2/2 (see upper, this order is important)
        suffixe = "@" + str(bdd)
        for j in User.objects.all(): #Suppression d'users pour lesquels l'utilisateur a été supprimé de la base locale
            if j.username[-3:] ==suffixe:
                try:
                    utilisateur =Utilisateur.objects.using(bdd).get(username =j.username)
                except:
                    j.delete() #suppression dans la bdd générale

    return render(request, 'epl/admzlib.html', locals())


@login_required
def alerts_adm(request, bdd):

    #contrôle d'accès ici
    suffixe = "@" + str(bdd)
    if not request.user.username[-3:] ==suffixe:
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)
    if not len(BddAdmin.objects.using(bdd).filter(contact =request.user.email)):
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)

    k =logstatus(request)
    version =epl_version
#    url ="/" + bdd + "/alerts_adm"
    url ="/" + bdd + "/adminbase"
    private =Proj_setting.objects.using(bdd)[0].prv

    # gestion des alertes et du mode (début)
    current_alerts =[] #initialzing
    if Proj_setting.objects.using(bdd)[0].rkg:
        current_alerts.append(_("positionnement"))
    if Proj_setting.objects.using(bdd)[0].arb:
        current_alerts.append(_("arbitrages"))
    if Proj_setting.objects.using(bdd)[0].ins:
        current_alerts.append(_("instructions"))
    if Proj_setting.objects.using(bdd)[0].edi:
        current_alerts.append(_("résultantes"))
    if len(current_alerts):
        al =1
    else:
        al =0
    if Proj_setting.objects.using(bdd)[0].prv:
        priv_mode = _("activé")
    else:
        priv_mode = _("désactivé")

    SETTING_CHOICES = (
        ('rkg', _("Alertes positionnement")),
        ('arb', _("Alertes arbitrages")),
        ('ins', _("Alertes instructions")),
        ('edi', _("Alertes résultantes")),
        ('prv', _("Mode édition restreint (usagers autorisés)")),
    )

    actu =[]
    projsetlist =Proj_setting.objects.using(bdd).all().order_by('pk')
    if Proj_setting.objects.using(bdd).get(pk = projsetlist[0].pk).rkg:
        actu.append('rkg')
    if Proj_setting.objects.using(bdd).get(pk = projsetlist[0].pk).arb:
        actu.append('arb')
    if Proj_setting.objects.using(bdd).get(pk = projsetlist[0].pk).ins:
        actu.append('ins')
    if Proj_setting.objects.using(bdd).get(pk = projsetlist[0].pk).edi:
        actu.append('edi')
    if Proj_setting.objects.using(bdd).get(pk = projsetlist[0].pk).prv:
        actu.append('prv')
    class ProjoSettings(forms.Form):
        projsett = forms.MultipleChoiceField(required = False, widget=forms.CheckboxSelectMultiple(), choices=SETTING_CHOICES, initial =actu, label =_("Choisissez vos nouveaux réglages"))

    projosetform = ProjoSettings(request.POST or None)
    if projosetform.is_valid():
        settinglist =projosetform.cleaned_data['projsett']
        newprojset =Proj_setting()
        if "rkg" in settinglist:
            newprojset.rkg =1
            for e in Utilisateur.objects.using(bdd).all():
                e.rkg =1
                e.save(using =bdd)
        else:
            newprojset.rkg =0
            for e in Utilisateur.objects.using(bdd).all():
                e.rkg =0
                e.save(using =bdd)
        if "arb" in settinglist:
            newprojset.arb =1
            for e in Utilisateur.objects.using(bdd).all():
                e.arb =1
                e.save(using =bdd)
        else:
            newprojset.arb =0
            for e in Utilisateur.objects.using(bdd).all():
                e.arb =0
                e.save(using =bdd)
        if "ins" in settinglist:
            newprojset.ins =1
            for e in Utilisateur.objects.using(bdd).all():
                e.ins =1
                e.save(using =bdd)
        else:
            newprojset.ins =0
            for e in Utilisateur.objects.using(bdd).all():
                e.ins =0
                e.save(using =bdd)
        if "edi" in settinglist:
            newprojset.edi =1
            for e in Utilisateur.objects.using(bdd).all():
                e.edi =1
                e.save(using =bdd)
        else:
            newprojset.edi =0
            for e in Utilisateur.objects.using(bdd).all():
                e.edi =0
                e.save(using =bdd)
        if "prv" in settinglist:
            newprojset.prv =1
        else:
            newprojset.prv =0
        newprojset.save(using =bdd)
        projsetlist =Proj_setting.objects.using(bdd).all().order_by('pk')
        oldprojset =Proj_setting.objects.using(bdd).get(pk = projsetlist[0].pk)
        oldprojset.delete(using =bdd)
        messages.info(request, _("Les alertes et le type d'accès ont été reconfigurés avec succès."))
        messages.info(request, _("Les utilisateurs recevront un message d'information circonstancié"))
        
        # (message)
        host = str(request.get_host())
        subject = _("eplouribousse (Projet : ") + Project.objects.using(bdd).all().order_by('pk')[0].name + \
        ")" + _(" > Modification des réglages")
        message = _("Les réglages du projet ont été réinitialisés par l'administrateur.") + "\n" + \
        _("Vous pouvez ignorer ce message si vous vous en remettez aux alertes activées au niveau du projet (recommandé)") + "\n" + \
        _("Sinon, pour voir les alertes activées et éventuellement en supprimer à votre niveau : ") + "\n" + \
        "http://" + host + "/" + bdd + "/alerts_user"
        dest =[]
        for libmt in Library.objects.using(bdd).all():
            if libmt.contact and libmt.contact not in dest:
                dest.append(libmt.contact)
            if libmt.contact_bis and libmt.contact_bis not in dest:
                dest.append(libmt.contact_bis)
            if libmt.contact_ter and libmt.contact_ter not in dest:
                dest.append(libmt.contact_ter)
        send_mail(subject, message, replymail, dest, fail_silently=True, )

    # gestion des alertes et du mode (fin)

    project = Project.objects.using(bdd).all().order_by('pk')[0].name

    if request.method =="POST":
        return HttpResponseRedirect(url)

    return render(request, 'epl/admzalerts.html', locals())


@login_required
def alerts_user(request, bdd):

    #contrôle d'accès ici
    suffixe = "@" + str(bdd)
    if not request.user.username[-3:] ==suffixe:
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)
    if not len(Utilisateur.objects.using(bdd).filter(mail =request.user.email)):
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)

    k =logstatus(request)
    version =epl_version
    url ="/" + bdd
    private =Proj_setting.objects.using(bdd)[0].prv

    # gestion des alertes au niveau de l'utilisateur (début)
    current_alerts =[] #initialzing
    SETTING_CHOICES = ()
    if Proj_setting.objects.using(bdd)[0].rkg:
        current_alerts.append(_("positionnement"))
        SETTING_CHOICES += (
        ('rkg', _("Alertes positionnement")),
        )
    if Proj_setting.objects.using(bdd)[0].arb:
        current_alerts.append(_("arbitrages"))
        SETTING_CHOICES += (
        ('arb', _("Alertes arbitrages")),
        )
    if Proj_setting.objects.using(bdd)[0].ins:
        current_alerts.append(_("instructions"))
        SETTING_CHOICES += (
        ('ins', _("Alertes instructions")),
        )
    if Proj_setting.objects.using(bdd)[0].edi:
        current_alerts.append(_("résultantes"))
        SETTING_CHOICES += (
        ('edi', _("Alertes résultantes")),
        )
    if len(current_alerts):
        al =1
    else:
        al =0

    actu =[]
    projsetlist =Proj_setting.objects.using(bdd).all().order_by('pk')
    if Utilisateur.objects.using(bdd).get(username =request.user.username).rkg:
        actu.append('rkg')
    if Utilisateur.objects.using(bdd).get(username =request.user.username).arb:
        actu.append('arb')
    if Utilisateur.objects.using(bdd).get(username =request.user.username).ins:
        actu.append('ins')
    if Utilisateur.objects.using(bdd).get(username =request.user.username).edi:
        actu.append('edi')

    class ProjoSettings(forms.Form):
        projsett = forms.MultipleChoiceField(required = False, widget=forms.CheckboxSelectMultiple(), choices=SETTING_CHOICES, initial =actu, label =_("Activez ou désactivez vos propres réglages courants selon vos souhaits"))

    projosetform = ProjoSettings(request.POST or None)
    if projosetform.is_valid():
        settinglist =projosetform.cleaned_data['projsett']
        u =Utilisateur.objects.using(bdd).get(username =request.user.username)
#        newprojset =Proj_setting()
        if "rkg" in settinglist:
            u.rkg =1
        else:
            u.rkg =0
        if "arb" in settinglist:
            u.arb =1
        else:
            u.arb =0
        if "ins" in settinglist:
            u.ins =1
        else:
            u.ins =0
        if "edi" in settinglist:
            u.edi =1
        else:
            u.edi =0
        u.save(using =bdd)

        messages.info(request, _("Les alertes et le type d'accès ont été reconfigurés avec succès"))
    # gestion des alertes au niveau de l'utilisateur (fin)

    project = Project.objects.using(bdd).all().order_by('pk')[0].name

    if request.method =="POST":
        return HttpResponseRedirect(url)

    return render(request, 'epl/alerts_user.html', locals())


@login_required
def admins_adm(request, bdd):

    #contrôle d'accès ici
    suffixe = "@" + str(bdd)
    if not request.user.username[-3:] ==suffixe:
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)
    if not len(BddAdmin.objects.using(bdd).filter(contact =request.user.email)):
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)

    k =logstatus(request)
    version =epl_version
    url ="/" + bdd + "/adminbase"
    private =Proj_setting.objects.using(bdd)[0].prv

    project = Project.objects.using(bdd).all().order_by('pk')[0].name

    #Stuff about bddadministrators
    admintuple =('', "Sélectionnez l'administrateur"),
    for b in BddAdmin.objects.using(bdd).all():
        admintuple +=(b.contact, Utilisateur.objects.using(bdd).get(mail =BddAdmin.objects.using(bdd).get(contact =b.contact).contact)),
    admintup =admintuple[1:]
    sizeadm =len(BddAdmin.objects.using(bdd).all())

    class ProjadmAjForm(forms.Form):
        contactajadm = forms.EmailField(required =True, label ='current email')
        identajadm = forms.CharField(required =True, widget=forms.TextInput(attrs=\
        {'placeholder': "Rosemonde@" + bdd, 'title': _("Suffixe obligatoire") + \
        ' : ' + '@' + bdd + '. ' + \
        "Saisissez un nom d'utilisateur valide. Il ne peut contenir que des lettres, des nombres ou les caractères « @ », « . », « + », « - » et « _ »."}), \
        max_length=30, label =_("identifiant"))

    projajadmform =ProjadmAjForm(request.POST or None)

    class ProjadmSupprForm(forms.Form):
        contactsuadm = forms.ChoiceField(required = True, widget=forms.Select, choices=admintuple, label =_("email courant"))
        suppradm = forms.BooleanField(required=True)

    projsuppradmform =ProjadmSupprForm(request.POST or None)

    if projajadmform.is_valid():
        if not projajadmform.cleaned_data['contactajadm'] == projajadmform.cleaned_data['contactajadm'].lower():
            messages.info(request, _("échec : l'adresse mail doit être indiquée entièrement en minuscules."))
            return render(request, 'epl/admzadmins.html', locals()) 
        try:
            newadm =BddAdmin.objects.using(bdd).get(contact =projajadmform.cleaned_data['contactajadm'])
            messages.info(request, _("(Administrateur déjà enregistré)"))
        except:
            try:
                uter =Utilisateur.objects.using(bdd).get(username =projajadmform.cleaned_data['identajadm'], mail =projajadmform.cleaned_data['contactajadm'])
                newadm =BddAdmin(contact =projajadmform.cleaned_data['contactajadm'])
                newadm.save(using =bdd)
                messages.info(request, _("Administrateur ajouté avec succès (réemploi d'un utilisateur déjà présent dans la base)"))
            except:
                try:
                    uter =Utilisateur.objects.using(bdd).get(username =projajadmform.cleaned_data['identajadm'])
                    messages.info(request, _("Echec : L'identifiant saisi est déjà utilisé"))
                except:
                    try:
                        uter =Utilisateur.objects.using(bdd).get(mail =projajadmform.cleaned_data['contactajadm'])
                        messages.info(request, _("Echec : L'email saisi est déjà utilisé"))
                    except:
                        if str(projajadmform.cleaned_data['identajadm'])[-3:] !=suffixe:
                            messages.info(request, _("Echec : L'identifiant doit se terminer en {}".format(suffixe)))
                        else:
                            try:
                                uter =Utilisateur(username =projajadmform.cleaned_data['identajadm'], mail =projajadmform.cleaned_data['contactajadm'], \
                                                  rkg =Proj_setting.objects.using(bdd)[0].rkg, \
                                                  arb =Proj_setting.objects.using(bdd)[0].arb, \
                                                  ins =Proj_setting.objects.using(bdd)[0].ins, \
                                                  edi =Proj_setting.objects.using(bdd)[0].edi)
                                user =User.objects.create_user(username =projajadmform.cleaned_data['identajadm'], email =projajadmform.cleaned_data['contactajadm'], password ="glass onion")
                                uter.save(using =bdd)
                                newadm =BddAdmin(contact =projajadmform.cleaned_data['contactajadm'])
                                newadm.save(using =bdd)
                                diffajupdate(request, bdd, projajadmform.cleaned_data['contactajadm'])
                                host = str(request.get_host())
                                subject = _("eplouribousse (Projet : ") + Project.objects.using(bdd).all().order_by('pk')[0].name + \
                                ")" + _(" > Création de votre mot de passe")
                                message = _("Le responsable de projet vient de vous enregistrer comme nouvel utilisateur (administrateur du projet) sous l'identifiant : {}".format(projajadmform.cleaned_data['identajadm'])) + \
                                "\n" + _("Votre email a été ajouté à la liste de diffusion du projet") + "\n" + \
                                _("Pour finaliser votre enregistrement, veuillez créer votre mot de passe :") + "\n" + \
                                "http://" + host + "/default/password_reset/" + "\n" + "\n" + \
                                _("L'utilisation du site suppose que vous consentez aux règles de confidentialité et aux conditions générales d'utilisation :") + \
                                "\n" + "http://" + host + "/default/cgu/" + "\n" + "http://" + host + "/default/confidentialite/" + "\n" + "\n" + \
                                _("Si vous pensez qu'il s'agit d'une erreur, veuillez contacter le responsable de projet concerné :") + "\n" + \
                                "http://" + host + bdd + "/projectmaster" + "\n" + "\n" + _("Merci d'utiliser eplouribousse !")
                                dest = [uter.mail]
                                send_mail(subject, message, replymail, dest, fail_silently=True, )
                                messages.info(request, _("Administrateur ajouté avec succès (un nouvel utilisateur a été créé ; les instructions complémentaires lui ont été automatiquement envoyées par mail.)"))
                            except:
                                messages.info(request, _("Echec : L'identifiant ne respecte pas le format prescrit"))

    if projsuppradmform.is_valid():
        if len(BddAdmin.objects.using(bdd).all()) ==1:
            messages.info(request, _("Vous ne pouvez pas supprimer le dernier administrateur restant"))
        else:
            suppradm =BddAdmin.objects.using(bdd).get(contact =projsuppradmform.cleaned_data['contactsuadm'])
            compteurc =0
            for u in Library.objects.using(bdd).all():
                if u.contact ==suppradm.contact:
                    compteurc +=1
                if u.contact_bis ==suppradm.contact:
                    compteurc +=1
                if u.contact_ter ==suppradm.contact:
                    compteurc +=1
            for v in BddAdmin.objects.using(bdd).all():
                if v.contact ==suppradm.contact:
                    compteurc +=1
            if compteurc ==1:
                user =User.objects.get(username =Utilisateur.objects.using(bdd).get(mail =projsuppradmform.cleaned_data['contactsuadm']).username)
                uter =Utilisateur.objects.using(bdd).get(mail =projsuppradmform.cleaned_data['contactsuadm'])
                user_suppr(request, bdd, Utilisateur.objects.using(bdd).get(mail =projsuppradmform.cleaned_data['contactsuadm']).username)
                diffsupupdate(request, bdd, projsuppradmform.cleaned_data['contactsuadm'])
                user.delete()
                uter.delete()
            suppradm.delete(using =bdd)
            messages.info(request, _('Administrateur supprimé avec succès'))

    if request.method =="POST":
        return HttpResponseRedirect(url)
    else:#request.method =="GET
    #La partie de code ci-dessous est reproduite dans la vue home(request, bdd) = Synchronisation de la base locale (utilisateurs) avec la base générale (users)
        for e in Utilisateur.objects.using(bdd).all():#1/2 création d'éventuels nouveaux users dans la base générale
            try:
                user =User.objects.get(username =e.username)
            except:
                user =User.objects.create_user(username =e.username, email =e.mail, password ="glass onion")

        #2/2 (see upper, this order is important)
        suffixe = "@" + str(bdd)
        for j in User.objects.all(): #Suppression d'users pour lesquels l'utilisateur a été supprimé de la base locale
            if j.username[-3:] ==suffixe:
                try:
                    utilisateur =Utilisateur.objects.using(bdd).get(username =j.username)
                except:
                    j.delete() #suppression dans la bdd générale

    return render(request, 'epl/admzadmins.html', locals())


@login_required
def uters_adm(request, bdd):
    
    """
    -------------------------------------------------------------------------------------------
    Gestion des utilisateurs.
    -------------------------------------------------------------------------------------------
    """

    #contrôle d'accès ici
    suffixe = "@" + str(bdd)
    if not request.user.username[-3:] ==suffixe:
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)
    if not len(BddAdmin.objects.using(bdd).filter(contact =request.user.email)):
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)

    k =logstatus(request)
    version =epl_version
    url ="/" + bdd + "/adminbase"
    private =Proj_setting.objects.using(bdd)[0].prv

    project = Project.objects.using(bdd).all().order_by('pk')[0].name

    #Stuff about instructors :
    uterstuple =('', "Sélectionnez l'utilisateur"),
    for u in Utilisateur.objects.using(bdd).all().order_by("username"):
        uterstuple +=(u.mail, Utilisateur.objects.using(bdd).get(mail =u.mail)),
    sizeuters =len(Utilisateur.objects.using(bdd).all())

    class UtModForm(forms.Form):
        uterxy = forms.ChoiceField(required = True, widget=forms.Select, choices=uterstuple, label =_("Utilisateur"))
        newuterid = forms.CharField(required =False, widget=forms.TextInput(attrs=\
        {'placeholder': "Marcel@" + bdd, 'title': _("Suffixe obligatoire") + \
        ' : ' + '@' + bdd + '. ' + \
        "Saisissez un nom d'utilisateur valide. Il ne peut contenir que des lettres, des nombres ou les caractères « @ », « . », « + », « - » et « _ »."}), \
        max_length=30, label =_("nouvel identifiant de l'utilisateur"))
        newutermail = forms.EmailField(required =False, label ="nouvel email de l'utilisateur")

    utermodform =UtModForm(request.POST or None)

    if utermodform.is_valid():
        if not utermodform.cleaned_data['newutermail'] == utermodform.cleaned_data['newutermail'].lower():
            messages.info(request, _("échec : l'adresse mail doit être indiquée entièrement en minuscules."))
            return render(request, 'epl/admzinstrtrs.html', locals())
        if utermodform.cleaned_data['newuterid'] and utermodform.cleaned_data['newutermail']:
            messages.info(request, _("Echec : Ne complétez qu'un des arguments à la fois"))
            return render(request, 'epl/admzinstrtrs.html', locals())
        else:
            try:
                uter =Utilisateur.objects.using(bdd).get(mail =utermodform.cleaned_data['newutermail'])
                messages.info(request, _("Echec : L'email saisi est déjà utilisé"))
            except:
                try:
                    uter =Utilisateur.objects.using(bdd).get(username =utermodform.cleaned_data['newuterid'])
                    messages.info(request, _("Echec : L'identifiant saisi est déjà utilisé"))
                except:
                    if utermodform.cleaned_data['newuterid']:
                        if str(utermodform.cleaned_data['newuterid'])[-3:] !=suffixe:
                            messages.info(request, _("Echec : L'identifiant doit se terminer en {}".format(suffixe)))
                        else:
                            try:
                                uter =Utilisateur.objects.using(bdd).get(mail =utermodform.cleaned_data['uterxy'])
                                uter.username =utermodform.cleaned_data['newuterid']
                                user =User.objects.get(username =Utilisateur.objects.using(bdd).get(mail =utermodform.cleaned_data['uterxy']).username)
                                user.username =utermodform.cleaned_data['newuterid']
                                uter.save(using =bdd)
                                user.save()
                                userid_mod(request, bdd, uter.username, uter.mail)
                                messages.info(request, _("L'identifiant de l'utilisateur a été modifié avec succès"))
                            except:
                                messages.info(request, _("L'identifiant ne respecte pas le format prescrit"))
                    elif utermodform.cleaned_data['newutermail']:
                        try:
                            uter =Utilisateur.objects.using(bdd).get(mail =utermodform.cleaned_data['uterxy'])
                            uter.mail =utermodform.cleaned_data['newutermail']
                            user =User.objects.get(username =Utilisateur.objects.using(bdd).get(mail =utermodform.cleaned_data['uterxy']).username)
                            for l in Library.objects.using(bdd).all():
                                if l.contact ==utermodform.cleaned_data['uterxy']:
                                    l.contact =utermodform.cleaned_data['newutermail']
                                if l.contact_bis ==utermodform.cleaned_data['uterxy']:
                                    l.contact_bis =utermodform.cleaned_data['newutermail']
                                if l.contact_ter ==utermodform.cleaned_data['uterxy']:
                                    l.contact_ter =utermodform.cleaned_data['newutermail']
                                l.save(using =bdd)
                            if BddAdmin.objects.using(bdd).filter(contact =utermodform.cleaned_data['uterxy']):
                                adm =BddAdmin.objects.using(bdd).get(contact =utermodform.cleaned_data['uterxy'])
                                adm.contact =utermodform.cleaned_data['newutermail']
                                adm.save(using =bdd)
                            uter.save(using =bdd)
                            user.save()
                            #
                            diffsupupdate(request, bdd, utermodform.cleaned_data['uterxy'])
                            diffajupdate(request, bdd, utermodform.cleaned_data['newutermail'])
                            #
                            usermail_mod(request, bdd, uter.username, uter.mail)
                            messages.info(request, _("L'email de l'utilisateur a été modifié avec succès"))
                        except:
                            pass

    # (la suppression éventuelle de l'utilisateur et du user est factorisée en fin de vue) ????

    if request.method =="POST":
        return HttpResponseRedirect(url)
    else:#request.method =="GET
    #La partie de code ci-dessous est reproduite dans la vue home(request, bdd) = Synchronisation de la base locale (utilisateurs) avec la base générale (users)
        for e in Utilisateur.objects.using(bdd).all():#1/2 création d'éventuels nouveaux users dans la base générale
            try:
                user =User.objects.get(username =e.username)
            except:
                user =User.objects.create_user(username =e.username, email =e.mail, password ="glass onion")

        #2/2 (see upper, this order is important)
        suffixe = "@" + str(bdd)
        for j in User.objects.all(): #Suppression d'users pour lesquels l'utilisateur a été supprimé de la base locale
            if j.username[-3:] ==suffixe:
                try:
                    utilisateur =Utilisateur.objects.using(bdd).get(username =j.username)
                except:
                    j.delete() #suppression dans la bdd générale

    return render(request, 'epl/admzuters.html', locals())


@login_required
def authusrs_adm(request, bdd):

    #contrôle d'accès ici
    suffixe = "@" + str(bdd)
    if not request.user.username[-3:] ==suffixe:
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)
    if not len(BddAdmin.objects.using(bdd).filter(contact =request.user.email)):
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)

    k =logstatus(request)
    version =epl_version
    url ="/" + bdd + "/adminbase"
    private =Proj_setting.objects.using(bdd)[0].prv

    project = Project.objects.using(bdd).all().order_by('pk')[0].name

    #Début stuff about other authorized users
    otherauthtuple =('', "Sélectionnez l'utilisateur"),
    ft =0

    for elmt in Utilisateur.objects.using(bdd).all():
        if not BddAdmin.objects.using(bdd).filter(contact =elmt.mail) and not \
        Library.objects.using(bdd).filter(contact =elmt.mail) and not \
        Library.objects.using(bdd).filter(contact_bis =elmt.mail) and not \
        Library.objects.using(bdd).filter(contact_ter =elmt.mail):
            if elmt.username[-3:] ==suffixe:
                otherauthtuple +=(elmt.mail, Utilisateur.objects.using(bdd).get(mail =elmt.mail)),
                ft +=1
    sizeotherus =ft
    otherauthtup =otherauthtuple[1:]

    class OthUsAjForm(forms.Form):
        contactajoth = forms.EmailField(required =True, label ='current email')
        identajoth = forms.CharField(required =True, widget=forms.TextInput(attrs=\
        {'placeholder': "Charles@" + bdd, 'title': _("Suffixe obligatoire") + \
        ' : ' + '@' + bdd + '. ' + \
        "Saisissez un nom d'utilisateur valide. Il ne peut contenir que des lettres, des nombres ou les caractères « @ », « . », « + », « - » et « _ »."}), \
        max_length=30, label =_("identifiant"))

    othusajform =OthUsAjForm(request.POST or None)

    class OthUsSupprForm(forms.Form):
        contactsuoth = forms.ChoiceField(required = True, widget=forms.Select, choices=otherauthtuple, label =_("email courant"))
        supproth = forms.BooleanField(required=True)

    othussupprform =OthUsSupprForm(request.POST or None)

    if othusajform.is_valid():
        if not othusajform.cleaned_data['contactajoth'] == othusajform.cleaned_data['contactajoth'].lower():
            messages.info(request, _("échec : l'adresse mail doit être indiquée entièrement en minuscules."))
            return render(request, 'epl/admzauthusrs.html', locals())
        try:
            newothus =Utilisateur.objects.using(bdd).get(contact =othusajform.cleaned_data['contactajoth'])
            messages.info(request, _("(Utilisateur déjà enregistré avec des droits suffisants)"))
        except:
            try:
                uter =Utilisateur.objects.using(bdd).get(username =othusajform.cleaned_data['identajoth'])
                messages.info(request, _("Echec : L'identifiant saisi est déjà utilisé"))
            except:
                if str(othusajform.cleaned_data['identajoth'])[-3:] !=suffixe:
                    messages.info(request, _("Echec : L'identifiant doit se terminer en {}".format(suffixe)))
                else:
                    try:
                        uter =Utilisateur(username =othusajform.cleaned_data['identajoth'], mail =othusajform.cleaned_data['contactajoth'])
                        user =User.objects.create_user(username =othusajform.cleaned_data['identajoth'], email =othusajform.cleaned_data['contactajoth'], password ="glass onion")
                        uter.save(using =bdd)
                        diffajupdate(request, bdd, othusajform.cleaned_data['contactajoth'])
                        host = str(request.get_host())
                        subject = _("eplouribousse (Projet : ") + Project.objects.using(bdd).all().order_by('pk')[0].name + \
                        ")" + _(" > Création de votre mot de passe")
                        message = _("Le responsable de projet vient de vous enregistrer comme nouvel utilisateur autorisé sous l'identifiant : {}".format(othusajform.cleaned_data['identajoth'])) + \
                        "\n" + _("Votre email est intégré à la liste de diffusion du projet.") + \
                        "\n" + _("Pour finaliser votre enregistrement, veuillez créer votre mot de passe :") + "\n" + \
                        "http://" + host + "/default/password_reset/" + "\n" + "\n" + \
                        _("L'utilisation du site suppose que vous consentez aux règles de confidentialité et aux conditions générales d'utilisation :") + \
                        "\n" + "http://" + host + "/default/cgu/" + "\n" + "http://" + host + "/default/confidentialite/" + "\n" + "\n" + \
                        _("Si vous pensez qu'il s'agit d'une erreur, veuillez contacter le responsable de projet concerné :") + "\n" + \
                        "http://" + host + bdd + "/projectmaster" + "\n" + "\n" + _("Merci d'utiliser eplouribousse !")
                        dest = [uter.mail]
                        send_mail(subject, message, replymail, dest, fail_silently=True, )
                        messages.info(request, _("Utilisateur créé avec succès ; un message vient de lui être envoyé pour la création de son mot de passe. Son email est intégré à la liste de diffusion."))
                    except:
                        messages.info(request, _("Echec : L'identifiant ne respecte pas le format prescrit"))

    if othussupprform.is_valid():
        user =User.objects.get(username =Utilisateur.objects.using(bdd).get(mail =othussupprform.cleaned_data['contactsuoth']).username)
        uter =Utilisateur.objects.using(bdd).get(mail =othussupprform.cleaned_data['contactsuoth'])
        user_suppr(request, bdd, Utilisateur.objects.using(bdd).get(mail =othussupprform.cleaned_data['contactsuoth']).username)
        diffsupupdate(request, bdd, othussupprform.cleaned_data['contactsuoth'])
        user.delete()
        uter.delete()

        messages.info(request, _('Utilisateur supprimé avec succès'))
    # Fin de stuff about other authorized users

    # (la suppression éventuelle de l'utilisateur et du user est factorisée en fin de vue) ????

    if request.method =="POST":
        return HttpResponseRedirect(url)
    else:#request.method =="GET
    #La partie de code ci-dessous est reproduite dans la vue home(request, bdd) = Synchronisation de la base locale (utilisateurs) avec la base générale (users)
        for e in Utilisateur.objects.using(bdd).all():#1/2 création d'éventuels nouveaux users dans la base générale
            try:
                user =User.objects.get(username =e.username)
            except:
                user =User.objects.create_user(username =e.username, email =e.mail, password ="glass onion")

        #2/2 (see upper, this order is important)
        suffixe = "@" + str(bdd)
        for j in User.objects.all(): #Suppression d'users pour lesquels l'utilisateur a été supprimé de la base locale
            if j.username[-3:] ==suffixe:
                try:
                    utilisateur =Utilisateur.objects.using(bdd).get(username =j.username)
                except:
                    j.delete() #suppression dans la bdd générale

    return render(request, 'epl/admzauthusrs.html', locals())


@login_required
def globadm(request):

    """Global administration"""

    #contrôle d'accès ici
    if not request.user.is_staff:
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à l'administration générale"))
        return selectbdd(request)
    
#########################(Cette partie est reproduite de la même vue dans 'home' et 'selectbdd')######################
    """
    Création (dans la base de données principale) des users non encore enregistrés pour toutes les bases projets !
    """
    for i in [n for n in range(100)]:
        if os.path.isfile('{:02d}.db'.format(i)):
            for j in Utilisateur.objects.using('{:02d}'.format(i)).all():
                try:
                    usr =User.objects.get(username =j.username)
                except:
                    nwuser =User(is_superuser =0, username =j.username, email =j.mail, is_staff =0, is_active =1)
                    nwuser.save()
####################################################(fin)###########################################################

    k =logstatus(request)
    version =epl_version
    date =date_version
    host = str(request.get_host())

    return render(request, 'epl/globadm.html', locals())



def about(request):

    k =logstatus(request)
    version =epl_version
    date =date_version
    host = str(request.get_host())
    platform = os.uname()[0]
    noyau = os.uname()[2]
    distri = os.uname()[3]
    archi = os.uname()[4]
    
    return render(request, 'epl/about.html', locals())


def contactdev(request):

    k =logstatus(request)
    version =epl_version
    date =date_version
    host = str(request.get_host())
    url = "contactdev"

    global inletters, innumbers
    if request.method == "GET":
        chlist = range(len(numberlist))
        aleatindice = random.choices(chlist, k=1)[0]
        inletters = alphalist[aleatindice]
        innumbers = numberlist[aleatindice]
    else:#(POST)
        pass
    
    if k:
        class ContactForm(forms.Form):
            object_list = (("Demande d'information", _("Demande d'information")), ("Bug", _("Bug")),\
             ("Réclamation", _("Réclamation")), ("Suggestion", _("Suggestion")), ("Avis", _("Avis")),  ("Autre", _("Autre")))
            objet = forms.ChoiceField(required = True, widget=forms.Select, choices=object_list, label =_("Objet"))
            content = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': _("Donnez ici toutes les informations utiles.") + "\n" + "\n" + _("Vous pouvez dimensionner ce cadre à partir de son coin inférieur droit.")}), label =_("Votre message"))
            captcha = forms.CharField(required=True, widget=forms.TextInput(attrs={'size': '3'}), max_length=3, label =_("Prouvez que vous n'êtes pas un robot ; écrivez le nombre *** {} *** en chiffres").format(inletters))
    else:
        class ContactForm(forms.Form):
            object_list = (("Demande d'information", _("Demande d'information")), ("Bug", _("Bug")),\
             ("Réclamation", _("Réclamation")), ("Suggestion", _("Suggestion")), ("Avis", _("Avis")),  ("Autre", _("Autre")))
            objet = forms.ChoiceField(required = True, widget=forms.Select, choices=object_list, label =_("Objet"))
            email = forms.EmailField(required = True, label =_("Votre adresse mail de contact"))
            email_confirm =forms.EmailField(required = True, label =_("Confirmation de l'adresse mail"))
            content = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': _("Donnez ici toutes les informations utiles.") + "\n" + "\n" + _("Vous pouvez dimensionner ce cadre à partir de son coin inférieur droit.")}), label =_("Votre message"))
            captcha = forms.CharField(required=True, widget=forms.TextInput(attrs={'size': '3'}), max_length=3, label =_("Prouvez que vous n'êtes pas un robot ; écrivez le nombre *** {} *** en chiffres").format(inletters))

    form = ContactForm(request.POST or None)
    if form.is_valid():
        if not form.cleaned_data["captcha"] == innumbers or not form.cleaned_data["captcha"] == innumbers:
            messages.info(request, _("Le nombre saisi était erroné"))
            return HttpResponseRedirect(url)
        else:
            if k:
                recipient = request.user.email
                dest2 = [request.user.email]
            else:
                recipient = form.cleaned_data['email']
                recipient_confirm = form.cleaned_data['email_confirm']
                if not recipient ==recipient_confirm:
                    messages.info(request, _("échec de l'envoi : les emails n'étaient pas identiques"))
                    return HttpResponseRedirect(url)
                else:
                    dest2 = [recipient]
            objet2 = form.cleaned_data['objet']
            body = form.cleaned_data['content']
            subject2 = "[eplouribousse]" + " - " + objet2
            subject1 = subject2 + " - " + version + " - " + host
            message1 = subject1 + " :\n" + "\n" + body
            message2 = _("Votre message a bien été envoyé au développeur de l'application qui y répondra prochainement")\
             + ".\n" + _("Ne répondez pas au présent mail s'il vous plaît") + ".\n" + \
            _("Rappel de votre message") + " :\n" + \
              _("***** Début *****") + "\n" + _("Objet") +  " : " + subject2 + "\n" + \
                _("Corps") + " : " + "\n" + body + "\n" + _("*****  Fin  *****")
            dest1 = ["eplouribousse@gmail.com"]
            dest2 = [recipient]
            email1 = EmailMessage(subject1, message1, recipient, [], dest1,)
            email2 = EmailMessage(subject2, message2, replymail, [], dest2,)
            email1.send(fail_silently=False)
            email2.send(fail_silently=False)
            messages.info(request, _("Votre message a bien été envoyé. Un message de confirmation vient de vous être adressé à l'email indiqué."))
            messages.info(request, _("Pour des raisons de sécurité et de confidentialité, les destinataires sont en copie cachée."))
            return HttpResponseRedirect("/")

    return render(request, 'epl/contactdev.html', locals())


def webmstr(request):

    k =logstatus(request)
    version =epl_version
    date =date_version
    host = str(request.get_host())
    url = "webmaster"

    global inletters, innumbers
    if request.method == "GET":
        chlist = range(len(numberlist))
        aleatindice = random.choices(chlist, k=1)[0]
        inletters = alphalist[aleatindice]
        innumbers = numberlist[aleatindice]
    else:#(POST)
        pass
    
    if k:
        class ContactForm(forms.Form):
            object_list = (("Demande d'information", _("Demande d'information")), ("Bug", _("Bug")),\
             ("Réclamation", _("Réclamation")), ("Suggestion", _("Suggestion")), ("Avis", _("Avis")),  ("Autre", _("Autre")))
            objet = forms.ChoiceField(required = True, widget=forms.Select, choices=object_list, label =_("Objet"))
            content = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': _("Donnez ici toutes les informations utiles.") + "\n" + "\n" + _("Vous pouvez dimensionner ce cadre à partir de son coin inférieur droit.")}), label =_("Votre message"))
            captcha = forms.CharField(required=True, widget=forms.TextInput(attrs={'size': '3'}), max_length=3, label =_("Prouvez que vous n'êtes pas un robot ; écrivez le nombre *** {} *** en chiffres").format(inletters))
    else:
        class ContactForm(forms.Form):
            object_list = (("Demande d'information", _("Demande d'information")), ("Bug", _("Bug")),\
             ("Réclamation", _("Réclamation")), ("Suggestion", _("Suggestion")), ("Avis", _("Avis")),  ("Autre", _("Autre")))
            objet = forms.ChoiceField(required = True, widget=forms.Select, choices=object_list, label =_("Objet"))
            email = forms.EmailField(required = True, label =_("Votre adresse mail de contact"))
            email_confirm =forms.EmailField(required = True, label =_("Confirmation de l'adresse mail"))
            content = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': _("Donnez ici toutes les informations utiles.") + "\n" + "\n" + _("Vous pouvez dimensionner ce cadre à partir de son coin inférieur droit.")}), label =_("Votre message"))
            captcha = forms.CharField(required=True, widget=forms.TextInput(attrs={'size': '3'}), max_length=3, label =_("Prouvez que vous n'êtes pas un robot ; écrivez le nombre *** {} *** en chiffres").format(inletters))
            
    form = ContactForm(request.POST or None)
    if form.is_valid():
        if not form.cleaned_data["captcha"] == innumbers or not form.cleaned_data["captcha"] == innumbers:
            messages.info(request, _("Le nombre saisi était erroné"))
            return redirect(url)
        else:
            if k:
                recipient = request.user.email
                dest2 = [request.user.email]
            else:
                recipient = form.cleaned_data['email']
                recipient_confirm = form.cleaned_data['email_confirm']
                if not recipient ==recipient_confirm:
                    messages.info(request, _("échec de l'envoi : les emails n'étaient pas identiques"))
                    return HttpResponseRedirect(url)
                else:
                    dest2 = [recipient]
            objet2 = form.cleaned_data['objet']
            body = form.cleaned_data['content']
            subject2 = "[eplouribousse]" + " - " + objet2
            subject1 = subject2 + " - " + version + " - " + host
            message1 = subject1 + " :\n" + "\n" + body
            message2 = _("Votre message a bien été envoyé au webmaster qui y répondra prochainement") + \
            ".\n" + _("Ne répondez pas au présent mail s'il vous plaît") + ".\n" \
             + _("Rappel de votre message") + " :\n" + _("***** Début *****") + "\n" + _("Objet") +  " : " + subject2 + \
            "\n" + _("Corps") + " : " + "\n" + body + "\n" + _("*****  Fin  *****")
            dest1 = [webmaster]
            dest2 = [recipient]
            email1 = EmailMessage(subject1, message1, recipient, [], dest1,)
            email2 = EmailMessage(subject2, message2, replymail, [], dest2,)
            email1.send(fail_silently=False)
            email2.send(fail_silently=False)
            messages.info(request, _("Votre message a bien été envoyé. Un message de confirmation vient de vous être adressé à l'email indiqué."))
            messages.info(request, _("Pour des raisons de sécurité et de confidentialité, les destinataires sont en copie cachée."))
            return HttpResponseRedirect("/")

    return render(request, 'epl/webmaster.html', locals())

@edmode3
def projmstr(request, bdd):

    k =logstatus(request)
    version =epl_version
    date =date_version
    host = str(request.get_host())
    project = Project.objects.using(bdd).all().order_by('pk')[0].name
    url = "/" + bdd + "/projectmaster"
    dest1 =[]
    for bddadm in BddAdmin.objects.using(bdd).all():
        dest1.append(bddadm.contact)

    global inletters, innumbers
    if request.method == "GET":
        chlist = range(len(numberlist))
        aleatindice = random.choices(chlist, k=1)[0]
        inletters = alphalist[aleatindice]
        innumbers = numberlist[aleatindice]
    else:#(POST)
        pass
    
    if k:
        class ContactForm(forms.Form):
            object_list = (("Signalement d'une anomalie", _("Signalement d'une anomalie")), ("Ajout, modification ou suppression de motifs d'exclusion", _("Ajout, modification ou suppression de motifs d'exclusion")), ("Ajout, modification ou suppression de correspondants d'une bibliothèque", _("Ajout, modification ou suppression de correspondants d'une bibliothèque")), ("Ajout, modification ou suppression d'administrateurs", _("Ajout, modification ou suppression d'administrateurs")), ("Ajout, modification ou suppression d'utilisateurs", _("Ajout, modification ou suppression d'utilisateurs")), ("Info d'un des administrateurs du projet à ses co-administrateurs", _("Info d'un des administrateurs du projet à ses co-administrateurs")), ("Signaler un manquement aux règles de confidentialité", _("Signaler un manquement aux règles de confidentialité")), ("Autre", _("Autre")))
            objet = forms.ChoiceField(required = True, widget=forms.Select, choices=object_list, label =_("Objet"))
            content = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': _("Donnez ici toutes les informations utiles.") + "\n" + "\n" + _("Vous pouvez dimensionner ce cadre à partir de son coin inférieur droit.")}), label =_("Votre message"))
            captcha = forms.CharField(required=True, widget=forms.TextInput(attrs={'size': '3'}), max_length=3, label =_("Prouvez que vous n'êtes pas un robot ; écrivez le nombre *** {} *** en chiffres").format(inletters))
    else:
        class ContactForm(forms.Form):
            object_list = (("Signalement d'une anomalie", _("Signalement d'une anomalie")), \
            ("M'ajouter à la liste de diffusion", _("M'ajouter à la liste de diffusion")), \
            ("Me supprimer de la liste de diffusion", _("Me supprimer de la liste de diffusion")), \
            ("Ajout, modification ou suppression de motifs d'exclusion", _("Ajout, modification ou suppression de motifs d'exclusion")),\
             ("Ajout, modification ou suppression de correspondants d'une bibliothèque", _("Ajout, modification ou suppression de correspondants d'une bibliothèque")), \
             ("Ajout, modification ou suppression d'administrateurs", _("Ajout, modification ou suppression d'administrateurs")), \
             ("Ajout, modification ou suppression d'utilisateurs", _("Ajout, modification ou suppression d'utilisateurs")), \
             ("Info d'un des administrateurs du projet à ses co-administrateurs", _("Info d'un des administrateurs du projet à ses co-administrateurs")), \
            ("Signaler un manquement aux règles de confidentialité", _("Signaler un manquement aux règles de confidentialité")), \
             ("Autre", _("Autre")))
            objet = forms.ChoiceField(required = True, widget=forms.Select, choices=object_list, label =_("Objet"))
            email = forms.EmailField(required = True, label =_("Votre adresse mail de contact"))
            email_confirm =forms.EmailField(required = True, label =_("Confirmation de l'adresse mail"))
            content = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': _("Donnez ici toutes les informations utiles.") + "\n" + "\n" + _("Vous pouvez dimensionner ce cadre à partir de son coin inférieur droit.")}), label =_("Votre message"))
            captcha = forms.CharField(required=True, widget=forms.TextInput(attrs={'size': '3'}), max_length=3, label =_("Prouvez que vous n'êtes pas un robot ; écrivez le nombre *** {} *** en chiffres").format(inletters))

    form = ContactForm(request.POST or None)
    if form.is_valid():
        if not form.cleaned_data["captcha"] == innumbers or not form.cleaned_data["captcha"] == innumbers:
            messages.info(request, _("Le nombre saisi était erroné"))
            return redirect(url)
        else:
            if k:
                dest2 =[request.user.email]
                recipient = request.user.email
            else:
                recipient = form.cleaned_data['email']
                recipient_confirm = form.cleaned_data['email_confirm']
                if not recipient ==recipient_confirm:
                    messages.info(request, _("échec de l'envoi : les emails n'étaient pas identiques"))
                    return HttpResponseRedirect(url)
                else:
                    dest2 = [recipient]
            objet2 = form.cleaned_data['objet']
            body = form.cleaned_data['content']
            subject2 = "[eplouribousse" + " @" + bdd + "]" + " - " + objet2
            subject1 = subject2 + " - " + version + " - " + host
            message1 = subject1 + " :\n" + "\n" + body
            message2 = _("Votre message a bien été envoyé à l'administrateur du projet qui y répondra prochainement")\
             + ".\n" + _("Ne répondez pas au présent mail s'il vous plaît") + ".\n" + _("Rappel de votre message") + " :\n" + \
                _("***** Début *****") + "\n" + _("Objet") +  " : " + subject2 + \
                "\n" + _("Corps") + " : " + "\n" + body + "\n" + _("*****  Fin  *****")
            email1 = EmailMessage(subject1, message1, recipient, [], dest1,)
            email2 = EmailMessage(subject2, message2, replymail, [], dest2,)
            email1.send(fail_silently=False)
            email2.send(fail_silently=False)
            messages.info(request, _("Votre message a bien été envoyé. Un message de confirmation vient de vous être adressé à l'email indiqué."))
            messages.info(request, _("Pour des raisons de sécurité et de confidentialité, les destinataires sont en copie cachée."))
            return HttpResponseRedirect("/" + bdd)

    return render(request, 'epl/projmaster.html', locals())


@edmode4
def router(request, bdd, lid):
    
    try:
        if Feature.objects.using(bdd).get(libname =Library.objects.using(bdd).get(lid =lid).name):
            newestfeature =Feature.objects.using(bdd).get(libname =Library.objects.using(bdd).get(lid =lid).name)
            key =newestfeature.feaname.split('$')
            if key[0] =="10":
                return ranktotake(request, bdd, lid, 'title')
            elif key[0] =="11":
                return xranktotake(request, bdd, lid, key[1], 'title')
            elif key[0] =="12":
                return modifranklist(request, bdd, lid, 'title')
            elif key[0] =="20":
                return arbitration(request, bdd, lid, 'title')
            elif key[0] =="21":
                return xarbitration(request, bdd, lid, key[1], 'title')
            elif key[0] =="22":
                return x1arb(request, bdd, lid, key[1], 'title')
            elif key[0] =="23":
                return x0arb(request, bdd, lid, key[1], 'title')
            elif key[0] =="24":
                return arbrk1(request, bdd, lid, 'title')
            elif key[0] =="25":
                return arbnork1(request, bdd, lid, 'title')
            elif key[0] =="30":
                return instrtodo(request, bdd, lid, 'title')
            elif key[0] =="31":
                return xinstrlist(request, bdd, lid, key[1], 'title')
            elif key[0] =="32":
                return xckbd(request, bdd, eval(key[1]))
            elif key[0] =="33":
                return xcknbd(request, bdd, eval(key[1]))
            elif key[0] =="34":
                return xckall(request, bdd, eval(key[1]))
            elif key[0] =="35":
                return instroneb(request, bdd, lid, 'title')
            elif key[0] =="36":
                return instrotherb(request, bdd, lid, 'title')
            elif key[0] =="37":
                return instronenotb(request, bdd, lid, 'title')
            elif key[0] =="38":
                return instrothernotb(request, bdd, lid, 'title')
            elif key[0] =="40":
                return tobeedited(request, bdd, lid, 'title')
            elif key[0] =="41":
                return mothered(request, bdd, lid, 'title')
            elif key[0] =="42":
                return notmothered(request, bdd, lid, 'title')
            elif key[0] =="43":
                return xmothered(request, bdd, lid, key[1], 'title')
            elif key[0] =="44":
                return xnotmothered(request, bdd, lid, key[1], 'title')
            elif key[0] =="50":
                return xnotmothered(request, bdd, lid, key[1], 'title')
            elif key[0] =="60":
                return xnotmothered(request, bdd, lid, key[1], 'title')
            elif key[0] =="70":
                return xnotmothered(request, bdd, lid, key[1], 'title')
            elif key[0] =="71":
                return xnotmothered(request, bdd, lid, key[1], 'title')
            else:
                messages.info(request, _("Il n'y avait pas de liste à laquelle retourner."))
                return homme(request, bdd)
    except:
        messages.info(request, _("Il n'y avait pas de liste à laquelle retourner."))
        return home(request, bdd)

    return render(request, 'epl/router.html', locals())


def lang(request):
    k =logstatus(request)
    version =epl_version
    
    redirect_to ="/"

    return render(request, 'epl/language.html', locals())


def logout_view(request):

    "Homepage special disconnected"

    logout(request)

    # Redirect to a success page.

    version =epl_version

    return render(request, 'epl/disconnect.html', locals())

@edmode5
def notintime(request, bdd, sid, lid):

    k =logstatus(request)
    version =epl_version

    library = Library.objects.using(bdd).get(lid = lid).name
    if lid =="999999999":
        try:
            title = ItemRecord.objects.using(bdd).get(sid =sid, rank =1).title
        except:
            title = sid
    else:
        title = ItemRecord.objects.using(bdd).get(sid =sid, lid =lid).title
    return render(request, 'epl/notintime.html', locals())

@edmode3
def indicators(request, bdd):

    k =logstatus(request)
    version =epl_version

    #Indicators :

    #Number of rankings (exclusions included) :
    rkall = len(ItemRecord.objects.using(bdd).exclude(rank =99))

    #Number of rankings (exclusions excluded) :
    rkright = len(ItemRecord.objects.using(bdd).exclude(rank =99).exclude(rank =0))

    #Number of exclusions (collections) :
    exclus = len(ItemRecord.objects.using(bdd).filter(rank =0))

    #Number of collections :
    coll = len(ItemRecord.objects.using(bdd).all())

    #number of libraries :
    nlib = len(Library.objects.using(bdd).all())

    #Exclusions details
    dict ={}
    EXCLUSION_CHOICES = ('', _('')),
    for e in list(ItemRecord.objects.using(bdd).filter(rank =0).exclude(excl ="Autre (Commenter)").values_list('excl', flat =True).distinct()):
        EXCLUSION_CHOICES += (e, e),
    EXCLUSION_CHOICES += ("Autre (Commenter)", _("Autre (Commenter)")),
    for e in EXCLUSION_CHOICES:
        exclusion =str(e[0])
        value =len(ItemRecord.objects.using(bdd).filter(excl =e[0]))
        dict[exclusion] =value
    del dict['']

    #Collections involved in arbitration for claiming 1st rank and number of serials concerned
    c1st, s1st =0,[]
    for i in ItemRecord.objects.using(bdd).filter(rank =1, status =0):
        if len(ItemRecord.objects.using(bdd).filter(rank =1, sid =i.sid)) >1:
            c1st +=1
            if i.sid not in s1st:
                s1st.append(i.sid)
    s1st = len(s1st)

    #Collections and ressources involved in arbitration for 1st rank not claimed by any of the libraries
    cnone, snone =0,[]
    for i in ItemRecord.objects.using(bdd).exclude(rank =0).exclude(rank =1).exclude(rank =99):
        if len(ItemRecord.objects.using(bdd).filter(sid =i.sid, rank =99)) ==0 and \
        len(ItemRecord.objects.using(bdd).filter(sid =i.sid, rank =1)) ==0 and \
        len(ItemRecord.objects.using(bdd).filter(sid =i.sid).exclude(rank =0)) >1:
            cnone +=1
            if i.sid not in snone:
                snone.append(i.sid)
    snone = len(snone)

    #Ressources involved in arbitration for either of the two reasons
    stotal = s1st + snone

    #Number of potential candidates :
    cand =[]
    dupl =[]
    tripl =[]
    qudrpl =[]
    isol =[]
    realcandress =[]
    realisol =[]
    for e in ItemRecord.objects.using(bdd).all():
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid)) >1 and not e.sid in cand:
            cand.append(e.sid)
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid).exclude(rank =0)) >1 and not e.sid in realcandress:
            realcandress.append(e.sid)
        #from which strict duplicates :
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid).exclude(rank =0)) ==2 and not e.sid in dupl:
            dupl.append(e.sid)
        #triplets :
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid).exclude(rank =0)) ==3 and not e.sid in tripl:
            tripl.append(e.sid)
        #quadruplets :
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid).exclude(rank =0)) ==4 and not e.sid in qudrpl:
            qudrpl.append(e.sid)
        #Unicas :
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid)) ==1 and not e.sid in isol:
            isol.append(e.sid)
        #Unicas after exclusions
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid).exclude(rank =0)) ==1 and not e.sid in realisol:
            realisol.append(e.sid)

    cand = len(cand)
    dupl = len(dupl)
    realcandress =len(realcandress)
    percentdupl = round(100*dupl/realcandress)
    tripl = len(tripl)
    percenttripl = round(100*tripl/realcandress)
    qudrpl = len(qudrpl)
    percentqudrpl = round(100*qudrpl/realcandress)
    isol = len(isol)
    pluspl =realcandress - (dupl + tripl + qudrpl)
    percentpluspl = round(100*pluspl/realcandress)
    realisol =len(realisol)

    #candidate collections :
    candcoll =coll - isol

    #Number of descarded ressources for exclusion reason :
    discard =[]
    for i in ItemRecord.objects.using(bdd).filter(rank =0):
        if len(ItemRecord.objects.using(bdd).filter(sid =i.sid).exclude(rank =0)) ==1 and not i.sid in discard:
            discard.append(i.sid)
    realcandcoll, sidlist =0, []
    #Number of real candidates (collections)
    for r in ItemRecord.objects.using(bdd).all():
        if r.sid not in sidlist and r.sid not in discard:
            sidlist.append(r.sid)
            realcandcoll +=len(ItemRecord.objects.using(bdd).filter(sid =r.sid).exclude(rank =0))
    discard = len(discard)

    #Number of ressources whose instruction of bound elements may begin or is ongoing :
    bd = len(ItemRecord.objects.using(bdd).filter(rank =1).exclude(status =0).exclude(status =3).exclude(status =4).exclude(status =5).exclude(status =6))#status in [1,2]

    #Number of ressources whose instruction of not bound elements may begin or is ongoing :
    notbd = len(ItemRecord.objects.using(bdd).filter(rank =1).exclude(status =0).exclude(status =1).exclude(status =2).exclude(status =5).exclude(status =6))#status in [3,4]

    #Number of ressources completely instructed :
    fullinstr = len(ItemRecord.objects.using(bdd).filter(rank =1, status =5))

    #Number of failing sheets :
    fail1, fail2 =0, 0
    for i in ItemRecord.objects.using(bdd).filter(status =6, rank =1):
        if len(Instruction.objects.using(bdd).filter(sid = i.sid, name = "checker")):
            fail2 +=1
        else:
            fail1 +=1
    fail = fail1 + fail2

    #Number of instructions :
    instr = len(Instruction.objects.using(bdd).all())

    #Fiches dont l'instruction peut être complétée
    incomp = bd + notbd

    #Number of real candidates (ressources)
    realcand =cand - discard# (=realcandress)

    #Ressource pour lesquelles au moins un positionnement n'a jamais encore été pris
    stocomp =realcandress - (fullinstr + incomp + fail + stotal)
    
    #Absolute achievement :
    absolute_real = round(10000*(fullinstr + discard)/cand)/100

    #Relative achievement :
    relative_real = round(10000*fullinstr/realcandress)/100

    x1 =[stocomp, stotal, discard, bd, notbd, fullinstr, fail]
    uri1 = get_pie(x1, _("Ressources candidates au départ"), labels =[_("positionnement") + " ({})".format(stocomp), _("arbitrages") + " ({})".format(stotal), _("écartées par excl. de coll.") + " ({})".format(discard), _("instr° reliés") + " ({})".format(bd), _("instr° non reliés") + " ({})".format(notbd), _("instr° achevée") + " ({})".format(fullinstr), _("fiches erronées") + " ({})".format(fail)])
    
    xx1 =[stocomp, stotal, bd, notbd, fullinstr, fail]
    urix1 = get_pie(xx1, _("Ressources effectivement candidates"), labels =[_("positionnement") + " ({})".format(stocomp), _("arbitrages") + " ({})".format(stotal), _("instr° reliés") + " ({})".format(bd), _("instr° non reliés") + " ({})".format(notbd), _("instr° achevée") + " ({})".format(fullinstr), _("fiches erronées") + " ({})".format(fail)])
    
    gh = fullinstr + discard
    gi = cand - gh
    x2 =[gh, gi]
    uri2 = get_pie(x2, "Avancement absolu", labels =[_("plus à instruire") + " ({})".format(gh), _("à instruire") + " ({})".format(gi)])
    
    gj = fullinstr
    gk = realcandress - fullinstr
    x3=[gj, gk]
    uri3 = get_pie(x3, "Avancement relatif", labels =[_("instruit") + " ({})".format(gj), _("à instruire") + " ({})".format(gk)])


    x4 =[dupl, tripl, qudrpl, pluspl]
    uri4 = get_pie(x4, _("Ressources effectivement candidates"), labels =[_("doublons") + " ({})".format(dupl), _("triplons") + " ({})".format(tripl), _("quadruplons") + " ({})".format(qudrpl), _("plus") + " ({})".format(pluspl)])
    
    qs =[Library.objects.using(bdd).get(name ="checker")]
    for l in Library.objects.using(bdd).all().exclude(name ="checker").order_by("name"):
        qs.append(l)
    x5, y5 =[], []
    for libmt in qs:
        x5.append(libmt.name)
        y5.append(len(Instruction.objects.using(bdd).filter(name =libmt.name)))
#    uri5 =get_scatter(x5, y5, _(""), _(""), _("nbr d'instr."))
    try:
#        uri5 =get_pie(y5, _("nbr d'instr."), labels =[e.name + " ({}%)".format(round(10000*len(Instruction.objects.using(bdd).filter(name =e.name))/len(Instruction.objects.using(bdd).all()))/100) for e in qs])
        uri5 =get_pie(y5, _("Instructions réalisées (lignes)"), labels =[e.name + " ({})".format(len(Instruction.objects.using(bdd).filter(name =e.name))) for e in qs])
    except: # (division by zero)
        pass

    sid2, sid4 =[], []
    for it in ItemRecord.objects.using(bdd).filter(status =2):
        if not len(ItemRecord.objects.using(bdd).filter(sid =it.sid, status =1)) and not len(ItemRecord.objects.using(bdd).filter(sid =it.sid, status =3)) and not it.sid in sid2:
            sid2.append(it.sid)
    for it in ItemRecord.objects.using(bdd).filter(status =4):
        if not len(ItemRecord.objects.using(bdd).filter(sid =it.sid, status =3)) and not it.sid in sid4:
            sid4.append(it.sid)
    check = len(sid2) + len(sid4)
    qs =[]
    x6, y61, y63, y613 =["admin", "checker"], [fail1, len(sid2)], [fail2, len(sid4)], [fail, check] 
    for l in Library.objects.using(bdd).all().exclude(name ="checker").order_by("name"):
        qs.append(l)
    for libmt in qs:
        x6.append(libmt.name)
        y61.append(len(list(ItemRecord.objects.using(bdd).filter(lid =libmt.lid, status =1))))
        y63.append(len(list(ItemRecord.objects.using(bdd).filter(lid =libmt.lid, status =3))))
        y613.append(len(list(ItemRecord.objects.using(bdd).filter(lid =libmt.lid, status =1))) + len(list(ItemRecord.objects.using(bdd).filter(lid =libmt.lid, status =3))))
    uri6 =multipleplot(x6, y61, y63, y613, _("reliés"), _("non reliés"), _("total"), _(""), _(""), _("Fiches à traiter") )

    qs =[]
    for l in Library.objects.using(bdd).all().exclude(name ="checker").order_by("name"):
        qs.append(l)
    x7, y7 =[], []
    for libmt in qs:
        x7.append(libmt.name)
        pos, nopos =0, 0
        for item in ItemRecord.objects.using(bdd).filter(lid =libmt.lid):
            if not item.rank ==99 and len(ItemRecord.objects.using(bdd).filter(sid =item.sid).exclude(rank =0)) >1:
                pos +=1
            elif item.rank ==99 and len(ItemRecord.objects.using(bdd).filter(sid =item.sid).exclude(rank =0)) >1:
                nopos +=1
        y7.append(round(10000*pos/(pos + nopos)/100))
    uri7 =get_scatter(x7, y7, _(""), _(""), _("Positionnements réalisés en % des rattachements"))

    libch = ('',''),
    if Library.objects.using(bdd).all().exclude(lid ="999999999"):
        for l in Library.objects.using(bdd).all().exclude(lid ="999999999").order_by('name'):
            libch += (l.name, l.name),

    class LibForm(forms.Form):
        name = forms.ChoiceField(required = False, widget=forms.Select, choices=libch, label =_("Filtrer avec les collections d'une bibliothèque"))

    if request.method =="GET":
        form = LibForm()
    else:
        form = LibForm(request.POST or None)
        if form.is_valid():
            lib = form.cleaned_data['name']
            if lib:
                lid = Library.objects.using(bdd).get(name =form.cleaned_data['name']).lid
                return indicators_x(request, bdd, lid)
            else:
                pass
        else:
            return HttpResponse("Invalid form")

    return render(request, 'epl/indicators.html', locals())


@edmode4
def indicators_x(request, bdd, lid):

    k =logstatus(request)
    version =epl_version
    
    libname =Library.objects.using(bdd).get(lid =lid).name

    #Indicators :

    #Number of rankings (exclusions included) :
    rkall = len([item for item in list(ItemRecord.objects.using(bdd).exclude(rank =99)) if ItemRecord.objects.using(bdd).filter(lid =lid, sid =item.sid)])

    #Number of rankings (exclusions excluded) :
    rkright = len([item for item in list(ItemRecord.objects.using(bdd).exclude(rank =99).exclude(rank =0)) if ItemRecord.objects.using(bdd).filter(lid =lid, sid =item.sid)])
    
    #Number of exclusions (collections) :
    exclus = len([item for item in list(ItemRecord.objects.using(bdd).filter(rank =0)) if ItemRecord.objects.using(bdd).filter(lid =lid, sid =item.sid)])

    #Number of collections :
    coll = len([item for item in list(ItemRecord.objects.using(bdd).all()) if ItemRecord.objects.using(bdd).filter(lid =lid, sid =item.sid).exclude(rank =0)])

    #number of libraries :
    nlib = len(Library.objects.using(bdd).all())

    #Exclusions details
    dict ={}
    EXCLUSION_CHOICES = ('', _('')),
    for e in list(ItemRecord.objects.using(bdd).filter(rank =0).exclude(excl ="Autre (Commenter)").values_list('excl', flat =True).distinct()):
        EXCLUSION_CHOICES += (e, e),
    EXCLUSION_CHOICES += ("Autre (Commenter)", _("Autre (Commenter)")),
    for e in EXCLUSION_CHOICES:
        exclusion =str(e[0])
        value =len([item for item in list(ItemRecord.objects.using(bdd).filter(excl =e[0])) if ItemRecord.objects.using(bdd).filter(lid =lid, sid =item.sid)])
        dict[exclusion] =value
    del dict['']

    #Collections involved in arbitration for claiming 1st rank and number of serials concerned
    c1st, s1st =0,[]
    for i in ItemRecord.objects.using(bdd).filter(rank =1, status =0):
        if len(ItemRecord.objects.using(bdd).filter(rank =1, sid =i.sid)) >1 and len(ItemRecord.objects.using(bdd).filter(sid =i.sid, lid =lid).exclude(rank =0)):
            c1st +=1
            if i.sid not in s1st:
                s1st.append(i.sid)
    s1st = len(s1st)

    #Collections and ressources involved in arbitration for 1st rank not claimed by any of the libraries
    cnone, snone =0,[]
    for i in ItemRecord.objects.using(bdd).exclude(rank =0).exclude(rank =1).exclude(rank =99):
        if len(ItemRecord.objects.using(bdd).filter(sid =i.sid, rank =99)) ==0 and \
        len(ItemRecord.objects.using(bdd).filter(sid =i.sid, rank =1)) ==0 and \
        len(ItemRecord.objects.using(bdd).filter(sid =i.sid).exclude(rank =0)) >1 and len(ItemRecord.objects.using(bdd).filter(sid =i.sid, lid =lid).exclude(rank =0)) :
            cnone +=1
            if i.sid not in snone:
                snone.append(i.sid)
    snone = len(snone)

    #Ressources involved in arbitration for either of the two reasons
    stotal = s1st + snone

    #Number of potential candidates :
    cand =[]
    dupl =[]
    tripl =[]
    qudrpl =[]
    isol =[]
    realcandress =[]
    realisol =[]
    for e in ItemRecord.objects.using(bdd).all():
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid)) >1 and len(ItemRecord.objects.using(bdd).filter(sid =e.sid, lid =lid)) and not e.sid in cand:
            cand.append(e.sid)
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid).exclude(rank =0)) >1 and len(ItemRecord.objects.using(bdd).filter(sid =e.sid, lid =lid).exclude(rank =0)) and not e.sid in realcandress:
            realcandress.append(e.sid)
        #from which strict duplicates :
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid).exclude(rank =0)) ==2 and len(ItemRecord.objects.using(bdd).filter(sid =e.sid, lid =lid).exclude(rank =0)) and not e.sid in dupl:
            dupl.append(e.sid)
        #triplets :
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid).exclude(rank =0)) ==3 and len(ItemRecord.objects.using(bdd).filter(sid =e.sid, lid =lid).exclude(rank =0)) and not e.sid in tripl:
            tripl.append(e.sid)
        #quadruplets :
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid).exclude(rank =0)) ==4 and len(ItemRecord.objects.using(bdd).filter(sid =e.sid, lid =lid).exclude(rank =0)) and not e.sid in qudrpl:
            qudrpl.append(e.sid)
        #Unicas :
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid)) ==1 and len(ItemRecord.objects.using(bdd).filter(sid =e.sid, lid =lid)) and not e.sid in isol:
            isol.append(e.sid)
        #Unicas after exclusions
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid).exclude(rank =0)) ==1 and len(ItemRecord.objects.using(bdd).filter(sid =e.sid, lid =lid)) and not e.sid in realisol:
            realisol.append(e.sid)

    cand = len(cand)
    dupl = len(dupl)
    realcandress =len(realcandress)
    percentdupl = round(100*dupl/realcandress)
    tripl = len(tripl)
    percenttripl = round(100*tripl/realcandress)
    qudrpl = len(qudrpl)
    percentqudrpl = round(100*qudrpl/realcandress)
    isol = len(isol)
    pluspl =realcandress - (dupl + tripl + qudrpl)
    percentpluspl = round(100*pluspl/realcandress)
    realisol =len(realisol)

    #candidate collections :
    candcoll =coll - isol

    #Number of descarded ressources for exclusion reason :
    discard =[]
    for i in ItemRecord.objects.using(bdd).filter(rank =0):
        if len(ItemRecord.objects.using(bdd).filter(sid =i.sid).exclude(rank =0)) ==1 and len(ItemRecord.objects.using(bdd).filter(sid =i.sid, lid =lid)) and not i.sid in discard:
            discard.append(i.sid)
    realcandcoll, sidlist =0, []
    #Number of real candidates (collections)
    for r in ItemRecord.objects.using(bdd).all():
        if r.sid not in sidlist and r.sid not in discard:
            sidlist.append(r.sid)
            realcandcoll +=len([item for item in list(ItemRecord.objects.using(bdd).filter(sid =r.sid).exclude(rank =0)) if ItemRecord.objects.using(bdd).filter(lid =lid, sid =item.sid).exclude(rank =0)])
    discard = len(discard)

    #Number of ressources whose instruction of bound elements may begin or is ongoing :
    bd = len([item for item in list(ItemRecord.objects.using(bdd).filter(rank =1).exclude(status =0).exclude(status =3).exclude(status =4).exclude(status =5).exclude(status =6)) if ItemRecord.objects.using(bdd).filter(lid =lid, sid =item.sid).exclude(rank =0)])

    #Number of ressources whose instruction of not bound elements may begin or is ongoing :
    notbd = len([item for item in list(ItemRecord.objects.using(bdd).filter(rank =1).exclude(status =0).exclude(status =1).exclude(status =2).exclude(status =5).exclude(status =6)) if ItemRecord.objects.using(bdd).filter(lid =lid, sid =item.sid).exclude(rank =0)])

    #Number of ressources completely instructed :
    fullinstr = len([item for item in list(ItemRecord.objects.using(bdd).filter(rank =1, status =5)) if ItemRecord.objects.using(bdd).filter(lid =lid, sid =item.sid).exclude(rank =0)])

    #Number of failing sheets :
    fail1, fail2 =0, 0
    for i in ItemRecord.objects.using(bdd).filter(status =6, rank =1):
        if len(Instruction.objects.using(bdd).filter(sid = i.sid, name = "checker")) and len(ItemRecord.objects.using(bdd).filter(sid =i.sid, lid =lid).exclude(rank =0)):
            fail2 +=1
        elif not len(Instruction.objects.using(bdd).filter(sid = i.sid, name = "checker")) and len(ItemRecord.objects.using(bdd).filter(sid =i.sid, lid =lid).exclude(rank =0)):
            fail1 +=1
    fail = fail1 + fail2

    #Number of instructions :
    instr = len([instr for instr in list(Instruction.objects.using(bdd).all()) if ItemRecord.objects.using(bdd).filter(lid =lid, sid =instr.sid).exclude(rank =0)])

    #Fiches dont l'instruction peut être complétée
    incomp = bd + notbd

#    #Number of real candidates (ressources)
#    realcand =cand - discard# (=realcandress)
    
    #Ressource pour lesquelles au moins un positionnement n'a jamais encore été pris
    stocomp =realcandress - (fullinstr + incomp + fail + stotal)
    
    #Absolute achievement :
    absolute_real = round(10000*(fullinstr + discard)/cand)/100

    #Relative achievement :
    relative_real = round(10000*fullinstr/realcandress)/100

    x1 =[stocomp, stotal, discard, bd, notbd, fullinstr, fail]
    uri1 = get_pie(x1, _("Ressources candidates au départ"), labels =[_("positionnement") + " ({})".format(stocomp), _("arbitrages") + " ({})".format(stotal), _("écartées par excl. de coll.") + " ({})".format(discard), _("instr° reliés") + " ({})".format(bd), _("instr° non reliés") + " ({})".format(notbd), _("instr° achevée") + " ({})".format(fullinstr), _("fiches erronées") + " ({})".format(fail)])
    
    xx1 =[stocomp, stotal, bd, notbd, fullinstr, fail]
    urix1 = get_pie(xx1, _("Ressources effectivement candidates (*)"), labels =[_("positionnement") + " ({})".format(stocomp), _("arbitrages") + " ({})".format(stotal), _("instr° reliés") + " ({})".format(bd), _("instr° non reliés") + " ({})".format(notbd), _("instr° achevée") + " ({})".format(fullinstr), _("fiches erronées") + " ({})".format(fail)])
    
    gh = fullinstr + discard
    gi = cand - gh
    x2 =[gh, gi]
    uri2 = get_pie(x2, "Avancement absolu", labels =[_("plus à instruire") + " ({})".format(gh), _("à instruire") + " ({})".format(gi)])
    
    gj = fullinstr
    gk = realcandress - fullinstr
    x3=[gj, gk]
    uri3 = get_pie(x3, "Avancement relatif (*)", labels =[_("instruit") + " ({})".format(gj), _("à instruire") + " ({})".format(gk)])


    x4 =[dupl, tripl, qudrpl, pluspl]
    uri4 = get_pie(x4, _("Ressources effectivement candidates (*)"), labels =[_("doublons") + " ({})".format(dupl), _("triplons") + " ({})".format(tripl), _("quadruplons") + " ({})".format(qudrpl), _("plus") + " ({})".format(pluspl)])
    
    qs =[Library.objects.using(bdd).get(name ="checker")]
    for l in Library.objects.using(bdd).all().exclude(name ="checker").order_by("name"):
        qs.append(l)
    x5, y5 =[], []
    for libmt in qs:
        x5.append(libmt.name)
        y5.append(len([instr for instr in list(Instruction.objects.using(bdd).filter(name =libmt.name)) if ItemRecord.objects.using(bdd).filter(lid =lid, sid =instr.sid).exclude(rank =0)]))
        
        
#    uri5 =get_scatter(x5, y5, _(""), _(""), _("nbr d'instr."))
    try:
#        uri5 =get_pie(y5, _("nbr d'instr."), labels =[e.name + " ({}%)".format(round(10000*len(Instruction.objects.using(bdd).filter(name =e.name))/len(Instruction.objects.using(bdd).all()))/100) for e in qs])
        uri5 =get_pie(y5, _("Instructions réalisées (lignes) (*)"), labels =[e.name + " ({})".format(len([instr for instr in list(Instruction.objects.using(bdd).filter(name =e.name)) if ItemRecord.objects.using(bdd).filter(lid =lid, sid =instr.sid).exclude(rank =0)])) for e in qs])
    except: # (division by zero)
        pass
    
    sid2, sid4 =[], []
    for it in ItemRecord.objects.using(bdd).filter(status =2):
        if not len(ItemRecord.objects.using(bdd).filter(sid =it.sid, status =1)) and not len(ItemRecord.objects.using(bdd).filter(sid =it.sid, status =3)) and not it.sid in sid2:
            sid2.append(it.sid)
    for it in ItemRecord.objects.using(bdd).filter(status =4):
        if not len(ItemRecord.objects.using(bdd).filter(sid =it.sid, status =3)) and not it.sid in sid4:
            sid4.append(it.sid)
    check = len(sid2) + len(sid4)
    qs =[]
    x6, y61, y63, y613 =["admin", "checker"], [fail1, len(sid2)], [fail2, len(sid4)], [fail, check] 
    for l in Library.objects.using(bdd).all().exclude(name ="checker").order_by("name"):
        qs.append(l)
    for libmt in qs:
        x6.append(libmt.name)
        y61.append(len([item for item in list(ItemRecord.objects.using(bdd).filter(lid =libmt.lid, status =1)) if ItemRecord.objects.using(bdd).filter(lid =lid, sid =item.sid).exclude(rank =0)]))        
        y63.append(len([item for item in list(ItemRecord.objects.using(bdd).filter(lid =libmt.lid, status =3)) if ItemRecord.objects.using(bdd).filter(lid =lid, sid =item.sid).exclude(rank =0)]))
        y613.append(len([item for item in list(ItemRecord.objects.using(bdd).filter(lid =libmt.lid, status =1)) if ItemRecord.objects.using(bdd).filter(lid =lid, sid =item.sid).exclude(rank =0)]) + len([item for item in list(ItemRecord.objects.using(bdd).filter(lid =libmt.lid, status =3)) if ItemRecord.objects.using(bdd).filter(lid =lid, sid =item.sid).exclude(rank =0)]))
    uri6 =multipleplot(x6, y61, y63, y613, _("reliés"), _("non reliés"), _("total"), _(""), _(""), _("Fiches à traiter (*)") )

    qs =[]
    for l in Library.objects.using(bdd).all().exclude(name ="checker").order_by("name"):
        qs.append(l)
    x7, y7 =[], []
    for libmt in qs:
        x7.append(libmt.name)
        pos, nopos =0, 0
        for item in ItemRecord.objects.using(bdd).filter(lid =libmt.lid):
            if not item.rank ==99 and len(ItemRecord.objects.using(bdd).filter(sid =item.sid).exclude(rank =0)) >1 and ItemRecord.objects.using(bdd).filter(lid =lid, sid =item.sid).exclude(rank =0):
                pos +=1
            elif item.rank ==99 and len(ItemRecord.objects.using(bdd).filter(sid =item.sid).exclude(rank =0)) >1 and ItemRecord.objects.using(bdd).filter(lid =lid, sid =item.sid).exclude(rank =0):
                nopos +=1
        y7.append(round(10000*pos/(pos + nopos)/100))
    uri7 =get_scatter(x7, y7, _(""), _(""), _("Positionnements réalisés en % des rattachements (*)"))

    return render(request, 'epl/indicators_x.html', locals())

@edmode3
def search(request, bdd):
# Lot of code for this view is similar with the code for "current_status" view : When changing here, think to change there

    k =logstatus(request)
    version =epl_version

    libch = ('checker','checker'),
    for l in Library.objects.using(bdd).all().exclude(name ='checker').order_by('name'):
        libch += (l.name, l.name),

    class SearchForm(forms.Form):
        sid = forms.CharField(required = True, label =_("ppn"))
        lib = forms.ChoiceField(required = True, widget=forms.Select, choices=libch, label =_("Votre bibliothèque"))

    l =0
    form = SearchForm(request.POST or None)
    if form.is_valid():
        sid = form.cleaned_data['sid']
        lib = form.cleaned_data['lib']
        lid = Library.objects.using(bdd).get(name =lib).lid
        n = len(ItemRecord.objects.using(bdd).filter(sid =sid))
        ranklist =[] # if n==0
        progress =0
        action, laction =0,0
        alteraction, lalteraction =0,0

        if ItemRecord.objects.using(bdd).filter(sid =sid):
            # Bibliographic data :
            title = ItemRecord.objects.using(bdd).filter(sid =sid)[0].title
            issn = ItemRecord.objects.using(bdd).filter(sid =sid)[0].issn
            pubhist = ItemRecord.objects.using(bdd).filter(sid =sid)[0].pubhist
        if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid):
            l =1
            # ItemRecord data :
            holdstat = ItemRecord.objects.using(bdd).get(sid =sid, lid = lid).holdstat
            missing = ItemRecord.objects.using(bdd).get(sid =sid, lid = lid).missing
            cn = ItemRecord.objects.using(bdd).get(sid =sid, lid = lid).cn

        if n ==1:
            bil =Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =sid).lid).name

        elif n >1:

            #Calcul de l'avancement:
            higher_status =ItemRecord.objects.using(bdd).filter(sid =sid).order_by("-status")[0].status
            if higher_status ==6:
                if len(Instruction.objects.using(bdd).filter(sid =sid, name ="checker")):
                    progress =_("Anomalie signalée lors de la phase des non reliés")
                else:
                    progress =_("Anomalie signalée lors de la phase des reliés")
            elif higher_status ==5:
                progress =_("Instruction achevée")
                if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid).exclude(rank =0):
                    action, laction =_("Edition de la fiche de résultante"), bdd + "/ed/" + str(sid) + "/" + str(lid)
            elif higher_status ==4:
                if len(ItemRecord.objects.using(bdd).filter(sid =sid, status =4)) ==len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)):
                    progress =_("En attente de validation finale par le contrôleur")
                    if lid =="999999999":
                        action, laction =_("Validation finale"), bdd + "/end/" + str(sid) + "/" + str(lid)
                else:
                    if lid !="999999999":
                        if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid, status =3):
                            if Instruction.objects.using(bdd).filter(sid =sid, bound =" ", name =Library.objects.using(bdd).get(lid =lid).name):
                                progress =_("Instruction des non reliés en cours pour votre collection")
                            else:
                                progress =_("Instruction des non reliés à débuter pour votre collection")
                            action, laction =_("Instruction"), bdd + "/add/" + str(sid) + "/" + str(lid)
                        else:
                            xname =Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =sid, status =3).lid).name
                            if Instruction.objects.using(bdd).filter(sid =sid, bound =" ", name =xname):
                                progress =_("Instruction des non reliés en cours pour : ")
                            else:
                                progress =_("Instruction des non reliés en cours ; à débuter pour : ")
                    else:#lid ="999999999"
                        xname =Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =sid, status =3).lid).name
                        if Instruction.objects.using(bdd).filter(sid =sid, bound =" ", name =xname):
                            progress =_("Instruction des non reliés en cours pour : ")
                        else:
                            progress =_("Instruction des non reliés en cours ; à débuter pour : ")
            elif higher_status ==3:
                if lid !="999999999":
                    if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid, status =3):
                        if Instruction.objects.using(bdd).filter(sid =sid, bound =" ", name =Library.objects.using(bdd).get(lid =lid).name):
                            progress =_("Instruction des non reliés en cours pour votre collection")
                        else:
                            progress =_("Instruction des non reliés à débuter pour votre collection")
                        action, laction =_("Instruction"), bdd + "/add/" + str(sid) + "/" + str(lid)
                    else:
                        xname =Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =sid, status =3).lid).name
                        if Instruction.objects.using(bdd).filter(sid =sid, bound =" ", name =xname):
                            progress =_("Instruction des non reliés en cours pour : ")
                        else:
                            progress =_("Instruction des non reliés en cours ; à débuter pour : ")
                else:#lid ="999999999"
                    xname =Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =sid, status =3).lid).name
                    if Instruction.objects.using(bdd).filter(sid =sid, bound =" ", name =xname):
                        progress =_("Instruction des non reliés en cours pour : ")
                    else:
                        progress =_("Instruction des non reliés en cours ; à débuter pour : ")
            elif higher_status ==2:
                if len(ItemRecord.objects.using(bdd).filter(sid =sid, status =2)) ==len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)):
                    progress =_("En attente de validation intermédiaire par le contrôleur")
                    if lid =="999999999":
                        action, laction =_("Validation intermédiaire"), bdd + "/end/" + str(sid) + "/" + str(lid)
                else:
                    if lid !="999999999":
                        if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid, status =1):
                            if Instruction.objects.using(bdd).filter(sid =sid, bound ="x", name =Library.objects.using(bdd).get(lid =lid).name):
                                progress =_("Instruction des reliés en cours pour votre collection")
                            else:
                                progress =_("Instruction des reliés à débuter pour votre collection")
                            action, laction =_("Instruction"), bdd + "/add/" + str(sid) + "/" + str(lid)
                        else:
                            xname =Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =sid, status =1).lid).name
                            if Instruction.objects.using(bdd).filter(sid =sid, bound ="x", name =xname):
                                progress =_("Instruction des reliés en cours pour : ")
                            else:
                                progress =_("Instruction des reliés en cours ; à débuter pour : ")
                    else:#lid ="999999999"
                        xname =Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =sid, status =1).lid).name
                        if Instruction.objects.using(bdd).filter(sid =sid, bound ="x", name =xname):
                            progress =_("Instruction des reliés en cours pour : ")
                        else:
                            progress =_("Instruction des reliés en cours ; à débuter pour : ")
            elif higher_status ==1:
                if lid !="999999999":
                    if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid, status =1):
                        if Instruction.objects.using(bdd).filter(sid =sid, bound ="x", name =Library.objects.using(bdd).get(lid =lid).name):
                            progress =_("Instruction des reliés en cours pour votre collection")
                        else:
                            progress =_("Instruction des reliés à débuter pour votre collection")
                        action, laction =_("Instruction"), bdd + "/add/" + str(sid) + "/" + str(lid)
                    else:
                        xname =Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =sid, status =1).lid).name
                        if Instruction.objects.using(bdd).filter(sid =sid, bound ="x", name =xname):
                            progress =_("Instruction des reliés en cours pour : ")
                        else:
                            progress =_("Instruction des reliés en cours ; à débuter pour : ")
                    if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid) and len(Instruction.objects.using(bdd).filter(sid =sid)) ==0:
                        alteraction, lalteraction =_("Modification éventuelle du rang de votre collection"), bdd + "/rk/" + str(sid) + "/" + str(lid)
                else:#lid ="999999999"
                    xname =Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =sid, status =1).lid).name
                    if Instruction.objects.using(bdd).filter(sid =sid, bound ="x", name =xname):
                        progress =_("Instruction des reliés en cours pour : ")
                    else:
                        progress =_("Instruction des reliés en cours ; à débuter pour : ")
            else: # higher_status ==0
                if lid !="999999999":
                    if len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) <2:
                        progress =_("La ressource n'est plus candidate au dédoublonnement")
                        if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid, rank =0):
                             action, laction =_("Repositionnement éventuel de votre collection"), bdd + "/rk/" + str(sid) + "/" + str(lid)
                    elif ItemRecord.objects.using(bdd).filter(sid =sid, rank =99) and len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) >1:
                        if ItemRecord.objects.using(bdd).filter(sid =sid, rank =99, lid =lid):
                            progress =_("Positionnement à compléter pour votre collection")
                            action, laction =_("Positionnement de votre collection"), bdd + "/rk/" + str(sid) + "/" + str(lid)
                        else:
                            progress =_("Positionnement à compléter pour une ou plusieurs collections")
                            if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid):
                                alteraction, lalteraction =_("Modification éventuelle du rang de votre collection"), bdd + "/rk/" + str(sid) + "/" + str(lid)
                    elif len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) >1:
                        if ItemRecord.objects.using(bdd).filter(sid =sid, rank =1, lid =lid):
                            progress =_("Rang 1 revendiqué pour plusieurs collections dont la vôtre")
                            action, laction =_("Repositionnement éventuel de votre collection"), bdd + "/rk/" + str(sid) + "/" + str(lid)
                        else:
                            progress =_("Rang 1 revendiqué pour plusieurs collections mais pas la vôtre")
                            if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid):
                                alteraction, lalteraction =_("Modification éventuelle du rang de votre collection"), bdd + "/rk/" + str(sid) + "/" + str(lid)
                    else:# len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) ==0:
                        progress =_("Le rang 1 n'a été revendiqué pour aucune collection")
                        if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid):
                            action, laction =_("Repositionnement éventuel de votre collection"), bdd + "/rk/" + str(sid) + "/" + str(lid)
                else: #lid ="999999999"
                    if len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) <2:
                        progress =_("La ressource n'est plus candidate au dédoublonnement")
                    elif ItemRecord.objects.using(bdd).filter(sid =sid, rank =99) and len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) >1:
                        progress =_("Positionnement à compléter pour une ou plusieurs collections")
                    elif len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) >1:
                        progress =_("Rang 1 revendiqué pour plusieurs collections")
                    else:# len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) ==0:
                        progress =_("Le rang 1 n'a été revendiqué pour aucune collection")

            #Getting instructions for the considered ressource :
            instrlist = Instruction.objects.using(bdd).filter(sid = sid).order_by('line')
            size =len(instrlist)

            try:
                pklastone = Instruction.objects.using(bdd).filter(sid = sid).latest('time').pk
            except:
                pklastone =0

            #Attachements :
            attchmt =ItemRecord.objects.using(bdd).filter(sid =sid).order_by('rank')
            attlist = [(Library.objects.using(bdd).get(lid =element.lid).name, element) for element in attchmt]

            rklist = ItemRecord.objects.using(bdd).filter(sid =sid).order_by('rank', 'lid')
            ranklist = [(element, Library.objects.using(bdd).get(lid =element.lid).name) for element in rklist]

    return render(request, 'epl/search.html', locals())

@edmode3
def general_search(request, bdd):

    k =logstatus(request)
    version =epl_version
    
    libch1 = ('', ''),
    for l in Library.objects.using(bdd).all().exclude(name ='checker').order_by('name'):
        libch1 += (l.name, l.name),
        
    libch2 = ('nix', _('')),
    for l in Library.objects.using(bdd).all().exclude(name ='checker').order_by('name'):
        libch2 += (l.name, l.name),
        
    mothch = ('nix', _('')), ('not', _("Pas la vôtre (et peut-être aucune autre)")), ('othan', _('Une autre que la vôtre')),
    for l in Library.objects.using(bdd).all().exclude(name ='checker').order_by('name'):
        mothch += (l.name, l.name),

    EXCLUSION_CHOICES =\
    ('nix', _('')),\
    ('none', _("**Pas d'exclusion**")),\
    ('anyone', _("**N'importe quelle exclusion**")),    
    for e in list(ItemRecord.objects.using(bdd).filter(rank =0).exclude(excl ="Autre (Commenter)").values_list('excl', flat =True).distinct()):
        EXCLUSION_CHOICES += (e, e),
    for e in Exclusion.objects.using(bdd).all().order_by('label'):
        if (e.label, e.label) not in EXCLUSION_CHOICES:
            EXCLUSION_CHOICES += (e.label, e.label),
    EXCLUSION_CHOICES += ("Autre (Commenter)", _("Autre (Commenter)")),
    
    STATUS_CHOICES =\
    ('a', _('')),\
    ('b', _('Ressources écartées par exclusion')),\
    ('c', _('Positionnement incomplet')),\
    ('d', _('Positionnement modifiable')),\
    ('e', _('Positionnement non modifiable')),\
    ('f', _('Le repositionnement de votre collection en 1 lèverait un arbitrage de type 0')),\
    ('g', _('Votre collection est impliquée dans un arbitrage de type 1')),\
    ('h', _('Instruction des reliés à débuter ou en cours dans une des bibliothèques')),\
    ('i', _('Instruction des non reliés à débuter ou en cours dans une des bibliothèques')),\
    ('j', _('Instruction achevée')),\
    ('k', _('Anomalie relevée')),\

    class SearchForm(forms.Form):
        lib = forms.ChoiceField(required = True, widget=forms.Select, choices=libch1, label =_("Votre bibliothèque"))
        sid = forms.CharField(required = False, label =_("PPN"))
        issn = forms.CharField(required = False, label =_("ISSN"))
        title_wrd1 = forms.CharField(required = False, label =_("Mot du titre"))
        title_wrd2 = forms.CharField(required = False, label =_("Autre mot du titre"))
        xlib = forms.ChoiceField(required = False, widget=forms.Select, choices=libch2, label =_("Autre bibliothèque"))
        mother = forms.ChoiceField(required = False, widget=forms.Select, choices=mothch, label =_("Collection mère"))
        statut = forms.ChoiceField(required = False, widget=forms.Select, choices=STATUS_CHOICES, label =_("Statut dans votre bibliothèque"))
        lib_excl = forms.ChoiceField(required = False, widget=forms.Select, choices=EXCLUSION_CHOICES, label =_("Motif d'exclusion dans votre bibliothèque"))
        xlib_excl = forms.ChoiceField(required = False, widget=forms.Select, choices=EXCLUSION_CHOICES, label =_("Le cas échéant, motif d'exclusion dans l'autre bibliothèque"))

    form = SearchForm(request.POST or None)
    if form.is_valid():
        lib = form.cleaned_data['lib']
        sid = form.cleaned_data['sid']
        issn = form.cleaned_data['issn']
        title_wrd1 = form.cleaned_data['title_wrd1']
        title_wrd2 = form.cleaned_data['title_wrd2']
        xlib = form.cleaned_data['xlib']
        mother = form.cleaned_data['mother']
        statut = form.cleaned_data['statut']
        lib_excl = form.cleaned_data['lib_excl']
        xlib_excl = form.cleaned_data['xlib_excl']
        
        lid = Library.objects.using(bdd).get(name =lib).lid

        sid_set = {"sid"}
        for i in ItemRecord.objects.using(bdd).filter(lid =lid):
            sid_set.add(i.sid)
        issn_set = {"issn"}
        for i in ItemRecord.objects.using(bdd).filter(lid =lid):
            issn_set.add(i.sid)
        lib_set = {"lib"}
        for i in ItemRecord.objects.using(bdd).filter(lid =lid):
            lib_set.add(i.sid)
        xlib_set = {"xlib"}
        for i in ItemRecord.objects.using(bdd).filter(lid =lid):
            xlib_set.add(i.sid)
        lib_excl_set = {"lib_excl"}
        for i in ItemRecord.objects.using(bdd).filter(lid =lid):
            lib_excl_set.add(i.sid)
        xlib_excl_set = {"xlib_excl"}
        for i in ItemRecord.objects.using(bdd).filter(lid =lid):
            xlib_excl_set.add(i.sid)
        tlib_excl_set = {"tlib_excl"}
        for i in ItemRecord.objects.using(bdd).filter(lid =lid):
            tlib_excl_set.add(i.sid)
        mother_set = {"mother"}
        for i in ItemRecord.objects.using(bdd).filter(lid =lid):
            mother_set.add(i.sid)
        title_wrd1_set = {"title_wrd1"}
        for i in ItemRecord.objects.using(bdd).filter(lid =lid):
            title_wrd1_set.add(i.sid)
        title_wrd2_set = {"title_wrd2"}
        for i in ItemRecord.objects.using(bdd).filter(lid =lid):
            title_wrd2_set.add(i.sid)
        statut_set = {"statut"}
        for i in ItemRecord.objects.using(bdd).filter(lid =lid):
            statut_set.add(i.sid)
        gen_set = {"gen"}
        
        if sid:
            try:
                sid_set ={ItemRecord.objects.using(bdd).get(lid =lid, sid =sid).sid}
            except:
                sid_set ={"sid"}
                messages.info(request, _("Pas de réponse pour ce ppn"))
        
        if issn:
            try:
                issn_set ={ItemRecord.objects.using(bdd).get(lid =lid, issn =issn).sid}
            except:
                issn_set ={"issn"}
                messages.info(request, _("Pas de réponse pour cet issn (essayez avec et sans tiret)"))

        if title_wrd1:
            title_wrd1_set ={"title_wrd1"}
            for i in ItemRecord.objects.using(bdd).filter(lid =lid):
                if title_wrd1 in i.title.split():
                    title_wrd1_set.add(i.sid)
            if title_wrd1_set =={"title_wrd1"}:
                messages.info(request, _("""Pas de réponse pour le mot "{}" """).format(title_wrd1))

        if title_wrd2:
            title_wrd2_set ={"title_wrd2"}
            for i in ItemRecord.objects.using(bdd).filter(lid =lid):
                if title_wrd2 in i.title.split():
                    title_wrd2_set.add(i.sid)
            if title_wrd2_set =={"title_wrd2"}:
                messages.info(request, _("""Pas de réponse pour le mot "{}" """).format(title_wrd2))    
        
        if xlib !="nix":
            xlid =Library.objects.using(bdd).get(name =xlib).lid
            xlib_set ={"xlib"}
            for i in ItemRecord.objects.using(bdd).filter(lid =lid):
                if ItemRecord.objects.using(bdd).filter(sid =i.sid, lid =xlid):
                    xlib_set.add(i.sid)
            if xlib_set =={"xlib"}:
                messages.info(request, _("Le croisement avec cette bibliothèque ne ramène aucun résultat"))
                    
        if mother =="nix":
            pass
        else:
            mother_set ={"mother"}
            if mother =="not":
                for i in ItemRecord.objects.using(bdd).all():
                    if len(ItemRecord.objects.using(bdd).filter(sid =i.sid, rank =99)) ==0 and \
                    len(ItemRecord.objects.using(bdd).filter(sid =i.sid).exclude(rank =0)) >1 and \
                    len(ItemRecord.objects.using(bdd).filter(sid =i.sid, lid =lid, rank =1)) ==0:
                        mother_set.add(i.sid)
            elif mother =="othan":
                for i in ItemRecord.objects.using(bdd).all():
                    if len(ItemRecord.objects.using(bdd).filter(sid =i.sid, rank =99)) ==0 and \
                    len(ItemRecord.objects.using(bdd).filter(sid =i.sid).exclude(rank =0)) >1 and \
                    len(ItemRecord.objects.using(bdd).filter(sid =i.sid, rank =1)) ==1 and \
                    len(ItemRecord.objects.using(bdd).filter(sid =i.sid, lid =lid, rank =1)) ==0:
                        mother_set.add(i.sid)
            else:
                for i in ItemRecord.objects.using(bdd).all():
                    if len(ItemRecord.objects.using(bdd).filter(sid =i.sid, rank =99)) ==0 and \
                    len(ItemRecord.objects.using(bdd).filter(sid =i.sid).exclude(rank =0)) >1 and \
                    len(ItemRecord.objects.using(bdd).filter(sid =i.sid, rank =1)) ==1 and \
                    len(ItemRecord.objects.using(bdd).filter(sid =i.sid, lid =Library.objects.using(bdd).get(name =mother).lid, rank =1)) ==1:
                        mother_set.add(i.sid)            
            if mother_set =={"mother"}:
                messages.info(request, _("La collection mère sélectionnée ne ramène aucun résultat"))
                
        if statut =="a":#--Indifférent--
            pass
        else:
            statut_set ={"statut"}
            if statut =="b":#Ressources écartées par exclusion
                discard =[]
                for i in ItemRecord.objects.using(bdd).filter(rank =0):
                    if len(ItemRecord.objects.using(bdd).filter(sid =i.sid).exclude(rank =0)) ==1 and not i.sid in discard:
                        discard.append(i.sid)
                for s in discard:
                    try:
                        statut_set.add(ItemRecord.objects.using(bdd).get(sid =s, lid =lid).sid)
                    except:
                        pass

            if statut =="c":#Positionnement incomplet
                resslist = []
                reclist = list(ItemRecord.objects.using(bdd).filter(rank =99))
                for e in reclist:
                    sid = e.sid
                    if len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) >1 and not sid in resslist:
                        resslist.append(e)
                sidlist = [ir.sid for ir in resslist]
                for s in sidlist:
                    try:
                        statut_set.add(ItemRecord.objects.using(bdd).get(sid =s, lid =lid).sid)
                    except:
                        pass
                    
            if statut =="d":#Positionnement modifiable
                resslist = []
                reclist = list(ItemRecord.objects.using(bdd).filter(lid =lid).exclude(rank =99))
                for e in reclist:
                    sid = e.sid
                    if len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) >1 and not Instruction.objects.using(bdd).filter(sid =sid) and not sid in resslist:
                        resslist.append(e)
                sidlist = [ir.sid for ir in resslist]
                for s in sidlist:
                    try:
                        statut_set.add(ItemRecord.objects.using(bdd).get(sid =s, lid =lid).sid)
                    except:
                        pass

            if statut =="e":#Positionnement non modifiable
                resslist = []
                reclist = list(ItemRecord.objects.using(bdd).exclude(rank =99))
                for e in reclist:
                    sid = e.sid
                    if len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) >1 and Instruction.objects.using(bdd).filter(sid =sid) and not sid in resslist:
                        resslist.append(e)
                sidlist = [ir.sid for ir in resslist]
                for s in sidlist:
                    try:
                        statut_set.add(ItemRecord.objects.using(bdd).get(sid =s, lid =lid).sid)
                    except:
                        pass

            if statut =="f":#Le repositionnement de votre collection en 1 lèverait un arbitrage de type 0
                resslist = []
                reclist = list(ItemRecord.objects.using(bdd).filter(status =0).exclude(rank =1).exclude(rank =0).exclude(rank =99))
                for e in reclist:
                    sid = e.sid
                    if len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) ==0 and \
                    len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =99)) ==0 and \
                    len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) >1 and not sid in resslist:
                        resslist.append(e)
                sidlist = [ir.sid for ir in resslist]
                for s in sidlist:
                    try:
                        if ItemRecord.objects.using(bdd).get(sid =s, lid =lid).rank in [0, 2, 3, 4]:
                            statut_set.add(ItemRecord.objects.using(bdd).get(sid =s, lid =lid).sid)
                    except:
                        pass

            if statut =="g":#Votre collection est impliquée dans un arbitrage de type 1
                resslist = []
                reclist = list(ItemRecord.objects.using(bdd).filter(rank = 1, status =0))
                for e in reclist:
                    sid = e.sid
                    if len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) >1 and not sid in resslist:
                        resslist.append(e)
                sidlist = [ir.sid for ir in resslist]
                for s in sidlist:
                    try:
                        statut_set.add(ItemRecord.objects.using(bdd).get(sid =s, lid =lid, rank =1).sid)
                    except:
                        pass

            if statut =="h":#Instruction des reliés à débuter ou en cours dans une des bibliothèques
                for i in ItemRecord.objects.using(bdd).filter(rank =1, status =1):
                    try:
                        statut_set.add(ItemRecord.objects.using(bdd).exclude(rank =0).get(sid =i.sid, lid =lid).sid)
                    except:
                        pass
                    
            if statut =="i":#Instruction des non reliés à débuter ou en cours dans une des bibliothèques
                for i in ItemRecord.objects.using(bdd).filter(rank =1, status =3):
                    try:
                        statut_set.add(ItemRecord.objects.using(bdd).exclude(rank =0).get(sid =i.sid, lid =lid).sid)
                    except:
                        pass

            if statut =="j":#Instruction achevée
                for i in ItemRecord.objects.using(bdd).filter(rank =1, status =5):
                    try:
                        statut_set.add(ItemRecord.objects.using(bdd).exclude(rank =0).get(sid =i.sid, lid =lid).sid)
                    except:
                        pass

            if statut =="k":#Anomalie relevée
                for i in ItemRecord.objects.using(bdd).filter(rank =1, status =6):
                    try:
                        statut_set.add(ItemRecord.objects.using(bdd).exclude(rank =0).get(sid =i.sid, lid =lid).sid)
                    except:
                        pass
                        
            if statut_set =={"statut"}:
                messages.info(request, _("Le statut sélectionné ne ramène aucun résultat"))
                
        if lib_excl =="nix":
            pass
        else:
            lib_excl_set ={"lib_excl"}
            if lib_excl =="none":
                for i in ItemRecord.objects.using(bdd).filter(lid =lid, excl =""):
                    lib_excl_set.add(i.sid)
            elif lib_excl =="anyone":
                for i in ItemRecord.objects.using(bdd).filter(lid =lid, rank =0):
                    lib_excl_set.add(i.sid)
            else:
                for i in ItemRecord.objects.using(bdd).filter(lid =lid, excl =lib_excl):
                    lib_excl_set.add(i.sid)
        if lib_excl_set =={"lib_excl"}:
            messages.info(request, _("Le motif d'exclusion choisi pour votre bibliothèque ne ramène aucun résultat"))
            
        if xlib_excl !="nix":
            if xlib =="nix":
                messages.info(request, _("Vous n'avez pas indiqué l'autre bibliothèque"))
                return render(request, 'epl/gen_search.html', locals())
            else:
                xlid =Library.objects.using(bdd).get(name =xlib).lid
                if xlib_excl =="nix":
                    pass
                else:
                    xlib_excl_set ={"xlib_excl"}
                    if xlib_excl =="none":
                        for i in ItemRecord.objects.using(bdd).filter(lid =xlid).exclude(rank =0):
                            xlib_excl_set.add(i.sid)
                    elif xlib_excl =="anyone":
                        for i in ItemRecord.objects.using(bdd).filter(lid =xlid, rank =0):
                            xlib_excl_set.add(i.sid)
                    else:
                        for i in ItemRecord.objects.using(bdd).filter(lid =xlid, excl =xlib_excl):
                            xlib_excl_set.add(i.sid)
                    if xlib_excl_set =={"xlib_excl"}:
                        messages.info(request, _("Le motif d'exclusion choisi pour l'autre bibliothèque ne ramène aucun résultat"))
                            
        gen_set = sid_set & issn_set & title_wrd1_set & \
        title_wrd2_set & xlib_set & mother_set & statut_set & \
        lib_excl_set & xlib_excl_set
        
        try:
            test = Library.objects.using(bdd).get(name =lib)
            test = 1
        except:
            test = 0
            
        size = len(gen_set)
        
        if size ==0:
            messages.info(request, _("La recherche ne produit aucun résultat"))
        elif size ==1:
            sid =list(gen_set)[0]
            messages.info(request, _("(Résultat unique de votre recherche)"))
            return current_status(request, bdd, sid, lid)
        else:
            pass
        
        if xlib =="nix":
            xlid ="None"
        
    return render(request, 'epl/gen_search.html', locals())


@edmode9
def cross_list(request, bdd, lid, xlid, recset, sort):
    
    libname = Library.objects.using(bdd).get(lid =lid).name

    sidlist =list(eval(recset[1:-1]))
    
    sidset =set(sidlist)
    
    results_set =ItemRecord.objects.using(bdd).filter(sid__in=sidlist, lid =lid).order_by(sort) 
    size =len(results_set)
    
    if xlid =="None":
        code ="80"
        newestfeat(request, bdd, libname, "80")        
    else:
        code ="81"
        xnewestfeat(request, bdd, libname, "81", xlid)

    return render(request, 'epl/gen_search_results.html', locals())


@login_required
def reinit(request, bdd, sid):

    k =logstatus(request)
    version =epl_version
    suffixe = "@" + str(bdd)

    #Authentication control :
    adminslist =[]
    for b in BddAdmin.objects.using(bdd).all():
        adminslist.append(b.contact)
    if not request.user.email in adminslist:
        messages.info(request, _("Vous avez été déconnecté parce que votre identifiant ne vous autorisait pas à accéder à la page demandée"))
        return logout_view(request)
    if not request.user.username[-3:] ==suffixe:
        messages.info(request, _("Vous avez été déconnecté parce que votre identifiant ne vous autorisait pas à accéder à la page demandée"))
        return logout_view(request)

    info =""

    ressource =ItemRecord.objects.using(bdd).get(sid =sid, rank =1)

    y = Flag()
    form = CheckForm(request.POST or None, instance =y)

    if form.is_valid():
        if y.flag:
            if Instruction.objects.using(bdd).filter(sid =sid, bound =" "):
                for instr in Instruction.objects.using(bdd).filter(sid =sid).exclude(bound ="x"):
                    instr.delete(using=bdd)
                for item in ItemRecord.objects.using(bdd).filter(sid =sid):
                    if item.rank ==1:
                        item.status =3
                        item.save(using=bdd)
                    else:
                        item.status =2
                        item.save(using=bdd)
            else:
                for instr in Instruction.objects.using(bdd).filter(sid =sid):
                    instr.delete(using=bdd)
                for item in ItemRecord.objects.using(bdd).filter(sid =sid):
                    if item.rank ==1:
                        item.status =1
                        item.save(using=bdd)
                    else:
                        item.status =0
                        item.save(using=bdd)
            if Proj_setting.objects.using(bdd).all()[0].ins:
                #Message data :
                nextlid =ItemRecord.objects.using(bdd).get(sid =sid, rank =1).lid
                nextlib =Library.objects.using(bdd).get(lid =nextlid)
                subject = "eplouribousse / instruction : " + bdd + " / " + str(sid) + " / " + str(nextlid)
                host = str(request.get_host())
                message = _("Votre tour est venu d'instruire la fiche eplouribousse pour le ppn ") + str(sid) + \
                " :\n" + "http://" + host + "/" + bdd + "/add/" + str(sid) + '/' + str(nextlid) + \
                "\n" + _("(Ce message fait suite à une correction apportée par l'administrateur de la base de données)")
                dest =[]
                if Utilisateur.objects.using(bdd).get(mail =nextlib.contact).ins:
                    dest.append(nextlib.contact)
                try:
                    if Utilisateur.objects.using(bdd).get(mail =nextlib.contact_bis).ins:
                        dest.append(nextlib.contact_bis)
                except:
                    st =1 #bidon pour passer
                try:
                    if Utilisateur.objects.using(bdd).get(mail =nextlib.contact_ter).ins:
                        dest.append(nextlib.contact_ter)
                except:
                    st =1 #bidon pour passer
                if len(dest):
                    send_mail(subject, message, replymail, dest, fail_silently=True, )


            return current_status(request, bdd, sid, "999999999")
        else:
            info =_("Vous n'avez pas coché !")

    return render(request, 'epl/reinit.html', locals())


@login_required
def takerank(request, bdd, sid, lid):

    k =logstatus(request)
    version =epl_version
    suffixe = "@" + str(bdd)

    #Authentication control :
    if not request.user.email in [Library.objects.using(bdd).get(lid =lid).contact, Library.objects.using(bdd).get(lid =lid).contact_bis, Library.objects.using(bdd).get(lid =lid).contact_ter]:
        messages.info(request, _("Vous avez été déconnecté parce que votre identifiant ne vous autorisait pas à accéder à la page demandée"))
        return logout_view(request)
    if not request.user.username[-3:] ==suffixe:
        messages.info(request, _("Vous avez été déconnecté parce que votre identifiant ne vous autorisait pas à accéder à la page demandée"))
        return logout_view(request)

    #Control (takerank only if still possible ; status still ==0 for all attached libraries ;
    #or status ==1 but no instruction yet ; lid not "999999999")

    if len(list(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(status =0).exclude(status =1))):
        return notintime(request, bdd, sid, lid)
    elif len(list(ItemRecord.objects.using(bdd).filter(sid =sid, status =1))) and len(list(Instruction.objects.using(bdd).filter(sid = sid))):
        return notintime(request, bdd, sid, lid)
    elif lid =="999999999":
        return notintime(request, bdd, sid, lid)
    
    #Ouvrir un message pour discuter le positionnement :
    sbjct ="[eplouribousse - " + Project.objects.using(bdd).all()[0].name + " (" + bdd + ") " + "] " + sid + " : Positionnement à discuter."
    to, cc =[request.user.email], [request.user.email]
    if len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) >1:
        for itelmt in ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0):
            if Library.objects.using(bdd).get(lid =itelmt.lid).lid ==lid:
                if "@" in str(Library.objects.using(bdd).get(lid =itelmt.lid).contact) and Library.objects.using(bdd).get(lid =itelmt.lid).contact not in cc:
                    cc.append(Library.objects.using(bdd).get(lid =itelmt.lid).contact)
                if "@" in str(Library.objects.using(bdd).get(lid =itelmt.lid).contact_bis) and Library.objects.using(bdd).get(lid =itelmt.lid).contact_bis not in cc:
                    cc.append(Library.objects.using(bdd).get(lid =itelmt.lid).contact_bis)
                if "@" in str(Library.objects.using(bdd).get(lid =itelmt.lid).contact_ter) and Library.objects.using(bdd).get(lid =itelmt.lid).contact_ter not in cc:
                    cc.append(Library.objects.using(bdd).get(lid =itelmt.lid).contact_ter)
            else:
                if "@" in str(Library.objects.using(bdd).get(lid =itelmt.lid).contact) and Library.objects.using(bdd).get(lid =itelmt.lid).contact not in to:
                    to.append(Library.objects.using(bdd).get(lid =itelmt.lid).contact)
                if "@" in str(Library.objects.using(bdd).get(lid =itelmt.lid).contact_bis) and Library.objects.using(bdd).get(lid =itelmt.lid).contact_bis not in to:
                    to.append(Library.objects.using(bdd).get(lid =itelmt.lid).contact_bis)
                if "@" in str(Library.objects.using(bdd).get(lid =itelmt.lid).contact_ter) and Library.objects.using(bdd).get(lid =itelmt.lid).contact_ter not in to:
                    to.append(Library.objects.using(bdd).get(lid =itelmt.lid).contact_ter)

    to.remove(request.user.email)
    cc.remove(request.user.email)
    if to:
        signal =1
    else:
        signal =0
    if signal ==1 and len(cc) >0:
        for mailmt in to:
            if mailmt in cc:
                cc.remove(mailmt)
    #(fin du codage pour le message servant à discuter le positionnement)

    # For position form :
    i = ItemRecord.objects.using(bdd).get(sid = sid, lid = lid)

    EXCLUSION_CHOICES = ('', ''),
    for e in Exclusion.objects.using(bdd).all().order_by('label'):
        EXCLUSION_CHOICES += (e.label, e.label),
    EXCLUSION_CHOICES += ("Autre (Commenter)", _("Autre (Commenter)")),


    class PositionForm(forms.ModelForm):
        class Meta:
            model = ItemRecord
            fields = ('rank', 'excl', 'comm',)
            widgets = {
                'rank' : forms.Select(attrs={'title': _("Choisissez 1 pour la collection mère ; 2, 3 ou 4 selon l'importance de votre collection ou d'autres raisons ...")}),
                'excl' : forms.Select(choices=EXCLUSION_CHOICES),
                'comm' : forms.Textarea(attrs={'placeholder': _("Commentaire éventuel pour expliquer votre choix (max. 250 caractères)")}),
                }

    f = PositionForm(request.POST, instance=i)
    if f.is_valid():
        #last controls before modifications :
        if (len(list(ItemRecord.objects.using(bdd).filter(sid = sid, status =1))) and not len(list(Instruction.objects.using(bdd).filter(sid = sid)))) or\
        len(list(ItemRecord.objects.using(bdd).filter(sid = sid).exclude(status =0))) ==0:
            # if len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(status =0)) ==0:
            if i.excl !='':
                i.rank =0
            try:
                old = ItemRecord.objects.using(bdd).get(lid =lid, last =1)
                old.last =0
                old.save(using =bdd)
                i.last =1
            except:
                i.last =1
            i.save(using=bdd)

            # Other status modification if all libraries have taken rank :
            # Status = 1 : item whose lid identified library must begin bound elements instructions on the sid identified serial (rank =1, no arbitration)
            # ordering by pk for identical ranks upper than 1.

            if len(ItemRecord.objects.using(bdd).filter(sid =sid, status =1)): #Since it's possible when modifying
                for elmt in ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =99):
                    if elmt.status !=0:
                        elmt.status =0
                        elmt.save(using=bdd)

            if len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =99)) ==0 and len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) ==1 \
            and len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) >1:
                p = ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0).exclude(rank =99).order_by("rank", "pk")[0]
                p.status =1
                p.save(using=bdd)
                if Proj_setting.objects.using(bdd).all()[0].ins:
                    #Message data :
                    nextlib =Library.objects.using(bdd).get(lid =p.lid)
                    nextlid =nextlib.lid
                    subject = "eplouribousse / instruction : " + bdd + " / " + str(sid) + " / " + str(nextlid)
                    host = str(request.get_host())
                    message = _("Votre tour est venu d'instruire la fiche eplouribousse pour le ppn ") + str(sid) +\
                    " :\n" + "http://" + host + "/" + bdd + "/add/" + str(sid) + '/' + str(nextlid)
                    dest =[]
                    if Utilisateur.objects.using(bdd).get(mail =nextlib.contact).ins:
                        dest.append(nextlib.contact)
                    try:
                        if Utilisateur.objects.using(bdd).get(mail =nextlib.contact_bis).ins:
                            dest.append(nextlib.contact_bis)
                    except:
                        st =1 #bidon pour passer
                    try:
                        if Utilisateur.objects.using(bdd).get(mail =nextlib.contact_ter).ins:
                            dest.append(nextlib.contact_ter)
                    except:
                        st =1 #bidon pour passer
                    if len(dest):
                        send_mail(subject, message, replymail, dest, fail_silently=True, )

            #Début codage alerte positionnement ou arbitrage

            if Proj_setting.objects.using(bdd).all()[0].rkg and len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =99)) and not \
            ItemRecord.objects.using(bdd).get(sid =sid, lid =lid).rank ==0:
                for itelmt in ItemRecord.objects.using(bdd).filter(sid =sid, rank =99):
                    dest =[]
                    if Utilisateur.objects.using(bdd).get(mail =Library.objects.using(bdd).get(lid =itelmt.lid).contact).rkg:
                        dest.append(Library.objects.using(bdd).get(lid =itelmt.lid).contact)
                    try:
                        if Utilisateur.objects.using(bdd).get(mail =Library.objects.using(bdd).get(lid =itelmt.lid).contact_bis).rkg:
                            dest.append(Library.objects.using(bdd).get(lid =itelmt.lid).contact_bis)
                    except:
                        st =1 #bidon pour passer
                    try:
                        if Utilisateur.objects.using(bdd).get(mail =Library.objects.using(bdd).get(lid =itelmt.lid).contact_ter).rkg:
                            dest.append(Library.objects.using(bdd).get(lid =itelmt.lid).contact_ter)
                    except:
                        st =1 #bidon pour passer

                    #Message data :
                    subject = "eplouribousse / positionnement : " + bdd + " / " + str(sid) + " / " + str(itelmt.lid)
                    host = str(request.get_host())
                    message = _("Un nouveau positionnement a été enregistré pour le ppn ") + \
                    str(sid) + " : rang " + str(i.rank) + " --> "  + Library.objects.using(bdd).get(lid =lid).name + \
                    "\n" + "Pour plus de détails et pour positionner votre collection" + \
                    " :\n" + "http://" + host + "/" + bdd + "/rk/" + str(sid) + '/' + str(itelmt.lid)
                    if len(dest):
                        send_mail(subject, message, replymail, dest, fail_silently=True, )


            if Proj_setting.objects.using(bdd).all()[0].arb and len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) ==0 and \
            len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =99)) ==0 and \
            len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) >1:
                for itelmt in ItemRecord.objects.using(bdd).filter(sid =sid):
                    dest =[]
                    if Utilisateur.objects.using(bdd).get(mail =Library.objects.using(bdd).get(lid =itelmt.lid).contact).arb:
                        dest.append(Library.objects.using(bdd).get(lid =itelmt.lid).contact)
                    try:
                        if Utilisateur.objects.using(bdd).get(mail =Library.objects.using(bdd).get(lid =itelmt.lid).contact_bis).arb:
                            dest.append(Library.objects.using(bdd).get(lid =itelmt.lid).contact_bis)
                    except:
                        st =1 #bidon pour passer
                    try:
                        if Utilisateur.objects.using(bdd).get(mail =Library.objects.using(bdd).get(lid =itelmt.lid).contact_ter).arb:
                            dest.append(Library.objects.using(bdd).get(lid =itelmt.lid).contact_ter)
                    except:
                        st =1 #bidon pour passer
                    #Message data :
                    subject = "eplouribousse / arbitrage (type 0) : " + bdd + " / " + str(sid) + " / " + str(itelmt.lid)
                    host = str(request.get_host())
                    message = _("Un nouvel arbitrage de type 0 a été repéré pour le ppn ") + str(sid) + \
                    "\n" + "Pour plus de détails ou pour modifier le rang de votre collection" + \
                    " :\n" + "http://" + host + "/" + bdd + "/rk/" + str(sid) + '/' + str(itelmt.lid)
                    if len(dest):
                        send_mail(subject, message, replymail, dest, fail_silently=True, )

            if Proj_setting.objects.using(bdd).all()[0].arb and len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) >1:
                for itelmt in ItemRecord.objects.using(bdd).filter(sid =sid, rank =1):
                    dest =[]
                    if Utilisateur.objects.using(bdd).get(mail =Library.objects.using(bdd).get(lid =itelmt.lid).contact).arb:
                        dest.append(Library.objects.using(bdd).get(lid =itelmt.lid).contact)
                    try:
                        if Utilisateur.objects.using(bdd).get(mail =Library.objects.using(bdd).get(lid =itelmt.lid).contact_bis).arb:
                            dest.append(Library.objects.using(bdd).get(lid =itelmt.lid).contact_bis)
                    except:
                        st =1 #bidon pour passer
                    try:
                        if Utilisateur.objects.using(bdd).get(mail =Library.objects.using(bdd).get(lid =itelmt.lid).contact_ter).arb:
                            dest.append(Library.objects.using(bdd).get(lid =itelmt.lid).contact_ter)
                    except:
                        st =1 #bidon pour passer
                    #Message data :
                    subject = "eplouribousse / arbitrage (type 1) : " + bdd + " / " + str(sid) + " / " + str(itelmt.lid)
                    host = str(request.get_host())
                    message = _("Un nouvel arbitrage de type 1 a été repéré pour le ppn ") + str(sid) + \
                    "\n" + "Pour plus de détails ou pour modifier le rang de votre collection" + \
                    " :\n" + "http://" + host + "/" + bdd + "/rk/" + str(sid) + '/' + str(itelmt.lid)
                    if len(dest):
                        send_mail(subject, message, replymail, dest, fail_silently=True, )

            #Fin codage alerte positionnement ou arbitrage
            #renvoi vers la liste adéquate en cas de recours au lien envoyé dans les alertes mail
            try:
                newestfeature =Feature.objects.using(bdd).get(libname =Library.objects.using(bdd).get(lid =lid).name)
                key =newestfeature.feaname.split('$')
                if key[0] in ["10", "11", "12", "20", "21", "22", "23", "24", "25"]:
                    return router(request, bdd, lid)
                else:
                    return ranktotake(request, bdd, lid, 'title')
            except:
                return ranktotake(request, bdd, lid, 'title')

        else:
            return notintime(request, bdd, sid, lid)

    # Item records list :
    itlist = ItemRecord.objects.using(bdd).filter(sid =  sid)
    itemlist = [(element, Library.objects.using(bdd).get(lid =element.lid).name) for element in itlist]
    # itemlist = list(itemlist)

    # restricted Item records list (without excluded collections) :
    r_itemlist = ItemRecord.objects.using(bdd).filter(sid =  sid).exclude(rank =0)
    r_itemlist = list(r_itemlist)

    # Ressource data :
    ress = itemlist[0][0]

    # Library data :
    lib = Library.objects.using(bdd).get(lid = lid)

    periscope = "https://periscope.sudoc.fr/Visualisation?ppnviewed=" + str(sid) + "&orderby=SORT_BY_PCP&collectionStatus=&tree="
    for i in r_itemlist[:-1]:
        periscope = periscope + i.lid + "%2C"
    periscope = periscope + r_itemlist[-1].lid

    return render(request, 'epl/ranking.html', locals())


@login_required
def addinstr(request, bdd, sid, lid):

    k =logstatus(request)
    version =epl_version

    length =0

    q = "x"
    if len(list((Instruction.objects.using(bdd).filter(sid =sid)).filter(name ='checker'))):
        q =" "
    else:
        q ="x"

    suffixe = "@" + str(bdd)

    #Authentication control :
    if not request.user.email in [Library.objects.using(bdd).get(lid =lid).contact, Library.objects.using(bdd).get(lid =lid).contact_bis, Library.objects.using(bdd).get(lid =lid).contact_ter]:
        messages.info(request, _("Vous avez été déconnecté parce que votre identifiant ne vous autorisait pas à accéder à la page demandée"))
        return logout_view(request)
    if not request.user.username[-3:] ==suffixe:
        messages.info(request, _("Vous avez été déconnecté parce que votre identifiant ne vous autorisait pas à accéder à la page demandée"))
        return logout_view(request)

    do = notintime(request, bdd, sid, lid)

    #Control (addinstr only if it's up to the considered lid)
    try:
        if lid !="999999999":
            if ItemRecord.objects.using(bdd).get(sid =sid, lid =lid).status not in [1, 3]:
                return do

        else: # i.e. lid =="999999999"
            if len(list((Instruction.objects.using(bdd).filter(sid =sid)).filter(name ='checker'))) ==2:
                return do
            elif len(list((Instruction.objects.using(bdd).filter(sid =sid)).filter(name ='checker'))) ==1:
                if len(list(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0))) != len(list(ItemRecord.objects.using(bdd).filter(sid =sid, status =4))):
                    return do
            else: # i.e. len(list((Instruction.objects.using(bdd).filter(sid =sid)).filter(name ='checker'))) ==0
                if len(list(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0))) != len(list(ItemRecord.objects.using(bdd).filter(sid =sid, status =2))):
                    return do
    except:
        z =1 #This is just to continue


    #Ressource data :
    itemlist = ItemRecord.objects.using(bdd).filter(sid = sid).exclude(rank =0).order_by("rank", 'pk')
    ress = itemlist[0]

    #Library data :
    lib = Library.objects.using(bdd).get(lid = lid)

    # Library list ordered by 'rank' (except "checker" which must be the last one)
    # to get from the precedent item list above :
    liblist = []
    for e in itemlist:
        liblist.append(Library.objects.using(bdd).get(lid = e.lid))
    liblist.append(Library.objects.using(bdd).get(name = 'checker'))

    #Remedied library list :
    remliblist = []
    for e in itemlist:
        remliblist.append(Library.objects.using(bdd).get(lid = e.lid))
    if (Library.objects.using(bdd).get(lid =lid)).name != 'checker':
        remliblist.remove(Library.objects.using(bdd).get(name = lib.name))

    #Info :
    info =""

    #Stage (bound or not bound) :
    if len(list((Instruction.objects.using(bdd).filter(sid =sid)).filter(name ='checker'))) ==0:
        bd =_('éléments reliés')
    elif len(list((Instruction.objects.using(bdd).filter(sid =sid)).filter(name ='checker'))) ==1:
        bd =_('éléments non reliés')

    if lid =="999999999":
        do = endinstr(request, bdd, sid, lid)
        return do

    else:
        #Instruction form instanciation and validation :
        i = Instruction(sid = sid, name = lib.name)

        class InstructionForm(forms.ModelForm):
            class Meta:
                REM_CHOICES =('',''),
                if Library.objects.using(bdd).all().exclude(name ='checker'):
                    for l in Library.objects.using(bdd).all().exclude(name ='checker').order_by('name'):
                        REM_CHOICES += (l.name, l.name),
                model = Instruction
                exclude = ('sid', 'name', 'bound',)
                widgets = {
                    'oname' : forms.Select(choices=REM_CHOICES, attrs={'title': _("Intitulé de la bibliothèque ayant précédemment déclaré une 'exception' ou un 'améliorable'")}),
                    'descr' : forms.TextInput(attrs={'placeholder': _("1990(2)-1998(12) par ex."), 'title': _("Suite ininterrompue chronologiquement ; le n° de ligne est à déterminer selon l'ordre chronologique de ce champ")}),
                    'exc' : forms.TextInput(attrs={'placeholder': _("1991(5) par ex."), 'title': \
                    _("éléments manquants dans le segment pour la forme considérée (pas forcément des lacunes si l'on considère la forme reliée)")}),
                    'degr' : forms.TextInput(attrs={'placeholder': _("1995(4) par ex."), 'title': \
                    _("éléments dégradés (un volume relié dégradé peut être remplacé par les fascicules correspondants en bon état)")}),
                }

        f = InstructionForm(request.POST, instance =i)

        REM_CHOICES =('',''),
        bibliolist =[]
        if Instruction.objects.using(bdd).filter(sid =sid).exclude(name =Library.objects.using(bdd).get(lid =lid).name).exclude(name ='checker'):
            for e in Instruction.objects.using(bdd).filter(sid =sid).exclude(name =Library.objects.using(bdd).get(lid =lid).name).exclude(name ='checker'):
                if (e.exc or e.degr) and Library.objects.using(bdd).get(name =e.name).name not in bibliolist:
                    bibliolist.append(Library.objects.using(bdd).get(name =e.name).name)
            bibliolist.sort()
            length =len(bibliolist)
        if length:
            for l in bibliolist:
                REM_CHOICES += (l, l),

        class Instr_Form(forms.Form):
            oname = forms.ChoiceField(required = False, widget=forms.Select(attrs={'title': _("Intitulé de la bibliothèque ayant précédemment déclaré une 'exception' ou un 'améliorable'")}), choices=REM_CHOICES, label =_("Bibliothèque remédiée"),)

        foname = Instr_Form(request.POST or None)

        if f.is_valid():
            if foname.is_valid():
                i.oname = foname.cleaned_data['oname']
            i.bound =q
            #A line may only be registered once :
            if not len(Instruction.objects.using(bdd).filter(sid =sid, name =lib.name, bound =i.bound, oname =i.oname, descr =i.descr, exc =i.exc, degr =i.degr)):
                # i.line +=1
                i.time =Now()
                i.save(using=bdd)
            else:
                info = _("Vous ne pouvez pas valider deux fois la même ligne d'instruction.")

        #Renumbering instruction lines :
        try:
            instr = Instruction.objects.using(bdd).filter(sid = sid).exclude(name = 'checker').exclude(descr =_("-- Néant --")).order_by('line', 'pk')
            l =1
            try:
                instrck = Instruction.objects.using(bdd).get(sid = sid, name ='checker', bound ="x")
                instrck.line =l
                instrck.save(using=bdd)
                l +=1
            except:
                pass
            try:
                for instrlmt in Instruction.objects.using(bdd).filter(sid = sid, descr =_("-- Néant --")).order_by("bound"):
                    instrlmt.line = l
                    instrlmt.save(using=bdd)
                    l +=1
            except:
                pass
            try:
                for instrlmt in instr:
                    instrlmt.line = l
                    instrlmt.save(using=bdd)
                    l +=1
            except:
                pass
        except:
            pass
        instrlist = Instruction.objects.using(bdd).filter(sid = sid).order_by('line')

        try:
            pklastone = Instruction.objects.using(bdd).filter(sid = sid).latest('time').pk
        except:
            pklastone =0

    try:
        itrec =ItemRecord.objects.using(bdd).get(sid =sid, lid =lid)
    except:
        itrec =""

    return render(request, 'epl/addinstruction.html', { 'ressource' : ress, \
    'library' : lib, 'instructions' : instrlist , 'form' : f, 'foname' : foname, 'librarylist' : \
    liblist, 'remedied_lib_list' : remliblist, 'sid' : sid, 'stage' : bd, 'info' : info, \
    'lid' : lid, 'expected' : q, 'lastone' : pklastone, 'k' : k, 'version' : version, 'l' : length, 'itrec' : itrec, 'webmaster' : webmaster, 'bdd' : bdd, })

@login_required
def selinstr(request, bdd, sid, lid):

    k =logstatus(request)
    version =epl_version
    suffixe = "@" + str(bdd)

    #Authentication control :
    if not request.user.email in [Library.objects.using(bdd).get(lid =lid).contact, Library.objects.using(bdd).get(lid =lid).contact_bis, Library.objects.using(bdd).get(lid =lid).contact_ter]:
        messages.info(request, _("Vous avez été déconnecté parce que votre identifiant ne vous autorisait pas à accéder à la page demandée"))
        return logout_view(request)
    if not request.user.username[-3:] ==suffixe:
        messages.info(request, _("Vous avez été déconnecté parce que votre identifiant ne vous autorisait pas à accéder à la page demandée"))
        return logout_view(request)

    do = notintime(request, bdd, sid, lid)

    #Control (selinstr only if it's up to the considered library == same conditions as for addinstr if lid not "999999999")
    try:
        if lid !="999999999":
            if ItemRecord.objects.using(bdd).get(sid = sid, lid =lid).status not in [1, 3]:
                return do

        else: # i.e. lid =="999999999"
            return do

    except:
        z =1 #This is just to continue

    #Ressource data :
    itemlist = ItemRecord.objects.using(bdd).filter(sid = sid).exclude(rank =0).order_by("rank", 'pk')
    ress = itemlist[0]

    #Library data :
    lib = Library.objects.using(bdd).get(lid = lid)

    # Library list ordered by 'rank' (except "checker" which must be the last one)
    # to get from the precedent item list above :
    liblist = []
    for e in itemlist:
        liblist.append(Library.objects.using(bdd).get(lid = e.lid))
    liblist.append(Library.objects.using(bdd).get(name = 'checker'))

    #Remedied library list :
    remliblist = []
    for e in itemlist:
        remliblist.append(Library.objects.using(bdd).get(lid = e.lid))
    if (Library.objects.using(bdd).get(lid =lid)).name != 'checker':
        remliblist.remove(Library.objects.using(bdd).get(name = lib.name))

    #Info :
    info =""

    #Stage (bound or not bound) :
    if len(list((Instruction.objects.using(bdd).filter(sid =sid)).filter(name ='checker'))) ==0:
        bd =_('éléments reliés')
        # ress_stage ='reliés'
        expected = "x"
    elif len(list((Instruction.objects.using(bdd).filter(sid =sid)).filter(name ='checker'))) ==1:
        bd =_('éléments non reliés')
        # ress_stage ='non reliés'
        expected = " "
    else:   # (==2)
        bd = _("instructions terminées")

    answer = ""

    LINE_CHOICES =('',''),
    for elmt in Instruction.objects.using(bdd).filter(sid =sid, name =lib.name).order_by('line'):
        if elmt.bound ==expected:
            LINE_CHOICES += (elmt.line, elmt.line),

    if LINE_CHOICES ==(('',''),):
        answer =_("Aucune ligne ne peut être modifiée")

    class Line_Form(forms.Form):
        row = forms.ChoiceField(required = True, widget=forms.Select, choices=LINE_CHOICES[1:])
    f = Line_Form(request.POST or None)

    if f.is_valid():
        linetomodify = f.cleaned_data['row']
        # return modinstr(request, bdd, sid, lid, linetomodify)
        url ="/" + bdd + "/mod/" + str(sid) + "/" + str(lid) + "/" + str(linetomodify)
        return HttpResponseRedirect(url)

    instrlist = Instruction.objects.using(bdd).filter(sid = sid).order_by('line')

    #Library list ordered by 'rank' to get from the precedent item list above :
    liblist = []
    for e in itemlist:
        liblist.append(Library.objects.using(bdd).get(lid = e.lid))
    liblist.append(Library.objects.using(bdd).get(name = 'checker'))

    try:
        itrec =ItemRecord.objects.using(bdd).get(sid =sid, lid =lid)
    except:
        itrec =""

    return render(request, 'epl/selinstruction.html', { 'ressource' : ress, \
    'library' : lib, 'instructions' : instrlist , 'form' : f, 'librarylist' : \
    liblist, 'remedied_lib_list' : remliblist, 'sid' : sid, 'stage' : bd, 'info' : info, \
    'lid' : lid, 'expected' : expected, 'answer' : answer, 'k' : k, 'version' : version, 'itrec' : itrec, 'webmaster' : webmaster, 'bdd' : bdd, })


@login_required
def modinstr(request, bdd, sid, lid, linetomodify):

    k =logstatus(request)
    version =epl_version

    length =0

    class InstructionForm(forms.ModelForm):
        class Meta:
            REM_CHOICES =('',''),
            if Library.objects.using(bdd).all().exclude(name ='checker'):
                for l in Library.objects.using(bdd).all().exclude(name ='checker').order_by('name'):
                    REM_CHOICES += (l.name, l.name),
            model = Instruction
            exclude = ('sid', 'name', 'bound',)
            widgets = {
                'oname' : forms.Select(choices=REM_CHOICES, attrs={'title': _("Intitulé de la bibliothèque ayant précédemment déclaré une 'exception' ou un 'améliorable'")}),
                'descr' : forms.TextInput(attrs={'placeholder': _("1990(2)-1998(12) par ex."), 'title': _("Suite ininterrompue chronologiquement ; le n° de ligne est à déterminer selon l'ordre chronologique de ce champ")}),
                'exc' : forms.TextInput(attrs={'placeholder': _("1991(5) par ex."), 'title': \
                _("éléments manquants dans le segment pour la forme considérée (pas forcément des lacunes si l'on considère la forme reliée)")}),
                'degr' : forms.TextInput(attrs={'placeholder': _("1995(4) par ex."), 'title': \
                _("éléments dégradés (un volume relié dégradé peut être remplacé par les fascicules correspondants en bon état)")}),
            }

    q = "x"
    if len(list((Instruction.objects.using(bdd).filter(sid =sid)).filter(name ='checker'))):
        q =" "
    else:
        q ="x"

    #Library data :
    lib = Library.objects.using(bdd).get(lid = lid)

    suffixe = "@" + str(bdd)

    #Authentication control :
    if not request.user.email in [Library.objects.using(bdd).get(lid =lid).contact, Library.objects.using(bdd).get(lid =lid).contact_bis, Library.objects.using(bdd).get(lid =lid).contact_ter]:
        messages.info(request, _("Vous avez été déconnecté parce que votre identifiant ne vous autorisait pas à accéder à la page demandée"))
        return logout_view(request)
    if not request.user.username[-3:] ==suffixe:
        messages.info(request, _("Vous avez été déconnecté parce que votre identifiant ne vous autorisait pas à accéder à la page demandée"))
        return logout_view(request)

    do = notintime(request, bdd, sid, lid)

    #Control (modinstr only if possible)
    try:
        if lid !="999999999":
            if ItemRecord.objects.using(bdd).get(sid =sid, lid =lid).status not in [1, 3]:
                return do
            if Instruction.objects.using(bdd).get(sid =sid, line =linetomodify).name !=lib.name:
                return do
            if Instruction.objects.using(bdd).get(sid =sid, line =linetomodify).bound !=q:
                return do

        else: # i.e. lid =="999999999"
            return do
    except:
        z =1 #This is just to continue


    #Ressource data :
    itemlist = ItemRecord.objects.using(bdd).filter(sid = sid).exclude(rank =0).order_by("rank", 'pk')
    ress = itemlist[0]

    # Library list ordered by 'rank' (except "checker" which must be the last one)
    # to get from the precedent item list above :
    liblist = []
    for e in itemlist:
        liblist.append(Library.objects.using(bdd).get(lid = e.lid))
    liblist.append(Library.objects.using(bdd).get(name = 'checker'))

    #Remedied library list :
    remliblist = []
    for e in itemlist:
        remliblist.append(Library.objects.using(bdd).get(lid = e.lid))
    if (Library.objects.using(bdd).get(lid =lid)).name != 'checker':
        remliblist.remove(Library.objects.using(bdd).get(name = lib.name))

    #Info :
    info =""

    #Stage (bound or not bound) :
    if len(list((Instruction.objects.using(bdd).filter(sid =sid)).filter(name ='checker'))) ==0:
        bd =_('éléments reliés')
    elif len(list((Instruction.objects.using(bdd).filter(sid =sid)).filter(name ='checker'))) ==1:
        bd =_('éléments non reliés')

    if lid =="999999999":
        do = endinstr(request, bdd, sid, lid)
        return do

    else:
        i = Instruction(sid = sid, name = lib.name)
        if request.method == 'POST':
            f = InstructionForm(request.POST, instance =i)

            REM_CHOICES =('',''),
            bibliolist =[]
            if Instruction.objects.using(bdd).filter(sid =sid).exclude(name =Library.objects.using(bdd).get(lid =lid).name).exclude(name ='checker'):
                for e in Instruction.objects.using(bdd).filter(sid =sid).exclude(name =Library.objects.using(bdd).get(lid =lid).name).exclude(name ='checker'):
                    if (e.exc or e.degr) and Library.objects.using(bdd).get(name =e.name).name not in bibliolist:
                        bibliolist.append(Library.objects.using(bdd).get(name =e.name).name)
                bibliolist.sort()
                length =len(bibliolist)
            if length:
                for l in bibliolist:
                    REM_CHOICES += (l, l),

            class Instr_Form(forms.Form):
                oname = forms.ChoiceField(required = False, widget=forms.Select\
                (attrs={'title': _("Intitulé de la bibliothèque ayant précédemment déclaré une 'exception' ou un 'améliorable'")})\
                , choices=REM_CHOICES, initial =Instruction.objects.using(bdd).get(sid =sid, line =linetomodify).\
                oname, label =_("Bibliothèque remédiée"),)

            foname = Instr_Form(request.POST or None)

            if f.is_valid():
                if foname.is_valid():
                    i.oname = foname.cleaned_data['oname']
                i.bound =q
                #A line may only be registered once :
                if len(Instruction.objects.using(bdd).exclude(line =linetomodify).filter(sid =sid, name =lib.name, bound =i.bound, oname =i.oname, descr =i.descr, exc =i.exc, degr =i.degr)):
                    info = _("Une autre ligne contient déjà les mêmes données.")
                else:
                    Instruction.objects.using(bdd).get(sid =sid, name =lib.name, line =linetomodify).delete()
                    if i.line <linetomodify:
                        # i.line +=1
                        i.time =Now()
                        i.save(using=bdd)
                    else:
                        i.line +=1
                        i.time =Now()
                        i.save(using=bdd)

            instrlist = Instruction.objects.using(bdd).filter(sid = sid).order_by('line')

            try:
                pklastone = Instruction.objects.using(bdd).filter(sid = sid).latest('time').pk
            except:
                pklastone =0
            if info =="":
                # return addinstr(request, bdd, sid, lid)
                url ="/" + bdd + "/add/" + str(sid) + "/" + str(lid)
                return HttpResponseRedirect(url) # Renumbering shall be done there.
        else:
            #Instruction form instanciation and validation :
            f = InstructionForm(instance =i, initial = {
            'line' : Instruction.objects.using(bdd).get(sid =sid, line =linetomodify).line - 1,
            # 'oname' : Instruction.objects.using(bdd).get(sid =sid, line =linetomodify).oname,
            'descr' : Instruction.objects.using(bdd).get(sid =sid, line =linetomodify).descr,
            'exc' : Instruction.objects.using(bdd).get(sid =sid, line =linetomodify).exc,
            'degr' : Instruction.objects.using(bdd).get(sid =sid, line =linetomodify).degr,
            })

            REM_CHOICES =('',''),
            bibliolist =[]
            if Instruction.objects.using(bdd).filter(sid =sid).exclude(name =Library.objects.using(bdd).get(lid =lid).name).exclude(name ='checker'):
                for e in Instruction.objects.using(bdd).filter(sid =sid).exclude(name =Library.objects.using(bdd).get(lid =lid).name).exclude(name ='checker'):
                    if (e.exc or e.degr) and Library.objects.using(bdd).get(name =e.name).name not in bibliolist:
                        bibliolist.append(Library.objects.using(bdd).get(name =e.name).name)
                bibliolist.sort()
                length =len(bibliolist)
            if length:
                for l in bibliolist:
                    REM_CHOICES += (l, l),

            class Instr_Form(forms.Form):
                oname = forms.ChoiceField(required = False, widget=forms.Select\
                (attrs={'title': _("Intitulé de la bibliothèque ayant précédemment déclaré une 'exception' ou un 'améliorable'")})\
                , choices=REM_CHOICES, initial =Instruction.objects.using(bdd).get(sid =sid, line =linetomodify).\
                oname, label =_("Bibliothèque remédiée"),)

            foname = Instr_Form()

            instrlist = Instruction.objects.using(bdd).filter(sid = sid).order_by('line')

    try:
        itrec =ItemRecord.objects.using(bdd).get(sid =sid, lid =lid)
    except:
        itrec =""

    return render(request, 'epl/modinstruction.html', { 'ressource' : ress, \
    'library' : lib, 'instructions' : instrlist , 'form' : f, 'foname' : foname, 'librarylist' : \
    liblist, 'remedied_lib_list' : remliblist, 'sid' : sid, 'stage' : bd, 'info' : info, \
    'lid' : lid, 'expected' : q, 'k' : k, 'version' : version, 'l' : length, 'line' : linetomodify, 'itrec' : itrec, 'webmaster' : webmaster, 'bdd' : bdd, })


@login_required
def delinstr(request, bdd, sid, lid):

    k =logstatus(request)
    version =epl_version
    suffixe = "@" + str(bdd)

    #Authentication control :
    if not request.user.email in [Library.objects.using(bdd).get(lid =lid).contact, Library.objects.using(bdd).get(lid =lid).contact_bis, Library.objects.using(bdd).get(lid =lid).contact_ter]:
        messages.info(request, _("Vous avez été déconnecté parce que votre identifiant ne vous autorisait pas à accéder à la page demandée"))
        return logout_view(request)
    if not request.user.username[-3:] ==suffixe:
        messages.info(request, _("Vous avez été déconnecté parce que votre identifiant ne vous autorisait pas à accéder à la page demandée"))
        return logout_view(request)

    do = notintime(request, bdd, sid, lid)

    #Control (delinstr only if it's up to the considered library == same conditions as for addinstr if lid not "999999999")
    try:
        if lid !="999999999":
            if ItemRecord.objects.using(bdd).get(sid = sid, lid =lid).status not in [1, 3]:
                return do

        else: # i.e. lid =="999999999"
            return do

    except:
        z =1 #This is just to continue

    #Ressource data :
    itemlist = ItemRecord.objects.using(bdd).filter(sid = sid).exclude(rank =0).order_by("rank", 'pk')
    ress = itemlist[0]

    #Library data :
    lib = Library.objects.using(bdd).get(lid = lid)

    # Library list ordered by 'rank' (except "checker" which must be the last one)
    # to get from the precedent item list above :
    liblist = []
    for e in itemlist:
        liblist.append(Library.objects.using(bdd).get(lid = e.lid))
    liblist.append(Library.objects.using(bdd).get(name = 'checker'))

    #Remedied library list :
    remliblist = []
    for e in itemlist:
        remliblist.append(Library.objects.using(bdd).get(lid = e.lid))
    if (Library.objects.using(bdd).get(lid =lid)).name != 'checker':
        remliblist.remove(Library.objects.using(bdd).get(name = lib.name))

    #Info :
    info =""

    #Stage (bound or not bound) :
    if len(list((Instruction.objects.using(bdd).filter(sid =sid)).filter(name ='checker'))) ==0:
        bd =_('éléments reliés')
        # ress_stage ='reliés'
        expected = "x"
    elif len(list((Instruction.objects.using(bdd).filter(sid =sid)).filter(name ='checker'))) ==1:
        bd =_('éléments non reliés')
        # ress_stage ='non reliés'
        expected = " "
    else:   # (==2)
        bd = _("instructions terminées")

    answer = ""

    LINE_CHOICES =('',''),
    for elmt in Instruction.objects.using(bdd).filter(sid =sid, name =lib.name).order_by('line'):
        if elmt.bound ==expected:
            LINE_CHOICES += (elmt.line, elmt.line),

    if LINE_CHOICES ==(('',''),):
        answer =1

    class Lines_Form(forms.Form):
        rows = forms.CharField(required = True, widget=forms.TextInput(attrs={'placeholder'\
        : "5, 8-12, 14", 'title': _("Par exemple : 5, 8-12, 14 pour supprimer les lignes 5, 8 à 12 et 14.")}))
    f = Lines_Form(request.POST or None)
    if f.is_valid():
        toparse = f.cleaned_data['rows'] # is a string
        toparse =toparse.replace(' ', '')
        toparse =toparse.split(',')
        linestodel =[]
        for elmt in toparse:
            try:
                linestodel.append(int(elmt))
            except:
                elmt =elmt.split('-')
                begin, end =int(elmt[0]), int(elmt[1])+1
                for subelmt in range(begin, end):
                    linestodel.append(subelmt)
        for todel in linestodel:
            try:
                j = Instruction.objects.using(bdd).get(sid =sid, bound = expected, name =lib.name, line =todel)
            except:
                answer = _(" <=== Expression invalide (vérifiez les conditions indiquées) ")
        if answer == "":
            for todel in linestodel:
                Instruction.objects.using(bdd).get(sid =sid, name =lib.name, line =todel).delete()
            # return addinstr(request, bdd, sid, lid)
            url ="/" + bdd + "/add/" + str(sid) + "/" + str(lid)
            return HttpResponseRedirect(url) # Renumbering shall be done there.

    instrlist = Instruction.objects.using(bdd).filter(sid = sid).order_by('line')

    #Library list ordered by 'rank' to get from the precedent item list above :
    liblist = []
    for e in itemlist:
        liblist.append(Library.objects.using(bdd).get(lid = e.lid))
    liblist.append(Library.objects.using(bdd).get(name = 'checker'))

    try:
        itrec =ItemRecord.objects.using(bdd).get(sid =sid, lid =lid)
    except:
        itrec =""

    return render(request, 'epl/delinstruction.html', { 'ressource' : ress, \
    'library' : lib, 'instructions' : instrlist , 'form' : f, 'librarylist' : \
    liblist, 'remedied_lib_list' : remliblist, 'sid' : sid, 'stage' : bd, 'info' : info, \
    'lid' : lid, 'expected' : expected, 'answer' : answer, 'k' : k, 'version' : version, 'itrec' : itrec, 'webmaster' : webmaster, 'bdd' : bdd, })


@login_required
def endinstr(request, bdd, sid, lid):

    k =logstatus(request)
    version =epl_version
    suffixe = "@" + str(bdd)

    #Authentication control :
    if not request.user.email in [Library.objects.using(bdd).get(lid =lid).contact, Library.objects.using(bdd).get(lid =lid).contact_bis, Library.objects.using(bdd).get(lid =lid).contact_ter]:
        messages.info(request, _("Vous avez été déconnecté parce que votre identifiant ne vous autorisait pas à accéder à la page demandée"))
        return logout_view(request)
    if not request.user.username[-3:] ==suffixe:
        messages.info(request, _("Vous avez été déconnecté parce que votre identifiant ne vous autorisait pas à accéder à la page demandée"))
        return logout_view(request)

    #Control (endinstr only if it's up to the considered library == same conditions as for addinstr)
    try:
        if lid !="999999999":
            if ItemRecord.objects.using(bdd).get(sid = sid, lid =lid).status not in [1, 3]:
                return notintime(request, bdd, sid, lid)

        else: # i.e. lid =="999999999"
            if len(list((Instruction.objects.using(bdd).filter(sid =sid)).filter(name ='checker'))) ==2:
                return notintime(request, bdd, sid, lid)
            elif len(list((Instruction.objects.using(bdd).filter(sid =sid)).filter(name ='checker'))) ==1:
                if len(list(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0))) != len(list(ItemRecord.objects.using(bdd).filter(sid =sid, status =4))):
                    return notintime(request, bdd, sid, lid)
            else: # i.e. len(list((Instruction.objects.using(bdd).filter(sid =sid)).filter(name ='checker'))) ==0
                if len(list(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0))) != len(list(ItemRecord.objects.using(bdd).filter(sid =sid, status =2))):
                    return notintime(request, bdd, sid, lid)
    except:
        z =1 #This is just to continue

    # Self instruction if no instruction
    answer = ""
    if lid != "999999999" and len(Instruction.objects.using(bdd).filter(sid =sid, name ='checker')) ==0:
        if not Instruction.objects.using(bdd).filter(sid =sid, name =Library.objects.using(bdd).get(lid =lid).name):
            answer =_("Votre collection ne comprend pas d'éléments reliés améliorant la résultante")
            #Renumbering instruction lines :
            for instr in Instruction.objects.using(bdd).filter(sid = sid):
                instr.line =instr.line +1
                instr.save(using=bdd)
            blankinst =Instruction(line =1, sid =sid, name =Library.objects.using(bdd).get(lid =lid)\
            .name, bound ="x", descr =_("-- Néant --"), time =Now())
            blankinst.save(using=bdd)

    elif lid != "999999999" and len(Instruction.objects.using(bdd).filter(sid =sid, name ='checker')) ==1:
        if not Instruction.objects.using(bdd).filter(sid =sid, name =Library.objects.using(bdd).get(lid =lid).name, bound =" "):
            answer =_("Votre collection ne comprend pas d'éléments non reliés améliorant la résultante")
            #Renumbering instruction lines :
            for instr in Instruction.objects.using(bdd).filter(sid = sid).exclude(line =1):
                instr.line =instr.line +1
                instr.save(using=bdd)
            blankinst =Instruction(line =2, sid =sid, name =Library.objects.using(bdd).get(lid =lid)\
            .name, bound =" ", descr =_("-- Néant --"), time =Now())
            blankinst.save(using=bdd)

    #Ressource data :
    itemlist = ItemRecord.objects.using(bdd).filter(sid = sid).exclude(rank =0).order_by("rank", 'pk')
    ress = itemlist[0]

    #Library data :
    lib = Library.objects.using(bdd).get(lid = lid)

    # Library list ordered by 'rank' (except "checker" which must be the last one)
    # to get from the precedent item list above :
    liblist = []
    liblistrict = []
    for e in itemlist:
        liblist.append(Library.objects.using(bdd).get(lid = e.lid))
        liblistrict.append(Library.objects.using(bdd).get(lid = e.lid)) #is used later for mailing
    liblist.append(Library.objects.using(bdd).get(name = 'checker'))

    #Remedied library list :
    remliblist = []
    for e in itemlist:
        remliblist.append(Library.objects.using(bdd).get(lid = e.lid))
    if (Library.objects.using(bdd).get(lid =lid)).name != 'checker':
        remliblist.remove(Library.objects.using(bdd).get(name = lib.name))

    #Info :
    info =""

    #Stage (bound or not bound) :
    if len(list((Instruction.objects.using(bdd).filter(sid =sid)).filter(name ='checker'))) ==0:
        bd =_('éléments reliés')
        # ress_stage ='reliés'
        expected = "x"
    elif len(list((Instruction.objects.using(bdd).filter(sid =sid)).filter(name ='checker'))) ==1:
        bd =_('éléments non reliés')
        # ress_stage ='non reliés'
        expected = " "
    else:   # (==2)
        bd = _("instructions terminées")
        expected = _("ni relié, ni non reliés")

    y = Flag()
    z = CheckForm(request.POST or None, instance =y)

    t = Check()
    u = AdminCheckForm(request.POST or None, instance =t)


    if lid =="999999999":
        nextlib = liblist[0]
        nextlid = nextlib.lid
        if u.is_valid() and t.checkin =="Visa":
            checkerinstruction = Instruction(sid =sid, name ="checker")
            checkerinstruction.line =0
            if len(Instruction.objects.using(bdd).filter(sid =sid, name ='checker')) ==0:
                checkerinstruction.bound ="x"
            if len(Instruction.objects.using(bdd).filter(sid =sid, name ='checker')) ==1:
                checkerinstruction.bound =" "
            time =Now()
            checkerinstruction.descr =time
            checkerinstruction.time =time
            checkerinstruction.save(using=bdd)

            #Renumbering instruction lines :
            try:
                instr = Instruction.objects.using(bdd).filter(sid = sid).order_by('line', 'pk')
                j, g =0, 1
                while j <= len(instr):
                    instr[j].line = g
                    instr[j].save(using=bdd)
                    j +=1
                    g +=1
            except:
                pass

            instrlist = Instruction.objects.using(bdd).filter(sid = sid).order_by('line')

            #Status changing :
            j = ItemRecord.objects.using(bdd).get(sid =sid, rank =1)
            if len(Instruction.objects.using(bdd).filter(sid =sid, name ='checker')) ==1:
                if j.status !=3:
                    j.status = 3
                    j.save(using=bdd)
                    if Proj_setting.objects.using(bdd).all()[0].ins:
                        #Message data :
                        subject = "eplouribousse / instruction : " + bdd + " / " + str(sid) + " / " + str(nextlid)
                        host = str(request.get_host())
                        message = _("Votre tour est venu d'instruire la fiche eplouribousse pour le ppn ") + str(sid) +\
                        " :\n" + "http://" + host + "/" + bdd + "/add/" + str(sid) + '/' + str(nextlid)
                        dest =[]
                        if Utilisateur.objects.using(bdd).get(mail =nextlib.contact).ins:
                            dest.append(nextlib.contact)
                        try:
                            if Utilisateur.objects.using(bdd).get(mail =nextlib.contact_bis).ins:
                                dest.append(nextlib.contact_bis)
                        except:
                            st =1 #bidon pour passer
                        try:
                            if Utilisateur.objects.using(bdd).get(mail =nextlib.contact_ter).ins:
                                dest.append(nextlib.contact_ter)
                        except:
                            st =1 #bidon pour passer
                        if len(dest):
                            send_mail(subject, message, replymail, dest, fail_silently=True, )

            if len(Instruction.objects.using(bdd).filter(sid =sid, name ='checker')) ==2:
                for e in ItemRecord.objects.using(bdd).filter(sid =sid, status =4):
                    e.status = 5
                    e.save(using=bdd)
                # envoi de l'alerte le cas échéant (début)
                if Proj_setting.objects.using(bdd).all()[0].edi:
                    for librelmt in liblistrict:
                        #Message data :
                        subject = "eplouribousse / fiche : " + bdd + " / " + str(sid) + " / " + str(librelmt.lid)
                        host = str(request.get_host())
                        message = _("La résultante est désormais disponible pour le ppn ") + str(sid) +\
                        " :\n" + "http://" + host + "/" + bdd + "/ed/" + str(sid) + '/' + str(librelmt.lid)
                        dest =[]
                        if Utilisateur.objects.using(bdd).get(mail =librelmt.contact).edi:
                            dest.append(librelmt.contact)
                        try:
                            if Utilisateur.objects.using(bdd).get(mail =librelmt.contact_bis).edi:
                                dest.append(librelmt.contact_bis)
                        except:
                            st =1 #bidon pour passer
                        try:
                            if Utilisateur.objects.using(bdd).get(mail =librelmt.contact_ter).edi:
                                dest.append(librelmt.contact_ter)
                        except:
                            st =1 #bidon pour passer
                        if len(dest):
                            send_mail(subject, message, replymail, dest, fail_silently=True, )
                # envoi de l'alerte le cas échéant (fin)

            #renvoi vers la liste adéquate en cas de recours au lien envoyé dans les alertes mail
            try:
                newestfeature =Feature.objects.using(bdd).get(libname =Library.objects.using(bdd).get(lid =lid).name)
                key =newestfeature.feaname.split('$')
                if key[0] in ["30", "31", "32", "33", "34", "35", "36", "37", "38"]:
                    return router(request, bdd, lid)
                else:
                    return instrtodo(request, bdd, lid, 'title')
            except:
                return instrtodo(request, bdd, lid, 'title')

        elif u.is_valid() and t.checkin =="Notify": #In this case BDD administrator will be informed of errors in the instructions.
            # Change all ItemRecords status (except those with rank =0) for the considered sid to status =6
            for e in ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0):
                e.status =6
                e.save(using=bdd)

            #Message data to the BDD administrator(s):
            subject = "eplouribousse : " + bdd + " / " + str(sid) + " / " + "status = 6"
            host = str(request.get_host())
            message = _("Fiche défectueuse signalée par le contrôleur pour le ppn ") + str(sid) +\
            "\n" + _("Une intervention est attendue de la part d'un des administrateurs de la base") +\
            " :\n" + "http://" + host + "/" + bdd + "/current_status/" + str(sid) + '/' + str(lid) + \
            "\n" + _("Merci !")
            destprov = BddAdmin.objects.using(bdd).all()
            dest =[]
            for d in destprov:
                dest.append(d.contact)
            exp = request.user.email
            send_mail(subject, message, exp, dest, fail_silently=True, )

            try:
                newestfeature =Feature.objects.using(bdd).get(libname =Library.objects.using(bdd).get(lid =lid).name)
                key =newestfeature.feaname.split('$')
                if key[0] in ["30", "31", "32", "33", "34", "35", "36", "37", "38"]:
                    return router(request, bdd, lid)
                else:
                    return instrtodo(request, bdd, lid, 'title')
            except:
                return instrtodo(request, bdd, lid, 'title')

    else: #lid !="999999999"
        if z.is_valid() and y.flag ==True:

            if len(Instruction.objects.using(bdd).filter(sid =sid, name ='checker')) ==0:

                if ItemRecord.objects.using(bdd).filter(sid =sid, status =0).exclude(lid =lid).exclude(rank =0).exists():
                    nextitem = ItemRecord.objects.using(bdd).filter(sid =sid, status =0).exclude(lid =lid).exclude(rank =0).order_by('rank', 'pk')[0]
                    nextlid = nextitem.lid
                    nextlib = Library.objects.using(bdd).get(lid =nextlid)
                    j, g = ItemRecord.objects.using(bdd).get(sid =sid, lid =lid), ItemRecord.objects.using(bdd).get(sid =sid, lid =nextlid)
                    if j.status !=2:
                        j.status, g.status = 2, 1
                        j.save(using=bdd)
                        g.save(using=bdd)
                else:
                    #(No nextitem, the whole pool of libraries finished instructing the current form, i.e. bound or not bound.)
                    nextlid = Library.objects.using(bdd).get(lid ="999999999").lid
                    nextlib = Library.objects.using(bdd).get(lid =nextlid)
                    j = ItemRecord.objects.using(bdd).get(sid =sid, lid =lid)
                    if j.status !=2:
                        j.status = 2
                        j.save(using=bdd)

            elif len(Instruction.objects.using(bdd).filter(sid =sid, name ='checker')) ==1:

                if ItemRecord.objects.using(bdd).filter(sid =sid, status =2).exclude(lid =lid).exclude(rank =0).exists():
                    nextitem = ItemRecord.objects.using(bdd).filter(sid =sid, status =2).exclude(lid =lid).exclude(rank =0).order_by('rank', 'pk')[0]
                    nextlid = nextitem.lid
                    nextlib = Library.objects.using(bdd).get(lid =nextlid)
                    j, g = ItemRecord.objects.using(bdd).get(sid =sid, lid =lid), ItemRecord.objects.using(bdd).get(sid =sid, lid =nextlid)
                    if j.status !=4:
                        j.status, g.status = 4, 3
                        j.save(using=bdd)
                        g.save(using=bdd)
                else:
                    #(No nextitem, the whole pool of libraries finished instructing the current form, i.e. bound or not bound.)
                    nextlid = Library.objects.using(bdd).get(lid ="999999999").lid
                    nextlib = Library.objects.using(bdd).get(lid =nextlid)
                    j = ItemRecord.objects.using(bdd).get(sid =sid, lid =lid)
                    if j.status !=4:
                        j.status = 4
                        j.save(using=bdd)
            if Proj_setting.objects.using(bdd).all()[0].ins:
                #Message data :
                subject = "eplouribousse / instruction : " + bdd + " / " + str(sid) + " / " + str(nextlid)
                host = str(request.get_host())
                message = _("Votre tour est venu d'instruire la fiche eplouribousse pour le ppn ") + str(sid) +\
                " :\n" + "http://" + host + "/" + bdd + "/add/" + str(sid) + '/' + str(nextlid)
                dest =[]
                if Utilisateur.objects.using(bdd).get(mail =nextlib.contact).ins:
                    dest.append(nextlib.contact)
                try:
                    if Utilisateur.objects.using(bdd).get(mail =nextlib.contact_bis).ins:
                        dest.append(nextlib.contact_bis)
                except:
                    st =1 #bidon pour passer
                try:
                    if Utilisateur.objects.using(bdd).get(mail =nextlib.contact_ter).ins:
                        dest.append(nextlib.contact_ter)
                except:
                    st =1 #bidon pour passer
                if len(dest):
                    send_mail(subject, message, replymail, dest, fail_silently=True, )

            try:
                newestfeature =Feature.objects.using(bdd).get(libname =Library.objects.using(bdd).get(lid =lid).name)
                key =newestfeature.feaname.split('$')
                if key[0] in ["30", "31", "32", "33", "34", "35", "36", "37", "38"]:
                    return router(request, bdd, lid)
                else:
                    return instrtodo(request, bdd, lid, 'title')
            except:
                return instrtodo(request, bdd, lid, 'title')

        if z.is_valid() and y.flag ==False:
            info =_("Vous n'avez pas coché !")

    instrlist = Instruction.objects.using(bdd).filter(sid = sid).order_by('line')

    try:
        itrec =ItemRecord.objects.using(bdd).get(sid =sid, lid =lid)
    except:
        itrec =""

    return render(request, 'epl/endinstruction.html', { 'ressource' : ress, \
    'library' : lib, 'instructions' : instrlist , 'librarylist' : \
    liblist, 'remedied_lib_list' : remliblist, 'sid' : sid, 'stage' : bd, 'info' : info, \
    'lid' : lid, 'checkform' : z, 'checkerform' : u, 'expected' : expected, 'k' : k, \
    'version' : version, 'itrec' : itrec, 'webmaster' : webmaster, 'answer' : answer, 'bdd' : bdd, })

@edmode1
def ranktotake(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name
    
    newestfeat(request, bdd, libname, "10")

    reclist = list(ItemRecord.objects.using(bdd).filter(lid = lid, rank = 99).order_by(sort))

    resslist = []
    for e in reclist:
        itemlist = list(ItemRecord.objects.using(bdd).filter(sid = e.sid).exclude(rank =0))
        if len(itemlist) > 1:
            resslist.append(e)
    l = len(resslist)
    
    sidlist = [ir.sid for ir in resslist]

    nlib = len(Library.objects.using(bdd).exclude(lid ="999999999"))

    try:
        lastrked =ItemRecord.objects.using(bdd).get(lid =lid, last =1)
        if len(Instruction.objects.using(bdd).filter(sid =lastrked.sid)):
            lastrked =None
    except:
        lastrked =None

    return render(request, 'epl/to_rank_list.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'l' : l, 'k' : k, 'nlib' : nlib, \
    'lastrked' : lastrked, 'version' : version, 'sort' : sort, \
    'webmaster' : webmaster, 'bdd' : bdd, 'sidlist' : sidlist,})

@edmode1
def modifranklist(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    reclist = list(ItemRecord.objects.using(bdd).filter(lid = lid).exclude(rank = 99)\
    .exclude(status =2).exclude(status =3).exclude(status =4).\
    exclude(status =5).exclude(status =6).order_by(sort))

    resslist = []
    for e in reclist:
        if not len(list(Instruction.objects.using(bdd).filter(sid = e.sid))):
            resslist.append(e)

    l = len(resslist)
    
    sidlist = [ir.sid for ir in resslist]

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name
    newestfeat(request, bdd, libname, "12")
    
    nlib = len(Library.objects.using(bdd).exclude(lid ="999999999"))

    try:
        lastrked =ItemRecord.objects.using(bdd).get(lid =lid, last =1)
        if len(Instruction.objects.using(bdd).filter(sid =lastrked.sid)):
            lastrked =None
    except:
        lastrked =None

    return render(request, 'epl/modifrklist.html', { 'resslist' : resslist, 'sidlist' : sidlist, \
    'lid' : lid, 'libname' : libname, 'l' : l, 'k' : k, 'nlib' : nlib, \
    'lastrked' : lastrked, 'version' : version, 'sort' : sort, 'webmaster' : webmaster, 'bdd' : bdd, })

@edmode4
def filter_rklist(request, bdd, lid):

    k =logstatus(request)
    version =epl_version

    "Filter rk list"

    libname = (Library.objects.using(bdd).get(lid =lid)).name

    libch = ('checker','checker'),
    if Library.objects.using(bdd).all().exclude(name ='checker').exclude(name =libname):
        for l in Library.objects.using(bdd).all().exclude(name ='checker').exclude(name =libname).order_by('name'):
            libch += (l.name, l.name),

    class XlibForm(forms.Form):
        name = forms.ChoiceField(required = True, widget=forms.Select, choices=libch[1:], label =_("Autre bibliothèque impliquée"))

    form = XlibForm(request.POST or None)
    if form.is_valid():
        xlib = form.cleaned_data['name']
        xlid = Library.objects.using(bdd).get(name =xlib).lid
        return xranktotake(request, bdd, lid, xlid, 'title')

    return render(request, 'epl/filter_rklist.html', locals())

@edmode2
def xranktotake(request, bdd, lid, xlid, sort):

    k =logstatus(request)
    version =epl_version

    #Getting ressources whose this lid must but has not yet taken rank :
    reclist = list(ItemRecord.objects.using(bdd).filter(lid = lid, rank = 99).order_by(sort))

    resslist = []
    for e in reclist:
        itemlist = list(ItemRecord.objects.using(bdd).filter(sid = e.sid).exclude(rank =0))
        if len(itemlist) > 1 and list(ItemRecord.objects.using(bdd).filter(sid = e.sid, lid = xlid).exclude(rank =0)):
            resslist.append(e)
    l = len(resslist)
    
    sidlist = [ir.sid for ir in resslist]

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name
    xlibname = Library.objects.using(bdd).get(lid =xlid).name
    xnewestfeat(request, bdd, libname, "11", xlid)

    try:
        lastrked =ItemRecord.objects.using(bdd).get(lid =lid, last =1)
        if len(Instruction.objects.using(bdd).filter(sid =lastrked.sid)):
            lastrked =None
    except:
        lastrked =None

    return render(request, 'epl/xto_rank_list.html', { 'resslist' : resslist, 'sidlist' : sidlist, \
    'lid' : lid, 'libname' : libname, 'l' : l, 'k' : k, 'xlibname' : xlibname, \
    'lastrked' : lastrked, 'version' : version, 'sort' : sort, 'xlid' : xlid, 'webmaster' : webmaster, 'bdd' : bdd, })

@edmode3
def excllist(request, bdd):

    k =logstatus(request)
    version =epl_version
    
    EXCLUSION_CHOICES = ('Tous', _('Tous')),
    for e in list(ItemRecord.objects.using(bdd).filter(rank =0).exclude(excl ="Autre (Commenter)").values_list('excl', flat =True).distinct()):
        EXCLUSION_CHOICES += (e, e),
    EXCLUSION_CHOICES += ("Autre (Commenter)", _("Autre (Commenter)")),

    l =0

    libch = ('',''),
    for l in Library.objects.using(bdd).all().exclude(name ='checker').order_by('name'):
        libch += (l.name, l.name),

    sortch = ('title',_('titre')), ('excl',_("motif d'exclusion")), ('cn',_('cote et titre')), ('sid',_('ppn')),

    stillmodch = ('Peu importe',_('Peu importe')), ('oui',_('oui')), ('non',_('non')),

    class Lib_Form(forms.Form):
        lib = forms.ChoiceField(required = True, widget=forms.Select, choices=libch, label =_("Votre bibliothèque"))
        sortingby = forms.ChoiceField(required = True, widget=forms.Select, choices=sortch, label =_("Critère de tri"))
        exclreason = forms.ChoiceField(required = False, widget=forms.Select, choices=EXCLUSION_CHOICES, label =_("Motif d'exclusion"))
        stillmod = forms.ChoiceField(required = False, widget=forms.Select, choices=stillmodch, label =_("Modifiable ?"))
    form = Lib_Form(request.POST or None)
    if form.is_valid():
        l =1
        lib = form.cleaned_data['lib']
        sort = form.cleaned_data['sortingby']
        exclreason = form.cleaned_data['exclreason']
        stillmod = form.cleaned_data['stillmod']

        lid = Library.objects.using(bdd).get(name =lib).lid
        name = lib

        if exclreason !='Tous' and stillmod != 'Peu importe':
            excl_list = []
            if stillmod =="oui":
                for elmt in ItemRecord.objects.using(bdd).filter(lid =lid, rank =0, excl =exclreason).order_by(sort):
                    if not Instruction.objects.using(bdd).filter(sid =elmt.sid):
                        if not elmt in excl_list:
                            excl_list.append(elmt)
            elif stillmod =="non":
                for elmt in ItemRecord.objects.using(bdd).filter(lid =lid, rank =0, excl =exclreason).order_by(sort):
                    if Instruction.objects.using(bdd).filter(sid =elmt.sid):
                        if not elmt in excl_list:
                            excl_list.append(elmt)
        elif exclreason !='Tous' and stillmod == 'Peu importe':
            excl_list =ItemRecord.objects.using(bdd).filter(lid =lid, rank =0, excl =exclreason).order_by(sort)
        elif stillmod != 'Peu importe' and exclreason =='Tous':
            excl_list = []
            if stillmod =="oui":
                for elmt in ItemRecord.objects.using(bdd).filter(lid =lid, rank =0).order_by(sort):
                    if not Instruction.objects.using(bdd).filter(sid =elmt.sid):
                        if not elmt in excl_list:
                            excl_list.append(elmt)
            if stillmod =="non":
                for elmt in ItemRecord.objects.using(bdd).filter(lid =lid, rank =0).order_by(sort):
                    if Instruction.objects.using(bdd).filter(sid =elmt.sid):
                        if not elmt in excl_list:
                            excl_list.append(elmt)
        elif stillmod == 'Peu importe' and exclreason =='Tous':
            excl_list =ItemRecord.objects.using(bdd).filter(lid =lid, rank =0).order_by(sort)

        length =len(excl_list)
        sidlist = [ir.sid for ir in excl_list]

    return render(request, 'epl/excl.html', locals())

@edmode3
def faulty(request, bdd):

    k =logstatus(request)
    version =epl_version

    l =0

    libch = ('checker','checker'),
    for l in Library.objects.using(bdd).all().exclude(name ='checker').order_by('name'):
        libch += (l.name, l.name),

    sortch =('title',_('titre')), ('cn',_('cote et titre')), ('sid',_('ppn')),

    class Lib_Form(forms.Form):
        lib = forms.ChoiceField(required = True, widget=forms.Select, choices=libch, label =_("Votre bibliothèque"))
        sortingby = forms.ChoiceField(required = True, widget=forms.Select, choices=sortch, label =_("Critère de tri"))
    form = Lib_Form(request.POST or None)
    if form.is_valid():
        l =1
        lib = form.cleaned_data['lib']
        sort = form.cleaned_data['sortingby']
        lid = Library.objects.using(bdd).get(name =lib).lid
        name = lib

        faulty_list =ItemRecord.objects.using(bdd).filter(rank =1, status =6).order_by(sort)

        length =len(faulty_list)
        sidlist = [ir.sid for ir in faulty_list]

    return render(request, 'epl/faulty.html', locals())

@edmode1
def arbitration(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    #For the lid identified library, getting ressources whose at \
    #least 2 libraries, including the considered one, took rank =1 \
    #(even if other libraries have not yet taken rank)
    #or all libraries have taken rank, none of them the rank 1

    #Initialization of the ressources to arbitrate :
    resslista = []
    resslistb = []

    for e in ItemRecord.objects.using(bdd).filter(lid =lid, rank = 1, status =0):
        sid = e.sid
        if ItemRecord.objects.using(bdd).exclude(lid =lid).filter(sid =sid, rank = 1):
            resslista.append(e)

    for e in ItemRecord.objects.using(bdd).filter(lid =lid, status =0).exclude(rank =1).exclude(rank =0).exclude(rank =99):
        sid = e.sid
        if len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) ==0 and \
        len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =99)) ==0 and \
        len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) >1:
            resslistb.append(e)

    resslist = resslista + resslistb

    if sort =='sid':
        resslist = sorted(resslist, key=serial_id)
    elif sort =='cn':
        resslist = sorted(resslist, key=coll_cn)
    else:
        resslist = sorted(resslist, key=serial_title)

    size = len(resslist)
    
    sidlist = [ir.sid for ir in resslist]

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name
    newestfeat(request, bdd, libname, "20")

    nlib = len(Library.objects.using(bdd).exclude(lid ="999999999"))

    try:
        lastrked =ItemRecord.objects.using(bdd).get(lid =lid, last =1)
        if len(Instruction.objects.using(bdd).filter(sid =lastrked.sid)):
            lastrked =None
    except:
        lastrked =None

    return render(request, 'epl/arbitration.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'size' : size, 'k' : k, 'sidlist' : sidlist, \
    'lastrked' : lastrked, 'version' : version, 'nlib' : nlib, 'sort' : sort, 'webmaster' : webmaster, 'bdd' : bdd, })

@edmode1
def arbrk1(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    #For the lid identified library, getting ressources whose at \
    #least 2 libraries, including the considered one, took rank =1 \
    #(even if other libraries have not yet taken rank)
    #or all libraries have taken rank, none of them the rank 1

    #Initialization of the ressources to arbitrate :
    resslist = []

    reclist = list(ItemRecord.objects.using(bdd).filter(lid =lid, rank = 1, status =0).order_by(sort))

    for e in reclist:
        sid = e.sid
        if ItemRecord.objects.using(bdd).exclude(lid =lid).filter(sid =sid, rank = 1):
            resslist.append(e)

    size = len(resslist)
    
    sidlist = [ir.sid for ir in resslist]

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name
    newestfeat(request, bdd, libname, "24")

    try:
        lastrked =ItemRecord.objects.using(bdd).get(lid =lid, last =1)
        if len(Instruction.objects.using(bdd).filter(sid =lastrked.sid)):
            lastrked =None
    except:
        lastrked =None

    return render(request, 'epl/arbrk1.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'size' : size, 'k' : k, 'sidlist' : sidlist, \
    'lastrked' : lastrked, 'version' : version, 'sort' : sort, 'webmaster' : webmaster, 'bdd' : bdd, })

@edmode1
def arbnork1(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    #For the lid identified library, getting ressources whose at \
    #least 2 libraries, including the considered one, took rank =1 \
    #(even if other libraries have not yet taken rank)
    #or all libraries have taken rank, none of them the rank 1

    #Initialization of the ressources to arbitrate :
    resslist = []

    reclist = list(ItemRecord.objects.using(bdd).filter(lid =lid, status =0).exclude(rank =1).exclude(rank =0).exclude(rank =99).order_by(sort))

    for e in reclist:
        sid = e.sid
        if len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) ==0 and \
        len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =99)) ==0 and \
        len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) >1:
            resslist.append(e)

    size = len(resslist)
    
    sidlist = [ir.sid for ir in resslist]

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name
    newestfeat(request, bdd, libname, "25")

    try:
        lastrked =ItemRecord.objects.using(bdd).get(lid =lid, last =1)
        if len(Instruction.objects.using(bdd).filter(sid =lastrked.sid)):
            lastrked =None
    except:
        lastrked =None

    return render(request, 'epl/arbnork1.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'size' : size, 'k' : k, 'sidlist' : sidlist, \
    'lastrked' : lastrked, 'version' : version, 'sort' : sort, 'webmaster' : webmaster, 'bdd' : bdd, })

@edmode4
def filter_arblist(request, bdd, lid):

    k =logstatus(request)
    version =epl_version

    "Filter arb list"

    libname = (Library.objects.using(bdd).get(lid =lid)).name

    libch = ('checker','checker'),
    if Library.objects.using(bdd).all().exclude(name ='checker').exclude(name =libname):
        for l in Library.objects.using(bdd).all().exclude(name ='checker').exclude(name =libname).order_by('name'):
            libch += (l.name, l.name),

    class XlibForm(forms.Form):
        name = forms.ChoiceField(required = True, widget=forms.Select, choices=libch[1:], label =_("Autre bibliothèque impliquée"))

    form = XlibForm(request.POST or None)
    if form.is_valid():
        xlib = form.cleaned_data['name']
        xlid = Library.objects.using(bdd).get(name =xlib).lid
        return xarbitration(request, bdd, lid, xlid, 'title')

    return render(request, 'epl/filter_arblist.html', locals())

@edmode2
def xarbitration(request, bdd, lid, xlid, sort):

    k =logstatus(request)
    version =epl_version

    #For the lid identified library, getting ressources whose at \
    #least 2 libraries, including the considered one, took rank =1 \
    #(even if other libraries have not yet taken rank)
    #or all libraries have taken rank, none of them the rank 1

    #Initialization of the ressources to arbitrate :
    resslista = []
    resslistb = []

    for e in ItemRecord.objects.using(bdd).filter(lid =lid, rank = 1, status =0):
        sid = e.sid
        if ItemRecord.objects.using(bdd).filter(sid =sid, lid = xlid, rank = 1):
            resslista.append(e)

    for e in ItemRecord.objects.using(bdd).filter(lid =lid, status =0).exclude(rank =1).exclude(rank =0).exclude(rank =99):
        sid = e.sid
        if ItemRecord.objects.using(bdd).filter(sid =sid, lid =xlid) and \
        ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid) and \
        len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) ==0 and \
        len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =99)) ==0 and \
        len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) >1:
            resslistb.append(e)

    l = resslista + resslistb

    if sort =='sid':
        resslist = sorted(l, key=serial_id)
    elif sort =='cn':
        resslist = sorted(l, key=coll_cn)
    else:
        resslist = sorted(l, key=serial_title)

    size = len(resslist)
    
    sidlist = [ir.sid for ir in l]

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name
    xlibname = Library.objects.using(bdd).get(lid =xlid).name
    xnewestfeat(request, bdd, libname, "21", xlid)

    try:
        lastrked =ItemRecord.objects.using(bdd).get(lid =lid, last =1)
        if len(Instruction.objects.using(bdd).filter(sid =lastrked.sid)):
            lastrked =None
    except:
        lastrked =None

    return render(request, 'epl/xarbitration.html', { 'resslist' : resslist, 'sidlist' : sidlist, \
    'lid' : lid, 'libname' : libname, 'size' : size, 'k' : k, 'xlibname' : xlibname, \
    'xlid' : xlid, 'lastrked' : lastrked, 'version' : version, 'sort' : sort, 'webmaster' : webmaster, 'bdd' : bdd, })

@edmode2
def x1arb(request, bdd, lid, xlid, sort):

    k =logstatus(request)
    version =epl_version

    #For the lid identified library, getting ressources whose at \
    #least 2 libraries, including the considered one, took rank =1 \
    #(even if other libraries have not yet taken rank)
    #or all libraries have taken rank, none of them the rank 1

    #Initialization of the ressources to arbitrate :
    resslist = []

    reclist = list(ItemRecord.objects.using(bdd).filter(lid =lid, rank = 1, status =0).order_by(sort))

    for e in reclist:
        sid = e.sid
        if ItemRecord.objects.using(bdd).filter(sid =sid, lid = xlid, rank = 1):
            resslist.append(e)

    size = len(resslist)
    
    sidlist = [ir.sid for ir in resslist]

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name
    xlibname = Library.objects.using(bdd).get(lid =xlid).name
    xnewestfeat(request, bdd, libname, "22", xlid)

    try:
        lastrked =ItemRecord.objects.using(bdd).get(lid =lid, last =1)
        if len(Instruction.objects.using(bdd).filter(sid =lastrked.sid)):
            lastrked =None
    except:
        lastrked =None

    return render(request, 'epl/x1arbitration.html', { 'resslist' : resslist, 'sidlist' : sidlist, \
    'lid' : lid, 'libname' : libname, 'size' : size, 'k' : k, 'xlibname' : xlibname, \
    'lastrked' : lastrked, 'version' : version, 'sort' : sort, 'xlid' : xlid, 'webmaster' : webmaster, 'bdd' : bdd, })

@edmode2
def x0arb(request, bdd, lid, xlid, sort):

    k =logstatus(request)
    version =epl_version

    #For the lid identified library, getting ressources whose at \
    #least 2 libraries, including the considered one, took rank =1 \
    #(even if other libraries have not yet taken rank)
    #or all libraries have taken rank, none of them the rank 1

    #Initialization of the ressources to arbitrate :
    resslist = []

    reclist = list(ItemRecord.objects.using(bdd).filter(lid =lid, status =0).exclude(rank =1).exclude(rank =0).exclude(rank =99).order_by(sort))

    for e in reclist:
        sid = e.sid
        if ItemRecord.objects.using(bdd).filter(sid =sid, lid =xlid) and \
        ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid) and \
        len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) ==0 and \
        len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =99)) ==0 and \
        len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) >1:
            resslist.append(e)

    size = len(resslist)
    
    sidlist = [ir.sid for ir in resslist]

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name
    xlibname = Library.objects.using(bdd).get(lid =xlid).name
    xnewestfeat(request, bdd, libname, "23", xlid)

    try:
        lastrked =ItemRecord.objects.using(bdd).get(lid =lid, last =1)
        if len(Instruction.objects.using(bdd).filter(sid =lastrked.sid)):
            lastrked =None
    except:
        lastrked =None

    return render(request, 'epl/x0arbitration.html', { 'resslist' : resslist, 'sidlist' : sidlist, \
    'lid' : lid, 'libname' : libname, 'size' : size, 'k' : k, 'xlibname' : xlibname, \
    'lastrked' : lastrked, 'version' : version, 'sort' : sort, 'xlid' : xlid, 'webmaster' : webmaster, 'bdd' : bdd, })

@edmode1
def instrtodo(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    if lid !="999999999":
        l = list(ItemRecord.objects.using(bdd).filter(lid =lid).exclude(status =0).exclude(status =2).\
        exclude(status =4).exclude(status =5).exclude(status =6).order_by(sort))

    elif lid =="999999999":

        l = []

        for e in ItemRecord.objects.using(bdd).filter(status =2, rank =1):
            if len(ItemRecord.objects.using(bdd).filter(sid =e.sid, status =2)) == len(ItemRecord.objects.using(bdd).filter(sid =e.sid).exclude(rank =0)) and len(Instruction.objects.using(bdd).filter(sid =e.sid, name= "checker")) ==0:
                l.append(ItemRecord.objects.using(bdd).get(sid =e.sid, rank =1)) #yehh ... rank =1 that's the trick !

        for e in ItemRecord.objects.using(bdd).filter(status =4, rank =1):
            if len(ItemRecord.objects.using(bdd).filter(sid =e.sid, status =4)) == len(ItemRecord.objects.using(bdd).filter(sid =e.sid).exclude(rank =0)) and len(Instruction.objects.using(bdd).filter(sid =e.sid, name= "checker")) ==1:
                l.append(ItemRecord.objects.using(bdd).get(sid =e.sid, rank =1)) #yehh ... rank =1 that's the trick !

    if sort =='sid':
        l = sorted(l, key=serial_id)
    elif sort =='cn':
        l = sorted(l, key=coll_cn)
    else:
        l = sorted(l, key=serial_title)

    size = len(l)
    
    sidlist = [ir.sid for ir in l]

    #Getting library name :
    libname = Library.objects.using(bdd).get(lid =lid).name
    newestfeat(request, bdd, libname, "30")

    nlib = len(Library.objects.using(bdd).exclude(lid ="999999999"))

    lidchecker = "999999999"

    return render(request, 'epl/instrtodo.html', locals())

@edmode1
def instroneb(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    if lid !="999999999":
        l = list(ItemRecord.objects.using(bdd).filter(lid =lid, rank =1).exclude(status =0).exclude(status =2).exclude(status =3)\
        .exclude(status =4).exclude(status =5).exclude(status =6).order_by(sort))
        # Ressources whose the lid identified library has rank =1 and has to deal with bound elements (status =1)

    elif lid =="999999999":
        do = home(request, bdd)
        return do

    size = len(l)
    
    sidlist = [ir.sid for ir in l]

    #Getting library name :
    libname = Library.objects.using(bdd).get(lid =lid).name
    newestfeat(request, bdd, libname, "35")

    return render(request, 'epl/instrtodobd1.html', locals())

@edmode1
def instrotherb(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    if lid !="999999999":
        l = list(ItemRecord.objects.using(bdd).filter(lid =lid).exclude(rank =1).\
        exclude(status =0).exclude(status =2).exclude(status =3).exclude(status =4)\
        .exclude(status =5).exclude(status =6).order_by(sort))
        # Ressources whose the lid identified library has rank !=1 and has to deal with bound elements (status =1)

    elif lid =="999999999":
        do = home(request, bdd)
        return do

    size = len(l)
    
    sidlist = [ir.sid for ir in l]

    #Getting library name :
    libname = Library.objects.using(bdd).get(lid =lid).name
    newestfeat(request, bdd, libname, "36")

    return render(request, 'epl/instrtodobdnot1.html', locals())

@edmode1
def instronenotb(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    if lid !="999999999":
        l = list(ItemRecord.objects.using(bdd).filter(lid =lid, rank =1).exclude(status =0).\
        exclude(status =1).exclude(status =2).exclude(status =4).exclude(status =5).exclude(status =6).order_by(sort))
        # Ressources whose the lid identified library has rank =1 and has to deal with not bound elements (status =3)

    elif lid =="999999999":
        do = home(request, bdd)
        return do

    size = len(l)
    
    sidlist = [ir.sid for ir in l]

    #Getting library name :
    libname = Library.objects.using(bdd).get(lid =lid).name
    newestfeat(request, bdd, libname, "37")

    return render(request, 'epl/instrtodonotbd1.html', locals())

@edmode1
def instrothernotb(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    if lid !="999999999":
        l = list(ItemRecord.objects.using(bdd).filter(lid =lid).exclude(rank =1).exclude(status =0).\
        exclude(status =1).exclude(status =2).exclude(status =4).exclude(status =5).exclude(status =6).order_by(sort))
        # Ressources whose the lid identified library has rank !=1 and has to deal with not bound elements (status =3)

    elif lid =="999999999":
        do = home(request, bdd)
        return do

    size = len(l)
    
    sidlist = [ir.sid for ir in l]

    #Getting library name :
    libname = Library.objects.using(bdd).get(lid =lid).name
    newestfeat(request, bdd, libname, "38")

    return render(request, 'epl/instrtodonotbdnot1.html', locals())

@edmode4
def instrfilter(request, bdd, lid):

    k =logstatus(request)
    version =epl_version

    "Filter instruction list"

    libname = (Library.objects.using(bdd).get(lid =lid)).name

    libch = ('checker','checker'),
    if Library.objects.using(bdd).all().exclude(name ='checker').exclude(name =libname):
        for l in Library.objects.using(bdd).all().exclude(name ='checker').exclude(name =libname).order_by('name'):
            libch += (l.name, l.name),

    class XlibForm(forms.Form):
        name = forms.ChoiceField(required = True, widget=forms.Select, choices=libch[1:], label =_("Autre bibliothèque impliquée"))

    form = XlibForm(request.POST or None)
    if form.is_valid():
        xlib = form.cleaned_data['name']
        xlid = Library.objects.using(bdd).get(name =xlib).lid
        return xinstrlist(request, bdd, lid, xlid, 'title')
    return render(request, 'epl/filter_instrlist.html', locals())

@edmode2
def xinstrlist(request, bdd, lid, xlid, sort):

    k =logstatus(request)
    version =epl_version

    if lid =="999999999":
        return notintime(request, bdd, "-?-", lid)

    name = Library.objects.using(bdd).get(lid =lid).name
    xname = Library.objects.using(bdd).get(lid =xlid).name
    xnewestfeat(request, bdd, name, "31", xlid)

    lprov = list(ItemRecord.objects.using(bdd).filter(lid =lid).exclude(status =0).exclude(status =2).\
    exclude(status =4).exclude(status =5).exclude(status =6).order_by(sort))

    l =[]
    for e in lprov:
        if ItemRecord.objects.using(bdd).filter(lid =xlid, sid =e.sid).exclude(rank =0):
            l.append(e)

    size = len(l)
    
    sidlist = [ir.sid for ir in l]

    return render(request, 'epl/xto_instr_list.html', locals())

@edmode1
def tobeedited(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    #For the lid identified library, getting ressources whose the resulting \
    #collection has been entirely completed and may consequently be edited.
    #Trick : These ressources have two instructions with name = 'checker' :

    l = list(ItemRecord.objects.using(bdd).filter(lid =lid).exclude(rank =0).order_by(sort))

    #Initializing a list of ressources to edit :
    resslist = []

    for e in l:
        nl = Instruction.objects.using(bdd).filter(sid =e.sid)
        kd = nl.filter(name = "checker")
        if len(kd) ==2:
            resslist.append(e)

    size = len(resslist)
    
    sidlist = [ir.sid for ir in resslist]

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name
    newestfeat(request, bdd, libname, "40")

    return render(request, 'epl/to_edit_list.html', locals())

@edmode1
def mothered(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    #For the lid identified library, getting ressources whose the resulting \
    #collection has been entirely completed and may consequently be edited.
    #Trick : These ressources have two instructions with name = 'checker' :

    l = list(ItemRecord.objects.using(bdd).filter(lid =lid, rank =1).order_by(sort))

    #Initializing a list of ressources to edit :
    resslist = []

    for e in l:
        nl = Instruction.objects.using(bdd).filter(sid =e.sid)
        kd = nl.filter(name = "checker")
        if len(kd) ==2:
            resslist.append(e)

    size = len(resslist)
    
    sidlist = [ir.sid for ir in resslist]

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name
    newestfeat(request, bdd, libname, "41")

    return render(request, 'epl/to_edit_list_mother.html', locals())

@edmode1
def notmothered(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    #For the lid identified library, getting ressources whose the resulting \
    #collection has been entirely completed and may consequently be edited.
    #Trick : These ressources have two instructions with name = 'checker' :

    l = list(ItemRecord.objects.using(bdd).filter(lid =lid).exclude(rank =1).exclude(rank =0).exclude(rank =99).order_by(sort))

    #Initializing a list of ressources to edit :
    resslist = []

    for e in l:
        nl = Instruction.objects.using(bdd).filter(sid =e.sid)
        kd = nl.filter(name = "checker")
        if len(kd) ==2:
            resslist.append(e)

    size = len(resslist)
    
    sidlist = [ir.sid for ir in resslist]

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name
    newestfeat(request, bdd, libname, "42")

    return render(request, 'epl/to_edit_list_notmother.html', locals())

@edmode4
def filter_edlist(request, bdd, lid):

    k =logstatus(request)
    version =epl_version

    "Filter"

    name = (Library.objects.using(bdd).get(lid =lid)).name

    libch = ('checker','checker'),
    if Library.objects.using(bdd).all().exclude(name ='checker').exclude(name =name):
        for l in Library.objects.using(bdd).all().exclude(name ='checker').exclude(name =name).order_by('name'):
            libch += (l.name, l.name),

    class EditionForm(forms.Form):
        rk_ch = (("a", _("Collection mère")), ("b", _("Collection non mère")),)
        rank = forms.ChoiceField(required = True, widget=forms.Select, choices=rk_ch, label =_("Rang des collections de la bibliothèque mentionnée dans l'entête de cette page"))
        lib = forms.ChoiceField(required = True, widget=forms.Select, choices=libch[1:], label =_("Autre bibliothèque impliquée"))

    form = EditionForm(request.POST or None)
    if form.is_valid():
        rank = form.cleaned_data['rank']
        xlib = form.cleaned_data['lib']
        xlid = Library.objects.using(bdd).get(name =xlib).lid
        if lid == xlid:
            if rank =="a":
                return mothered(request, bdd, lid, 'title')
            else:
                return notmothered(request, bdd, lid, 'title')
        else: # lid != xlid
            if rank =="a":
                return xmothered(request, bdd, lid, xlid, 'title')
            else:
                return xnotmothered(request, bdd, lid, xlid, 'title')

    return render(request, 'epl/filter_edlist.html', locals())

@edmode2
def xmothered(request, bdd, lid, xlid, sort):

    k =logstatus(request)
    version =epl_version

    l = list(ItemRecord.objects.using(bdd).filter(lid =lid, rank =1).order_by(sort))

    #Initializing a list of ressources to edit :
    resslist = []

    for e in l:
        nl = Instruction.objects.using(bdd).filter(sid =e.sid)
        kd = nl.filter(name = "checker")
        if len(kd) ==2 and Instruction.objects.using(bdd).filter(sid =e.sid, name =Library.objects.using(bdd).get(lid =xlid)):
            resslist.append(e)

    size = len(resslist)
    
    sidlist = [ir.sid for ir in resslist]

    name = Library.objects.using(bdd).get(lid =lid).name
    xname = Library.objects.using(bdd).get(lid =xlid).name
    xnewestfeat(request, bdd, name, "43", xlid)

    return render(request, 'epl/xto_edit_list_mother.html', locals())

@edmode2
def xnotmothered(request, bdd, lid, xlid, sort):

    k =logstatus(request)
    version =epl_version

    l = list(ItemRecord.objects.using(bdd).filter(lid =lid).exclude(rank =1).exclude(rank =0).exclude(rank =99).order_by(sort))

    #Initializing a list of ressources to edit :
    resslist = []

    for e in l:
        nl = Instruction.objects.using(bdd).filter(sid =e.sid)
        kd = nl.filter(name = "checker")
        if len(kd) ==2 and Instruction.objects.using(bdd).filter(sid =e.sid, name =Library.objects.using(bdd).get(lid =xlid)):
            resslist.append(e)

    size = len(resslist)
    
    sidlist = [ir.sid for ir in resslist]

    name = Library.objects.using(bdd).get(lid =lid).name
    xname = Library.objects.using(bdd).get(lid =xlid).name
    xnewestfeat(request, bdd, name, "44", xlid)

    return render(request, 'epl/xto_edit_list_notmother.html', locals())

@edmode5
def edition(request, bdd, sid, lid):

    k =logstatus(request)
    version =epl_version

    #edition of the resulting collection for the considered sid and lid :

    #Control (edition only if yet possible)
    if len(Instruction.objects.using(bdd).filter(sid =sid, name ="checker")) ==2:
        #Getting an item record from which we can obtain ressource data :
        issn = ItemRecord.objects.using(bdd).get(sid =sid, lid =lid, status =5).issn
        title = ItemRecord.objects.using(bdd).get(sid =sid, lid =lid, status =5).title
        pubhist = ItemRecord.objects.using(bdd).get(sid =sid, lid =lid, status =5).pubhist


        #Getting instructions for the considered ressource :
        instrlist = Instruction.objects.using(bdd).filter(sid =sid).order_by('line')
        l = list(instrlist)

        #Getting library name for the considered library (will be used to
        #highlight the instruction of the considered library) :
        name = (Library.objects.using(bdd).get(lid =lid)).name

        mothercollection = Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =sid, rank =1).lid).name

        try:
            itrec =ItemRecord.objects.using(bdd).get(sid =sid, lid =lid)
        except:
            itrec =""

        # Contributing collections (lib) ordered by 'rank'
        coliblist = []
        coitemlist =ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0).order_by("rank", "pk")
        for co in coitemlist:
            coliblist.append(Library.objects.using(bdd).get(lid = co.lid))

        # Not Contributing collections (lib) ordered by 'rank'
        exlist = []
        for elmt in ItemRecord.objects.using(bdd).filter(sid =sid, rank =0):
            exlist.append(((Library.objects.using(bdd).get(lid = elmt.lid)).name, elmt.excl, elmt.comm))

        return render(request, 'epl/edition.html', locals())

    else:
        return notintime(request, bdd, sid, lid)

@edmode5
def current_status(request, bdd, sid, lid):
# Lot of code for this view is similar with the code for "search" view : When changing here, think to change there

    k =logstatus(request)
    version =epl_version

    l =1
    lib = Library.objects.using(bdd).get(lid =lid).name
    n = len(ItemRecord.objects.using(bdd).filter(sid =sid))
    ranklist =[] # if n==0
    progress =0
    action, laction =0,0
    alteraction, lalteraction =0,0

    tem =1
    # Bibliographic data :
    title = ItemRecord.objects.using(bdd).filter(sid =sid)[0].title
    issn = ItemRecord.objects.using(bdd).filter(sid =sid)[0].issn
    pubhist = ItemRecord.objects.using(bdd).filter(sid =sid)[0].pubhist

    # ItemRecord data :
    try:
        holdstat = ItemRecord.objects.using(bdd).get(sid =sid, lid = lid).holdstat
        missing = ItemRecord.objects.using(bdd).get(sid =sid, lid = lid).missing
        cn = ItemRecord.objects.using(bdd).get(sid =sid, lid = lid).cn
    except:
        tem =0

    #Calcul de l'avancement:
    higher_status =ItemRecord.objects.using(bdd).filter(sid =sid).order_by("-status")[0].status
    if higher_status ==6:
        if len(Instruction.objects.using(bdd).filter(sid =sid, name ="checker")):
            progress =_("Anomalie signalée lors de la phase des non reliés")
        else:
            progress =_("Anomalie signalée lors de la phase des reliés")
    elif higher_status ==5:
        progress =_("Instruction achevée")
        if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid).exclude(rank =0):
            action, laction =_("Edition de la fiche de résultante"), bdd + "/ed/" + str(sid) + "/" + str(lid)
    elif higher_status ==4:
        if len(ItemRecord.objects.using(bdd).filter(sid =sid, status =4)) ==len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)):
            progress =_("En attente de validation finale par le contrôleur")
            if lid =="999999999":
                action, laction =_("Validation finale"), bdd + "/end/" + str(sid) + "/" + str(lid)
        else:
            if lid !="999999999":
                if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid, status =3):
                    if Instruction.objects.using(bdd).filter(sid =sid, bound =" ", name =Library.objects.using(bdd).get(lid =lid).name):
                        progress =_("Instruction des non reliés en cours pour votre collection")
                    else:
                        progress =_("Instruction des non reliés à débuter pour votre collection")
                    action, laction =_("Instruction"), bdd + "/add/" + str(sid) + "/" + str(lid)
                else:
                    xname =Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =sid, status =3).lid).name
                    if Instruction.objects.using(bdd).filter(sid =sid, bound =" ", name =xname):
                        progress =_("Instruction des non reliés en cours pour : ")
                    else:
                        progress =_("Instruction des non reliés en cours ; à débuter pour : ")
            else:#lid ="999999999"
                xname =Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =sid, status =3).lid).name
                if Instruction.objects.using(bdd).filter(sid =sid, bound =" ", name =xname):
                    progress =_("Instruction des non reliés en cours pour : ")
                else:
                    progress =_("Instruction des non reliés en cours ; à débuter pour : ")
    elif higher_status ==3:
        if lid !="999999999":
            if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid, status =3):
                if Instruction.objects.using(bdd).filter(sid =sid, bound =" ", name =Library.objects.using(bdd).get(lid =lid).name):
                    progress =_("Instruction des non reliés en cours pour votre collection")
                else:
                    progress =_("Instruction des non reliés à débuter pour votre collection")
                action, laction =_("Instruction"), bdd + "/add/" + str(sid) + "/" + str(lid)
            else:
                xname =Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =sid, status =3).lid).name
                if Instruction.objects.using(bdd).filter(sid =sid, bound =" ", name =xname):
                    progress =_("Instruction des non reliés en cours pour : ")
                else:
                    progress =_("Instruction des non reliés en cours ; à débuter pour : ")
        else:#lid ="999999999"
            xname =Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =sid, status =3).lid).name
            if Instruction.objects.using(bdd).filter(sid =sid, bound =" ", name =xname):
                progress =_("Instruction des non reliés en cours pour : ")
            else:
                progress =_("Instruction des non reliés en cours ; à débuter pour : ")
    elif higher_status ==2:
        if len(ItemRecord.objects.using(bdd).filter(sid =sid, status =2)) ==len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)):
            progress =_("En attente de validation intermédiaire par le contrôleur")
            if lid =="999999999":
                action, laction =_("Validation intermédiaire"), bdd + "/end/" + str(sid) + "/" + str(lid)
        else:
            if lid !="999999999":
                if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid, status =1):
                    if Instruction.objects.using(bdd).filter(sid =sid, bound ="x", name =Library.objects.using(bdd).get(lid =lid).name):
                        progress =_("Instruction des reliés en cours pour votre collection")
                    else:
                        progress =_("Instruction des reliés à débuter pour votre collection")
                    action, laction =_("Instruction"), bdd + "/add/" + str(sid) + "/" + str(lid)
                else:
                    xname =Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =sid, status =1).lid).name
                    if Instruction.objects.using(bdd).filter(sid =sid, bound ="x", name =xname):
                        progress =_("Instruction des reliés en cours pour : ")
                    else:
                        progress =_("Instruction des reliés en cours ; à débuter pour : ")
            else:#lid ="999999999"
                xname =Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =sid, status =1).lid).name
                if Instruction.objects.using(bdd).filter(sid =sid, bound ="x", name =xname):
                    progress =_("Instruction des reliés en cours pour : ")
                else:
                    progress =_("Instruction des reliés en cours ; à débuter pour : ")
    elif higher_status ==1:
        if lid !="999999999":
            if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid, status =1):
                if Instruction.objects.using(bdd).filter(sid =sid, bound ="x", name =Library.objects.using(bdd).get(lid =lid).name):
                    progress =_("Instruction des reliés en cours pour votre collection")
                else:
                    progress =_("Instruction des reliés à débuter pour votre collection")
                action, laction =_("Instruction"), bdd + "/add/" + str(sid) + "/" + str(lid)
            else:
                xname =Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =sid, status =1).lid).name
                if Instruction.objects.using(bdd).filter(sid =sid, bound ="x", name =xname):
                    progress =_("Instruction des reliés en cours pour : ")
                else:
                    progress =_("Instruction des reliés en cours ; à débuter pour : ")
            if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid) and len(Instruction.objects.using(bdd).filter(sid =sid)) ==0:
                alteraction, lalteraction =_("Modification éventuelle du rang de votre collection"), bdd + "/rk/" + str(sid) + "/" + str(lid)
        else:#lid ="999999999"
            xname =Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =sid, status =1).lid).name
            if Instruction.objects.using(bdd).filter(sid =sid, bound ="x", name =xname):
                progress =_("Instruction des reliés en cours pour : ")
            else:
                progress =_("Instruction des reliés en cours ; à débuter pour : ")
    else: # higher_status ==0
        if lid !="999999999":
            if len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) <2:
                progress =_("La ressource n'est plus candidate au dédoublonnement")
                if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid, rank =0):
                     action, laction =_("Repositionnement éventuel de votre collection"), bdd + "/rk/" + str(sid) + "/" + str(lid)
            elif ItemRecord.objects.using(bdd).filter(sid =sid, rank =99) and len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) >1:
                if ItemRecord.objects.using(bdd).filter(sid =sid, rank =99, lid =lid):
                    progress =_("Positionnement à compléter pour votre collection")
                    action, laction =_("Positionnement de votre collection"), bdd + "/rk/" + str(sid) + "/" + str(lid)
                else:
                    progress =_("Positionnement à compléter pour une ou plusieurs collections")
                    if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid):
                        alteraction, lalteraction =_("Modification éventuelle du rang de votre collection"), bdd + "/rk/" + str(sid) + "/" + str(lid)
            elif len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) >1:
                if ItemRecord.objects.using(bdd).filter(sid =sid, rank =1, lid =lid):
                    progress =_("Rang 1 revendiqué pour plusieurs collections dont la vôtre")
                    action, laction =_("Repositionnement éventuel de votre collection"), bdd + "/rk/" + str(sid) + "/" + str(lid)
                else:
                    progress =_("Rang 1 revendiqué pour plusieurs collections mais pas la vôtre")
                    if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid):
                        alteraction, lalteraction =_("Modification éventuelle du rang de votre collection"), bdd + "/rk/" + str(sid) + "/" + str(lid)
            else:# len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) ==0:
                progress =_("Le rang 1 n'a été revendiqué pour aucune collection")
                if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid):
                    action, laction =_("Repositionnement éventuel de votre collection"), bdd + "/rk/" + str(sid) + "/" + str(lid)
        else: #lid ="999999999"
            if len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) <2:
                progress =_("La ressource n'est plus candidate au dédoublonnement")
            elif ItemRecord.objects.using(bdd).filter(sid =sid, rank =99) and len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) >1:
                progress =_("Positionnement à compléter pour une ou plusieurs collections")
            elif len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) >1:
                progress =_("Rang 1 revendiqué pour plusieurs collections")
            else:# len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) ==0:
                progress =_("Le rang 1 n'a été revendiqué pour aucune collection")

    #Getting instructions for the considered ressource :
    instrlist = Instruction.objects.using(bdd).filter(sid = sid).order_by('line')
    size =len(instrlist)

    try:
        pklastone = Instruction.objects.using(bdd).filter(sid = sid).latest('time').pk
    except:
        pklastone =0

    #Attachements :
    attchmt =ItemRecord.objects.using(bdd).filter(sid =sid).order_by("rank")
    attlist = [(Library.objects.using(bdd).get(lid =element.lid).name, element) for element in attchmt]

    rklist = ItemRecord.objects.using(bdd).filter(sid =sid).order_by('rank', 'lid')
    ranklist = [(element, Library.objects.using(bdd).get(lid =element.lid).name) for element in rklist]

    return render(request, 'epl/current.html', locals())


@login_required
def statadmin(request, bdd, sid):

    #contrôle ici
    suffixe = "@" + str(bdd)
    if not request.user.username[-3:] ==suffixe:
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)
    if not len(BddAdmin.objects.using(bdd).filter(contact =request.user.email)):
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)

    k =logstatus(request)
    version =epl_version
    
    itemrec =ItemRecord.objects.using(bdd).get(sid =sid, rank =1)
    
    #Ressource data :
    itemlist = ItemRecord.objects.using(bdd).filter(sid = sid).exclude(rank =0).order_by("rank", 'pk')
    # Library list ordered as in instruction order
    liblist = []
    for e in itemlist:
        liblist.append(Library.objects.using(bdd).get(lid = e.lid))
    liblist.append(Library.objects.using(bdd).get(name = 'checker'))    
    LIBRARYTEMP_CHOICES = ('temp', 'temp'),
    for liblmt in liblist:
        LIBRARYTEMP_CHOICES += (liblmt.name, liblmt.name),
    LIBRARY_CHOICES = LIBRARYTEMP_CHOICES[1:]
    
    class LibTurnForm(forms.Form):
        name = forms.ChoiceField(required = True, widget=forms.Select, choices=LIBRARY_CHOICES, label =_(""))

    form = LibTurnForm(request.POST or None)
    if request.method =="POST" and form.is_valid():
        name = form.cleaned_data['name']
        #Controls first !
        if len(Instruction.objects.using(bdd).filter(sid =sid, name ="checker")) ==1:
            m =0
            for lib in liblist:
                if lib.name ==name:#status 3
                    m =1
                    if len(Instruction.objects.using(bdd).filter(sid =sid, name =lib.name, bound ="x")) ==0:
                            messages.info(request, _("échec : vérifiez qu'il y a au moins une instruction avec des éléments reliés pour : {}".format(lib.name)))
                            return current_status(request, bdd, sid, "999999999")
                else:
                    if m ==0:#status 4
                        if len(Instruction.objects.using(bdd).filter(sid =sid, name =lib.name).exclude(bound ="x")) ==0:
                            messages.info(request, _("échec : vérifiez qu'il y a au moins une instruction avec des éléments non reliés pour : {}".format(lib.name)))
                            return current_status(request, bdd, sid, "999999999")
                        elif len(Instruction.objects.using(bdd).filter(sid =sid, name =lib.name, bound ="x")) ==0:
                            messages.info(request, _("échec : vérifiez qu'il y a au moins une instruction avec des éléments reliés pour : {}".format(lib.name)))
                            return current_status(request, bdd, sid, "999999999")
                    else:#status 2
                        if len(Instruction.objects.using(bdd).filter(sid =sid, name =lib.name, bound ="x")) ==0:
                            messages.info(request, _("échec : vérifiez qu'il y a au moins une instruction avec des éléments reliés pour : {}".format(lib.name)))
                            return current_status(request, bdd, sid, "999999999")
                        if len(Instruction.objects.using(bdd).filter(sid =sid, name =lib.name).exclude(bound ="x")):
                            messages.info(request, _("échec : vérifiez qu'il n'y a aucune instruction avec des éléments non reliés pour : {}".format(lib.name)))
                            return current_status(request, bdd, sid, "999999999")
        if len(Instruction.objects.using(bdd).filter(sid =sid, name ="checker")) ==0:
            if len(Instruction.objects.using(bdd).filter(sid =sid).exclude(bound ="x")):
                messages.info(request, _("échec : vérifiez qu'il n'y a aucune instruction avec des éléments non reliés"))
            else:
                m =0
                for lib in liblist:
                    if lib.name ==name:#status 1
                        m =1
                        if len(Instruction.objects.using(bdd).filter(sid =sid, name =lib.name).exclude(bound ="x")):
                            messages.info(request, _("échec : vérifiez qu'il n'y a aucune instruction avec des éléments non reliés pour : {}".format(lib.name)))
                            return current_status(request, bdd, sid, "999999999")
                    else:
                        if m ==0:#status 2
                            if len(Instruction.objects.using(bdd).filter(sid =sid, name =lib.name, bound ="x")) ==0:
                                messages.info(request, _("échec : vérifiez qu'il y a au moins une instruction avec des éléments reliés pour : {}".format(lib.name)))
                                return current_status(request, bdd, sid, "999999999")
                            if len(Instruction.objects.using(bdd).filter(sid =sid, name =lib.name).exclude(bound ="x")):
                                messages.info(request, _("échec : vérifiez qu'il n'y a aucune instruction avec des éléments non reliés pour : {}".format(lib.name)))
                                return current_status(request, bdd, sid, "999999999")
                        else:#status 0
                            if len(Instruction.objects.using(bdd).filter(sid =sid, name =lib.name, bound ="x")):
                                messages.info(request, _("échec : vérifiez qu'il n'y a aucune instruction avec des éléments reliés pour : {}".format(lib.name)))
                                return current_status(request, bdd, sid, "999999999")
                            if len(Instruction.objects.using(bdd).filter(sid =sid, name =lib.name).exclude(bound ="x")):
                                messages.info(request, _("échec : vérifiez qu'il n'y a aucune instruction avec des éléments non reliés pour : {}".format(lib.name)))
                                return current_status(request, bdd, sid, "999999999")
        #Then status modification if all controls are ok :                    
        if len(Instruction.objects.using(bdd).filter(sid =sid, name ="checker")) ==1:
            m =0
            for lib in liblist:
                if lib.name ==name:
                    m =1
                    try:
                        it = ItemRecord.objects.using(bdd).get(sid =sid, lid =Library.objects.using(bdd).get(name =lib.name).lid)
                        it.status =3
                        it.save(using=bdd)
                    except:#(checker)
                        pass
                else:
                    if m ==0:
                        try:
                            it = ItemRecord.objects.using(bdd).get(sid =sid, lid =Library.objects.using(bdd).get(name =lib.name).lid)
                            it.status =4
                            it.save(using=bdd)
                        except:#(checker)
                            pass
                    else:
                        try:
                            it = ItemRecord.objects.using(bdd).get(sid =sid, lid =Library.objects.using(bdd).get(name =lib.name).lid)
                            it.status =2
                            it.save(using=bdd)
                        except:#(checker)
                            pass
        if len(Instruction.objects.using(bdd).filter(sid =sid, name ="checker")) ==0:
            if len(Instruction.objects.using(bdd).filter(sid =sid).exclude(bound ="x")):
                messages.info(request, _("échec : vérifiez qu'il n'y a aucune instruction avec des éléments non reliés"))
            else:
                m =0
                for lib in liblist:
                    if lib.name ==name:
                        m =1
                        try:
                            it = ItemRecord.objects.using(bdd).get(sid =sid, lid =Library.objects.using(bdd).get(name =lib.name).lid)
                            it.status =1
                            it.save(using=bdd)
                        except:#(checker)
                            pass
                    else:
                        if m ==0:
                            try:
                                it = ItemRecord.objects.using(bdd).get(sid =sid, lid =Library.objects.using(bdd).get(name =lib.name).lid)
                                it.status =2
                                it.save(using=bdd)
                            except:#(checker)
                                pass
                        else:
                            try:
                                it = ItemRecord.objects.using(bdd).get(sid =sid, lid =Library.objects.using(bdd).get(name =lib.name).lid)
                                it.status =0
                                it.save(using=bdd)
                            except:#(checker)
                                pass
        
        messages.info(request, _("(Les statuts ont été calculés automatiqument)"))
        messages.info(request, _("Un message a été envoyé aux instructeurs de - {} - pour les informer que leur tour est venu d'instruire cette fiche".format(name)))
        if Proj_setting.objects.using(bdd).all()[0].ins:
            nextlib =Library.objects.using(bdd).get(name =name)
            nextlid = nextlib.lid
            message_end = _("(Ce message fait suite à une correction apportée par l'administrateur de la base de données)") + "\n" + _("(Il est possible qu'il vous ait attribué le tour pour simple vérification ; dans ce cas, vous n'aurez plus qu'à indiquer que vous avez fini pour la phase courante)")
            if nextlid =="999999999":
                message_end = _("(Ce message fait suite à une correction apportée par l'administrateur de la base de données)")            
            subject = "eplouribousse / instruction : " + bdd + " / " + str(sid) + " / " + str(nextlid)
            host = str(request.get_host())
            message = _("Votre tour est venu d'instruire la fiche eplouribousse pour le ppn ") + str(sid) + \
            " :\n" + "http://" + host + "/" + bdd + "/add/" + str(sid) + '/' + str(nextlid) + \
            "\n" + message_end
            dest =[]
            if Utilisateur.objects.using(bdd).get(mail =nextlib.contact).ins:
                dest.append(nextlib.contact)
            try:
                if Utilisateur.objects.using(bdd).get(mail =nextlib.contact_bis).ins:
                    dest.append(nextlib.contact_bis)
            except:
                st =1 #bidon pour passer
            try:
                if Utilisateur.objects.using(bdd).get(mail =nextlib.contact_ter).ins:
                    dest.append(nextlib.contact_ter)
            except:
                st =1 #bidon pour passer
            if len(dest):
                send_mail(subject, message, replymail, dest, fail_silently=True, )

        return current_status(request, bdd, sid, "999999999")

    return render(request, 'epl/statadmin.html', locals())


@login_required
def instradmin(request, bdd, id):

    #contrôle ici
    suffixe = "@" + str(bdd)
    if not request.user.username[-3:] ==suffixe:
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)
    if not len(BddAdmin.objects.using(bdd).filter(contact =request.user.email)):
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return home(request, bdd)

    k =logstatus(request)
    version =epl_version
    instrid =int(id)
    instru =Instruction.objects.using(bdd).get(id =instrid)
    sid =instru.sid
    name =instru.name
    lid = Library.objects.using(bdd).get(name =name).lid
    
    LIBRARY_CHOICES = ('checker', 'checker'),
    REM_CHOICES =('',''),
    for itlmt in ItemRecord.objects.using(bdd).filter(sid =sid):
        if not itlmt.excl:
            l = Library.objects.using(bdd).get(lid = itlmt.lid)
            LIBRARY_CHOICES += (l.name, l.name),
            REM_CHOICES += (l.name, l.name),

    try:
        d =ItemRecord.objects.using(bdd).filter(sid =Instruction.objects.using(bdd).get(id =instrid).sid)[0]
        bib =Library.objects.using(bdd).get(lid =d.lid)
    except:
        return HttpResponse(_("Pas d'instruction correspondante"))

    instrlist =Instruction.objects.using(bdd).filter(sid =d.sid).order_by('line')

    class InstructionForm(forms.ModelForm):
        class Meta:
            model = Instruction
            fields =('line', 'name', 'bound', 'oname', 'descr', 'exc', 'degr', 'time')
            # exclude = ('sid', 'name', 'bound',)
            widgets = {
                'name' : forms.Select(choices=LIBRARY_CHOICES, attrs={'title': _("Intitulé")}),
                'bound' : forms.Select(choices=(('',''),('x','x'),)),
                'oname' : forms.Select(choices=REM_CHOICES, attrs={'title': _("Intitulé de la bibliothèque ayant précédemment déclaré une 'exception' ou un 'améliorable'")}),
                'descr' : forms.TextInput(attrs={'placeholder': _("1990(2)-1998(12) par ex."), 'title': _("Suite ininterrompue chronologiquement ; le n° de ligne est à déterminer selon l'ordre chronologique de ce champ")}),
                'exc' : forms.TextInput(attrs={'placeholder': _("1991(5) par ex."), 'title': \
                _("éléments manquants dans le segment pour la forme considérée (pas forcément des lacunes si l'on considère la forme reliée)")}),
                'degr' : forms.TextInput(attrs={'placeholder': _("1995(4) par ex."), 'title': \
                _("éléments dégradés (un volume relié dégradé peut être remplacé par les fascicules correspondants en bon état)")}),
            }

    i =Instruction(sid =sid)
    f = InstructionForm(request.POST or None, instance =i, initial = {
    'line' : Instruction.objects.using(bdd).get(id =instrid).line -1,
    'name' : Instruction.objects.using(bdd).get(id =id).name,
    'bound' : Instruction.objects.using(bdd).get(id =instrid).bound,
    'oname' : Instruction.objects.using(bdd).get(id =instrid).oname,
    'descr' : Instruction.objects.using(bdd).get(id =instrid).descr,
    'exc' : Instruction.objects.using(bdd).get(id =instrid).exc,
    'degr' : Instruction.objects.using(bdd).get(id =instrid).degr,
    })

    class SupAjForm(forms.Form):
        suppr = forms.BooleanField(required=False)
        ajo = forms.BooleanField(required=False)

    modeform =SupAjForm(request.POST or None)

    if request.method =="POST" and f.is_valid() and modeform.is_valid():
        sup = modeform.cleaned_data['suppr']
        aj = modeform.cleaned_data['ajo']
        i.time =Now()
        if (sup, aj) ==(False, False):
            messages.info(request, _("(Aucune modification n'a été effectuée car vous n'avez rien coché)"))
            return current_status(request, bdd, d.sid, bib.lid)
        elif (sup, aj) ==(True, True):
            instru.delete(using=bdd)
            i.save(using=bdd)
        elif (sup, aj) ==(True, False):
            instru.delete(using=bdd)
        elif (sup, aj) ==(False, True):
            i.save(using=bdd)
        else:#it should never happen
            HttpResponse("Unexpected request !")

        #Renumbering instruction lines :
        try:
            instr = Instruction.objects.using(bdd).filter(sid = sid).order_by('line', 'pk')
            j, l =0, 1
            while j <= len(instr):
                instr[j].line = l
                instr[j].save(using=bdd)
                j +=1
                l +=1
        except:
            pass

        return current_status(request, bdd, d.sid, bib.lid)
        # return HttpResponseRedirect("/" + bdd + "/current_status" + "/" + str(d.sid) + "/" + str(bib.lid))

    return render(request, 'epl/instradmin.html', locals())

@edmode3
def checkinstr(request, bdd):

    k =logstatus(request)
    version =epl_version

    project = Project.objects.using(bdd).all().order_by('pk')[0].name

    return render(request, 'epl/checker.html', locals())

@edmode3
def checkerfilter(request, bdd):

    k =logstatus(request)
    version =epl_version

    LIBRARY_CHOICES = ('', ''),
    if Library.objects.using(bdd).all().exclude(name ='checker'):
        for l in Library.objects.using(bdd).all().exclude(name ='checker').order_by('name'):
            LIBRARY_CHOICES += (l.name, l.name),

    class InstructionCheckerFilter(forms.Form):
        name = forms.MultipleChoiceField(required = True, widget=forms.CheckboxSelectMultiple, choices=LIBRARY_CHOICES[1:], label =_("Bibliothèques impliquées (opérateur 'ou')"))
        phase = forms.MultipleChoiceField(required = True, widget=forms.CheckboxSelectMultiple, choices=PHASE_CHOICES, label =_("Phase d'instruction"))

    form = InstructionCheckerFilter(request.POST or None)
    if form.is_valid():
        coll_set = form.cleaned_data['name']
        phase_set = form.cleaned_data['phase']
        l = []
        if len(phase_set) ==2:
            return xckall(request, bdd, coll_set)
        elif phase_set[0] =='bound':
            return xckbd(request, bdd, coll_set)
        else:
            return xcknbd(request, bdd, coll_set)

    return render(request, 'epl/filter_ck_instrlist.html', locals())

@edmode6
def xckbd(request, bdd, coll_set):

    k =logstatus(request)
    version =epl_version
        
    xnewestfeat(request, bdd, "checker", "32", coll_set)

    l = []

    reclist = list(ItemRecord.objects.using(bdd).filter(status =2, rank =1).order_by('title'))

    for e in reclist:
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid, status =2)) == len(ItemRecord.objects.using(bdd).filter(sid =e.sid).exclude(rank =0)) and len(Instruction.objects.using(bdd).filter(sid =e.sid, name= "checker")) ==0:
            for coll in coll_set:
                if ItemRecord.objects.using(bdd).filter(lid =Library.objects.using(bdd).get(name =coll).lid, sid =e.sid).exclude(rank =0):
                    if ItemRecord.objects.using(bdd).get(sid =e.sid, rank =1) not in l:
                        l.append(ItemRecord.objects.using(bdd).get(sid =e.sid, rank =1)) #yehh ... rank =1 that's the trick !

    size = len(l)

    return render(request, 'epl/xckbd.html', locals())

@edmode6
def xcknbd(request, bdd, coll_set):

    k =logstatus(request)
    version =epl_version
    
    xnewestfeat(request, bdd, "checker", "33", coll_set)

    l = []

    reclist = list(ItemRecord.objects.using(bdd).filter(status =4, rank =1).order_by('title'))

    for e in reclist:
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid, status =4)) == len(ItemRecord.objects.using(bdd).filter(sid =e.sid).exclude(rank =0)) and len(Instruction.objects.using(bdd).filter(sid =e.sid, name= "checker")) ==1:
            for coll in coll_set:
                if ItemRecord.objects.using(bdd).filter(lid =Library.objects.using(bdd).get(name =coll).lid, sid =e.sid).exclude(rank =0):
                    if ItemRecord.objects.using(bdd).get(sid =e.sid, rank =1) not in l:
                        l.append(ItemRecord.objects.using(bdd).get(sid =e.sid, rank =1)) #yehh ... rank =1 that's the trick !

    size = len(l)

    return render(request, 'epl/xcknbd.html', locals())

@edmode6
def xckall(request, bdd, coll_set):

    k =logstatus(request)
    version =epl_version
    
    xnewestfeat(request, bdd, "checker", "34", coll_set)

    l = []

    for e in ItemRecord.objects.using(bdd).filter(status =2, rank =1):
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid, status =2)) == len(ItemRecord.objects.using(bdd).filter(sid =e.sid).exclude(rank =0)) and len(Instruction.objects.using(bdd).filter(sid =e.sid, name= "checker")) ==0:
            for coll in coll_set:
                if ItemRecord.objects.using(bdd).filter(lid =Library.objects.using(bdd).get(name =coll).lid, sid =e.sid).exclude(rank =0):
                    if ItemRecord.objects.using(bdd).get(sid =e.sid, rank =1) not in l:
                        l.append(ItemRecord.objects.using(bdd).get(sid =e.sid, rank =1)) #yehh ... rank =1 that's the trick !

    for e in ItemRecord.objects.using(bdd).filter(status =4, rank =1):
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid, status =4)) == len(ItemRecord.objects.using(bdd).filter(sid =e.sid).exclude(rank =0)) and len(Instruction.objects.using(bdd).filter(sid =e.sid, name= "checker")) ==1:
            for coll in coll_set:
                if ItemRecord.objects.using(bdd).filter(lid =Library.objects.using(bdd).get(name =coll).lid, sid =e.sid).exclude(rank =0):
                    if ItemRecord.objects.using(bdd).get(sid =e.sid, rank =1) not in l:
                        l.append(ItemRecord.objects.using(bdd).get(sid =e.sid, rank =1)) #yehh ... rank =1 that's the trick !

    l = sorted(l, key=serial_title)

    size = len(l)

    return render(request, 'epl/xckall.html', locals())


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Demande d'assignation d'un mot de passe"
					email_template_name = "registration/password_reset_email.html"
					from_email = replymail
					c = {
					"email":user.email,
					'domain': str(request.get_host()),
					'site_name': str(request.get_host()),
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, replymail , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse("Erreur d'entête rencontrée.")
				return redirect ("/accounts/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="registration/password_reset_form.html", context={"password_reset_form":password_reset_form})


def cgu(request):
    
    site_name = str(request.get_host())
    
    return render(request, 'epl/cgu.html', locals())


def confidentialite(request):
    
    return render(request, 'epl/confidentialite.html', locals())

#################################################################################################
def diffusion(request, bdd, smthng, origcontent):
    
    link = "http://" + str(request.get_host()) + "/" + bdd + "/diffusion/" + smthng + "/" + origcontent
    lien = "http://" + str(request.get_host()) + "/" + bdd + "/diffusion/"
    if smthng =="~":
        smthng =""
        origcontent =""
    else:
        origcontent ="\n\n\n\n=== Rappel message d'origine ===\n\n" + origcontent

    prj = Project.objects.using(bdd).all().order_by('pk')[0]
    list_diff =prj.descr.split(", ")
    try:
        list_diff.remove("")
    except:
        pass
    k =logstatus(request)
    flag =0
    
    global inletters, innumbers
    if request.method == "GET":
        chlist = range(len(numberlist))
        aleatindice = random.choices(chlist, k=1)[0]
        inletters = alphalist[aleatindice]
        innumbers = numberlist[aleatindice]
    else:#(POST)
        pass

    if k:
        class DiffusionForm(forms.Form):
            subject = forms.CharField(required=True, widget=forms.TextInput(attrs={'size': '40'}), initial =smthng, label ="Objet")
            message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Vous pouvez dimensionner ce cadre à partir de son coin inférieur droit."}), required=True, initial =origcontent, label ="Message")
            captcha = forms.CharField(required=True, widget=forms.TextInput(attrs={'size': '3'}), max_length=3, label =_("Prouvez que vous n'êtes pas un robot ; écrivez le nombre *** {} *** en chiffres").format(inletters))
    else:
        class DiffusionForm(forms.Form):
            from_email = forms.EmailField(required=True, label ="Votre email")
            subject = forms.CharField(required=True, widget=forms.TextInput(attrs={'size': '40'}), initial =smthng, label ="Objet")
            message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Vous pouvez dimensionner ce cadre à partir de son coin inférieur droit."}), required=True, initial =origcontent, label ="Message")
            captcha = forms.CharField(required=True, widget=forms.TextInput(attrs={'size': '3'}), max_length=3, label =_("Prouvez que vous n'êtes pas un robot ; écrivez le nombre *** {} *** en chiffres").format(inletters))
            
    if request.method == "GET":
        form = DiffusionForm()
    else:
        form = DiffusionForm(request.POST, request.FILES)
        if form.is_valid():
            if not form.cleaned_data["captcha"] == innumbers or not form.cleaned_data["captcha"] == innumbers:
                messages.info(request, _("Le nombre saisi était erroné"))
                return redirect(link)
            else:
                if k:
                    from_email = request.user.email
                    subject = form.cleaned_data["subject"]
                    message = form.cleaned_data['message']
                else:
                    from_email = form.cleaned_data["from_email"]
                    subject = form.cleaned_data["subject"]
                    message = form.cleaned_data['message']
                    if from_email not in list_diff:
                        flag =1
                        list_diff.append(from_email)
                        list_diff.sort()
                        try:
                            list_diff.remove("")
                        except:
                            pass
                re_message =message
                if len(re_message) >500:
                    re_message =message[:299] + "...\n\n..." + message[-200:]
                try:
                    message += "\n" + "\n" + \
                    "----------------------------------------------------------------------------------------" + "\n" + \
                    _("Pour répondre à ce message : ") + lien + iri_to_uri("Re: ") + iri_to_uri(quote(form.cleaned_data["subject"])) + "/" + iri_to_uri(quote(re_message.replace("/","|"))) + "\n" + "\n" + \
                    _("Pour un nouveau message : ") + lien + "~/~"  + "\n" + \
                    _("(Destinataires en copie cachée pour des raisons de sécurité et de confidentialité)") + "\n" + \
                    "----------------------------------------------------------------------------------------"
                    subject = "eplouribousse - [{}] : ".format(prj.name) + subject
                    email = EmailMessage(
                    subject,
                    message,
                    from_email,
                    [], list_diff)
                    email.send(fail_silently=False)
                except BadHeaderError:
                    return HttpResponse("Invalid header found.")
                messages.info(request, _("Votre message a bien été transmis à la liste de diffusion du projet [{}]".format(prj.name)))
                if not k:
                    messages.info(request, _("Vous le recevrez également"))
                    if flag:
                        messages.info(request, _("(Pour info : votre email ne figure pas dans la liste de diffusion --> 'Contact du projet' pour demander l'ajout.)"))
                messages.info(request, _("Pour des raisons de sécurité et de confidentialité, les destinataires sont en copie cachée."))
                return redirect("/./" + bdd)

    return render(request, "epl/diffusion.html", locals())

################################################################################################

@edmode1
def listall(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version
    code ="70"

##########################
    cases_list =[
    (_("Ressource écartée par exclusion d'une autre collection"), _("En savoir +")),#0 (status =0)
    (_("Ressource écartée par exclusion de votre collection"), _("Reconsidérer l'exclusion de ma collection",)),#1 (status =0)
    (_("Positionnement à réaliser"), _("Positionner ma collection")),#2 (status =0)
    (_("Positionnement modifiable"), _("Revoir le positionnement de ma collection (si besoin)")),#3 (status =0)
    (_("Arbitrage de type 1"), _("En savoir +")),#4 (status =0)
    (_("Arbitrage de type 1"), _("Reconsidérer le positionnement de ma collection")),#5 (status =0)
    (_("Arbitrage de type 0"), _("Reconsidérer le positionnement de ma collection")),#6 (status =0)
    (_("Instruction des éléments reliés en cours dans une bibliothèque vous précédant"), _("En savoir +")),#7 (status =0)
    (_("A vous d'instruire"), _("Instruire les éléments reliés")),#8 (status =1)
    (_("Instruction des éléments reliés en cours (vous avez déjà instruit)"), _("En savoir +")),#9 (status =2)
    (_("A vous d'instruire"), _("Instruire les éléments non reliés")),#10 (status 3)
    (_("Instruction des éléments non reliés en cours (vous avez déjà instruit)"), _("En savoir +")),#11 (status =4)
    (_("La ressource est complètement instruite"), _("Editer la résultante")),#12 (status =5)
    (_("Anomalie constatée"), _("En savoir +")),#13 (status =6)
    (_("Résultante à laquelle vous ne participez pas, ou autres cas"), _("En savoir +")),#14 (status =0)
    ]
    
    reclist = list(ItemRecord.objects.using(bdd).filter(lid = lid).order_by(sort, "rank", "excl"))
    resslist, case, action, sidlist = [], [], [], []
    for e in reclist:
        if ItemRecord.objects.using(bdd).filter(sid = e.sid).exclude(lid =lid):
            if ItemRecord.objects.using(bdd).get(sid = e.sid, lid =lid).status ==0:
                if len(ItemRecord.objects.using(bdd).filter(sid = e.sid)) - len(ItemRecord.objects.using(bdd).filter(sid = e.sid, rank =0)) <=1:
                    if ItemRecord.objects.using(bdd).get(sid = e.sid, lid = lid).rank !=0:#0
                        if e.sid not in sidlist:
                            resslist.append(e)
                            case.append(cases_list[0][0])
                            action.append(cases_list[0][1])
                            sidlist.append(e.sid)
                    elif ItemRecord.objects.using(bdd).get(sid = e.sid, lid = lid).rank ==0:#1
                        if e.sid not in sidlist:
                            resslist.append(e)
                            case.append(cases_list[1][0])
                            action.append(cases_list[1][1])
                            sidlist.append(e.sid)
                elif len(ItemRecord.objects.using(bdd).filter(sid = e.sid, rank =1)) >1:
                    if ItemRecord.objects.using(bdd).get(sid = e.sid, lid =lid).rank ==1:
                        if e.sid not in sidlist:
                            resslist.append(e)
                            case.append(cases_list[5][0])
                            action.append(cases_list[5][1])
                            sidlist.append(e.sid)
                    else:
                        if e.sid not in sidlist:
                            resslist.append(e)
                            case.append(cases_list[4][0])
                            action.append(cases_list[4][1])
                            sidlist.append(e.sid)
                elif len(ItemRecord.objects.using(bdd).filter(sid = e.sid, rank =99)) ==0 and len(ItemRecord.objects.using(bdd).filter(sid = e.sid).exclude(rank =0)) >=1 and len(ItemRecord.objects.using(bdd).filter(sid = e.sid, rank =1)) ==0:
                    if e.sid not in sidlist:
                        resslist.append(e)
                        case.append(cases_list[6][0])
                        action.append(cases_list[6][1])
                        sidlist.append(e.sid)
                elif len(ItemRecord.objects.using(bdd).filter(sid = e.sid, status =1)) ==1:
                    if e.sid not in sidlist:
                        resslist.append(e)
                        case.append(cases_list[7][0])
                        action.append(cases_list[7][1])
                        sidlist.append(e.sid)
                elif len(ItemRecord.objects.using(bdd).filter(sid = e.sid).exclude(rank =0)) >1 and len(ItemRecord.objects.using(bdd).filter(sid = e.sid, lid =lid, rank =99)) ==1:
                    if e.sid not in sidlist:
                        resslist.append(e)
                        case.append(cases_list[2][0])
                        sidlist.append(e.sid)
                        action.append(cases_list[2][1])                                                                                                     
                elif len(ItemRecord.objects.using(bdd).filter(sid = e.sid).exclude(rank =0)) >1 and len(ItemRecord.objects.using(bdd).filter(sid = e.sid, lid =lid, rank =99)) ==0 and len(Instruction.objects.using(bdd).filter(sid = e.sid)) ==0:#Peu importe si tous les positionnements sont réalisés ou non.
                    if e.sid not in sidlist:
                        resslist.append(e)
                        case.append(cases_list[3][0])
                        action.append(cases_list[3][1])
                        sidlist.append(e.sid)
                else:
                    if e.sid not in sidlist:
                        resslist.append(e)
                        case.append(cases_list[14][0])
                        action.append(cases_list[14][1])
                        sidlist.append(e.sid)                    
            elif ItemRecord.objects.using(bdd).get(sid = e.sid, lid =lid).status ==1:
                if e.sid not in sidlist:
                    resslist.append(e)
                    case.append(cases_list[8][0])
                    action.append(cases_list[8][1])
                    sidlist.append(e.sid)
            elif ItemRecord.objects.using(bdd).get(sid = e.sid, lid =lid).status ==2:
                if e.sid not in sidlist:
                    resslist.append(e)
                    case.append(cases_list[9][0])
                    action.append(cases_list[9][1])
                    sidlist.append(e.sid)
            elif ItemRecord.objects.using(bdd).get(sid = e.sid, lid =lid).status ==3:
                if e.sid not in sidlist:
                    resslist.append(e)
                    case.append(cases_list[10][0])
                    action.append(cases_list[10][1])
                    sidlist.append(e.sid)
            elif ItemRecord.objects.using(bdd).get(sid = e.sid, lid =lid).status ==4:
                if e.sid not in sidlist:
                    resslist.append(e)
                    case.append(cases_list[11][0])
                    action.append(cases_list[11][1])
                    sidlist.append(e.sid)
            elif ItemRecord.objects.using(bdd).get(sid = e.sid, lid =lid).status ==5:
                if e.sid not in sidlist:
                    resslist.append(e)
                    case.append(cases_list[12][0])
                    action.append(cases_list[12][1])
                    sidlist.append(e.sid)
            elif ItemRecord.objects.using(bdd).get(sid = e.sid, lid =lid).status ==6:
                if e.sid not in sidlist:
                    resslist.append(e)
                    case.append(cases_list[13][0])
                    action.append(cases_list[13][1])
                    sidlist.append(e.sid)
    total_list, i = [], 0
    while i <len(sidlist):
        total_list.append((resslist[i], case[i], action[i]))
        i +=1
##########################
    size = len(sidlist)

    libname = Library.objects.using(bdd).get(lid =lid).name
    newestfeat(request, bdd, libname, "70")

    return render(request, 'epl/listall.html', locals())


@edmode1
def filter_listall(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    "Filter list all"

    libname = (Library.objects.using(bdd).get(lid =lid)).name
    libch = ('',''),
    if Library.objects.using(bdd).all().exclude(lid ="999999999").exclude(lid =lid):
        for l in Library.objects.using(bdd).all().exclude(lid ="999999999").exclude(lid =lid).order_by('name'):
            libch += (l.name, l.name),

    class LibForm(forms.Form):
        name = forms.ChoiceField(required = False, widget=forms.Select, choices=libch, label =_("Croiser avec"))

    if request.method =="GET":
        form = LibForm()
    else:
        form = LibForm(request.POST or None)
        if form.is_valid():
            xlib = form.cleaned_data['name']
            if xlib:
                xlid = Library.objects.using(bdd).get(name =form.cleaned_data['name']).lid
                return xlistall(request, bdd, lid, xlid, sort)
            else:
                return listall(request, bdd, lid, sort)
        else:
            return HttpResponse("Invalid form")

    return render(request, 'epl/filter_listall.html', locals())


@edmode2
def xlistall(request, bdd, lid, xlid, sort):

    k =logstatus(request)
    version =epl_version
    code ="71"

##########################
    cases_list =[
    (_("Ressource écartée par exclusion d'une autre collection"), _("En savoir +")),#0 (status =0)
    (_("Ressource écartée par exclusion de votre collection"), _("Reconsidérer l'exclusion de ma collection",)),#1 (status =0)
    (_("Positionnement à réaliser"), _("Positionner ma collection")),#2 (status =0)
    (_("Positionnement modifiable"), _("Revoir le positionnement de ma collection (si besoin)")),#3 (status =0)
    (_("Arbitrage de type 1"), _("En savoir +")),#4 (status =0)
    (_("Arbitrage de type 1"), _("Reconsidérer le positionnement de ma collection")),#5 (status =0)
    (_("Arbitrage de type 0"), _("Reconsidérer le positionnement de ma collection")),#6 (status =0)
    (_("Instruction des éléments reliés en cours dans une bibliothèque vous précédant"), _("En savoir +")),#7 (status =0)
    (_("A vous d'instruire"), _("Instruire les éléments reliés")),#8 (status =1)
    (_("Instruction des éléments reliés en cours (vous avez déjà instruit)"), _("En savoir +")),#9 (status =2)
    (_("A vous d'instruire"), _("Instruire les éléments non reliés")),#10 (status 3)
    (_("Instruction des éléments non reliés en cours (vous avez déjà instruit)"), _("En savoir +")),#11 (status =4)
    (_("La ressource est complètement instruite"), _("Editer la résultante")),#12 (status =5)
    (_("Anomalie constatée"), _("En savoir +")),#13 (status =6)
    (_("Résultante à laquelle vous ne participez pas, ou autres cas"), _("En savoir +")),#14 (status =0)
    ]
    
    reclist = list(ItemRecord.objects.using(bdd).filter(lid = lid).order_by(sort, "rank", "excl"))
    resslist, case, action, sidlist = [], [], [], []
    for e in reclist:
        try:
            y = ItemRecord.objects.using(bdd).get(lid = xlid, sid = e.sid).excl
            if not y:
                if ItemRecord.objects.using(bdd).get(sid = e.sid, lid =lid).status ==0:
                    if len(ItemRecord.objects.using(bdd).filter(sid = e.sid)) - len(ItemRecord.objects.using(bdd).filter(sid = e.sid, rank =0)) <=1:
                        if ItemRecord.objects.using(bdd).get(sid = e.sid, lid = lid).rank !=0:#0
                            if e.sid not in sidlist:
                                resslist.append(e)
                                case.append(cases_list[0][0])
                                action.append(cases_list[0][1])
                                sidlist.append(e.sid)
                        elif ItemRecord.objects.using(bdd).get(sid = e.sid, lid = lid).rank ==0:#1
                            if e.sid not in sidlist:
                                resslist.append(e)
                                case.append(cases_list[1][0])
                                action.append(cases_list[1][1])
                                sidlist.append(e.sid)
                    elif len(ItemRecord.objects.using(bdd).filter(sid = e.sid, rank =1)) >1:
                        if ItemRecord.objects.using(bdd).get(sid = e.sid, lid =lid).rank ==1:
                            if e.sid not in sidlist:
                                resslist.append(e)
                                case.append(cases_list[5][0])
                                action.append(cases_list[5][1])
                                sidlist.append(e.sid)
                        else:
                            if e.sid not in sidlist:
                                resslist.append(e)
                                case.append(cases_list[4][0])
                                action.append(cases_list[4][1])
                                sidlist.append(e.sid)
                    elif len(ItemRecord.objects.using(bdd).filter(sid = e.sid, rank =99)) ==0 and len(ItemRecord.objects.using(bdd).filter(sid = e.sid).exclude(rank =0)) >=1 and len(ItemRecord.objects.using(bdd).filter(sid = e.sid, rank =1)) ==0:
                        if e.sid not in sidlist:
                            resslist.append(e)
                            case.append(cases_list[6][0])
                            action.append(cases_list[6][1])
                            sidlist.append(e.sid)
                    elif len(ItemRecord.objects.using(bdd).filter(sid = e.sid, status =1)) ==1:
                        if e.sid not in sidlist:
                            resslist.append(e)
                            case.append(cases_list[7][0])
                            action.append(cases_list[7][1])
                            sidlist.append(e.sid)
                    elif len(ItemRecord.objects.using(bdd).filter(sid = e.sid).exclude(rank =0)) >1 and len(ItemRecord.objects.using(bdd).filter(sid = e.sid, lid =lid, rank =99)) ==1:
                        if e.sid not in sidlist:
                            resslist.append(e)
                            case.append(cases_list[2][0])
                            sidlist.append(e.sid)
                            action.append(cases_list[2][1])                                                                                                     
                    elif len(ItemRecord.objects.using(bdd).filter(sid = e.sid).exclude(rank =0)) >1 and len(ItemRecord.objects.using(bdd).filter(sid = e.sid, lid =lid, rank =99)) ==0 and len(Instruction.objects.using(bdd).filter(sid = e.sid)) ==0:#Peu importe si tous les positionnements sont réalisés ou non.
                        if e.sid not in sidlist:
                            resslist.append(e)
                            case.append(cases_list[3][0])
                            action.append(cases_list[3][1])
                            sidlist.append(e.sid)
                    else:
                        if e.sid not in sidlist:
                            resslist.append(e)
                            case.append(cases_list[14][0])
                            action.append(cases_list[14][1])
                            sidlist.append(e.sid)                    
                elif ItemRecord.objects.using(bdd).get(sid = e.sid, lid =lid).status ==1:
                    if e.sid not in sidlist:
                        resslist.append(e)
                        case.append(cases_list[8][0])
                        action.append(cases_list[8][1])
                        sidlist.append(e.sid)
                elif ItemRecord.objects.using(bdd).get(sid = e.sid, lid =lid).status ==2:
                    if e.sid not in sidlist:
                        resslist.append(e)
                        case.append(cases_list[9][0])
                        action.append(cases_list[9][1])
                        sidlist.append(e.sid)
                elif ItemRecord.objects.using(bdd).get(sid = e.sid, lid =lid).status ==3:
                    if e.sid not in sidlist:
                        resslist.append(e)
                        case.append(cases_list[10][0])
                        action.append(cases_list[10][1])
                        sidlist.append(e.sid)
                elif ItemRecord.objects.using(bdd).get(sid = e.sid, lid =lid).status ==4:
                    if e.sid not in sidlist:
                        resslist.append(e)
                        case.append(cases_list[11][0])
                        action.append(cases_list[11][1])
                        sidlist.append(e.sid)
                elif ItemRecord.objects.using(bdd).get(sid = e.sid, lid =lid).status ==5:
                    if e.sid not in sidlist:
                        resslist.append(e)
                        case.append(cases_list[12][0])
                        action.append(cases_list[12][1])
                        sidlist.append(e.sid)
                elif ItemRecord.objects.using(bdd).get(sid = e.sid, lid =lid).status ==6:
                    if e.sid not in sidlist:
                        resslist.append(e)
                        case.append(cases_list[13][0])
                        action.append(cases_list[13][1])
                        sidlist.append(e.sid)
            else:
                if e.sid not in sidlist:
                    resslist.append(e)
                    case.append(cases_list[0][0])
                    action.append(cases_list[0][1])
                    sidlist.append(e.sid)
        except:
            pass
    total_list, i = [], 0
    while i <len(sidlist):
        total_list.append((resslist[i], case[i], action[i]))
        i +=1
##########################
            
    size = len(sidlist)

    libname = Library.objects.using(bdd).get(lid =lid).name
    xlibname = Library.objects.using(bdd).get(lid =xlid).name
    xnewestfeat(request, bdd, libname, "71", xlid)

    return render(request, 'epl/xlistall.html', locals())

def license(request):
    
    """
    License
    """

    return render(request, 'epl/license.html', locals())


#############################
# HIC DESINIT LABOR GEORGII #
#           ____            #
#           |  |            #
#       ~~~~~~~?~~~~        #
#         ( @  @ )          #
#           .\/.            #
#           <~~>            #
#          __[]__           #
#         |  []   |         #
#         |  []   |         #
#         t  [ ]  j         #
#            [  ]           #
#           [    ]          #
#           [    ]___       #
#       ==__[               #
#############################