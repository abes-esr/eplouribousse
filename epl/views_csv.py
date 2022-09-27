import csv
from django.http import HttpResponse
from .models import *
from django.utils.translation import ugettext as _
import os
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .views import selectbdd
from .decorators import edmode7
from datetime import datetime

@edmode7
def simple_csv(request, bdd, lid, xlid, recset, what, length):

    project = Project.objects.using(bdd).all().order_by('pk')[0].name

    fea =""
    
    size =int(length)

    if what =="10":
        fea ="rk"
    elif what =="11":
        fea ="xrk"
    elif what =="12":
        fea ="mrk"
    elif what =="20":
        fea ="arb"
    elif what =="21":
        fea ="xarb"
    elif what =="22":
        fea ="x1arb"
    elif what =="23":
        fea ="x0arb"
    elif what =="24":
        fea ="arb1"
    elif what =="25":
        fea ="arb0"
    elif what =="30":
        fea ="instr"
    elif what =="31":
        fea ="xinstr"
    elif what =="35":
        fea ="instr1b"
    elif what =="36":
        fea ="instrxb"
    elif what =="37":
        fea ="instr1nb"
    elif what =="38":
        fea ="instrxnb"
    elif what =="40":
        fea ="res"
    elif what =="41":
        fea ="resm"
    elif what =="42":
        fea ="resnm"
    elif what =="43":
        fea ="xmoth"
    elif what =="44":
        fea ="xnomoth"
    elif what =="50":
        fea ="excl"
    elif what =="60":
        fea ="faulty"

    filename = bdd + '_' + fea + '_' + lid + '_' + xlid + '.csv'
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    writer = csv.writer(response)
    writer.writerow(['#', _('requêté'), _('ppn'), "issn", _('rcr'), _("positionnement"), \
    _("motif d'exclusion"), _("commentaire"), _('bibliothèque'), _("cote"), \
    _("titre"), _("période de publication"), _("état de collection"), \
    _("lacunes"), _("statut")])


    c =1
    setrec =''.join(recset[1:-1])
    tresec = setrec.replace("'", "")
    rectes = tresec.replace(' ', '')
    parsed =rectes.split(',')
            
    for e in parsed:
        sid =e
        i =ItemRecord.objects.using(bdd).get(sid =sid, lid =lid)
        set =ItemRecord.objects.using(bdd).filter(sid =sid)
        writer.writerow([c, "x", sid, i.issn, lid, i.rank, i.excl, \
        i.comm, Library.objects.using(bdd).get(lid =lid).name, i.cn, i.title, \
        i.pubhist, i.holdstat, i.missing, i.status])
        if xlid =="None":
            for k in set.exclude(lid =lid):
                writer.writerow([c, "", k.sid, k.issn, k.lid, k.rank, k.excl, \
                k.comm, Library.objects.using(bdd).get(lid =k.lid).name, k.cn, k.title, \
                k.pubhist, k.holdstat, k.missing, k.status])
        elif xlid !="None":
            j =ItemRecord.objects.using(bdd).get(sid =sid, lid =xlid)
            writer.writerow([c, "x", sid, j.issn, xlid, j.rank, j.excl, \
            j.comm, Library.objects.using(bdd).get(lid =xlid).name, j.cn, j.title, \
            j.pubhist, j.holdstat, j.missing, j.status])
            for k in set.exclude(lid =lid).exclude(lid =xlid):
                writer.writerow([c, "", k.sid, k.issn, k.lid, k.rank, k.excl, \
                k.comm, Library.objects.using(bdd).get(lid =k.lid).name, k.cn, k.title, \
                k.pubhist, k.holdstat, k.missing, k.status])
        c +=1

    if size ==0:
        writer.writerow([_("(Aucun enregistrement)"),"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ])
    if c !=size +1:
        writer.writerow([_("(ATTENTION : LISTE INCOMPLETE)"),"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ])
    else:
        writer.writerow([_("(Liste complète)"),"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ])

    return response


@login_required
def uters_csv(request):

    """Extraction de l'ensemble des utilisateurs"""

    #contrôle d'accès ici
    if not request.user.is_staff:
        messages.info(request, _("Vous avez été renvoyé à cette page parce que vous n'avez pas les droits d'accès à la page que vous demandiez"))
        return selectbdd(request)

    host = str(request.get_host())
    adesso =str(datetime.now())
    filename = 'allusers_' + host + '_' + adesso + '_' + '_.csv'
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    writer = csv.writer(response)
    writer.writerow(['','','','', _("horodatage de l'extraction : "), adesso])
    writer.writerow([])
    writer.writerow(['#', _('centralid'), _('bdd'), _('bddid'), _("date d'enregistrement"), \
    _('dernier login'), _('identifiant'), _("email"), _('super admin'), _('admin général'), \
    _('admin projet'), _("checker"), _("contact bib (hors checker)"), \
    _('autorisé'), _('mode privé activé')])


    c =1
    for user in User.objects.all():
        if user.is_superuser and user.is_staff:
            writer.writerow([c, user.id, '', '', user.date_joined, \
            user.last_login, user.username, user.email, 'x', 'x', \
            '', '', '', '', ''])
            c +=1
        elif user.is_superuser and not user.is_staff: # (but it should not happen)
            writer.writerow([c, user.id, '', '', user.date_joined, \
            user.last_login, user.username, user.email, 'x', '', \
            '', '', '', '', ''])
            c +=1
        elif user.is_staff and not user.is_superuser:
            writer.writerow([c, user.id, '', '', user.date_joined, \
            user.last_login, user.username, user.email, '', 'x', \
            '', '', '', '', ''])
            c +=1
        else: # i.e. project users
            suffx =user.username[-2:]
            try:
                if Proj_setting.objects.using(suffx)[0].prv:
                    private =_("oui")
                else:
                    private =_("non")
                if BddAdmin.objects.using(suffx).filter(contact =user.email):
                    projadmin ="@" + suffx
                else:
                    projadmin =""

                if Utilisateur.objects.using(suffx).get(username =user.username).mail ==\
                Library.objects.using(suffx).get(name ="checker").contact or \
                Utilisateur.objects.using(suffx).get(username =user.username).mail ==\
                Library.objects.using(suffx).get(name ="checker").contact_bis or \
                Utilisateur.objects.using(suffx).get(username =user.username).mail ==\
                Library.objects.using(suffx).get(name ="checker").contact_ter:
                    projchecker ="@" + suffx
                else:
                    projchecker =""

                is_instructor =""
                for libelmt in Library.objects.using(suffx).all().exclude(name ="checker"):
                    if Utilisateur.objects.using(suffx).get(username =user.username).mail ==libelmt.contact:
                        is_instructor +="@" + str(Library.objects.using(suffx).get(name =libelmt.name).name) +" - "
                    if Utilisateur.objects.using(suffx).get(username =user.username).mail ==libelmt.contact_bis:
                        is_instructor +="@" + str(Library.objects.using(suffx).get(name =libelmt.name).name) +" - "
                    if Utilisateur.objects.using(suffx).get(username =user.username).mail ==libelmt.contact_ter:
                        is_instructor +="@" + str(Library.objects.using(suffx).get(name =libelmt.name).name) +" - "

                if Utilisateur.objects.using(suffx).get(username =user.username) and not \
                Library.objects.using(suffx).filter(contact =user.email) and not \
                Library.objects.using(suffx).filter(contact_bis =user.email) and not \
                Library.objects.using(suffx).filter(contact_ter =user.email) and not \
                BddAdmin.objects.using(suffx).filter(contact =user.email):
                    autoris ="x"
                else:
                    autoris =""

                writer.writerow([c, user.id, suffx, Utilisateur.objects.using(suffx).get(username =user.username).id, \
                user.date_joined, user.last_login, user.username, user.email, '', '', projadmin, projchecker, is_instructor, \
                autoris, private])

                c +=1

            except:
                writer.writerow([suffx, user.id, "absente", "?", user.date_joined, user.last_login, \
                user.username, user.email, '', '', '?', '?', '?', '?', '?'])
                c +=1

    return response
