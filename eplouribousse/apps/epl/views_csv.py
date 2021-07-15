import csv
from django.http import HttpResponse
from .models import *
from django.utils.translation import ugettext as _
import os
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .views import selectbdd

def simple_csv(request, bdd, lid, xlid, recset, what, length):

    project = Project.objects.using(bdd).all().order_by('pk')[0].name

    fea =""
    parsed =recset.split("<ItemRecord: ")
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
    for e in parsed[1:]:
        sid =e[0:9]
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

    filename = 'alluters.csv'
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    writer = csv.writer(response)
    writer.writerow(['#', _('bdd'), _('bddid'), _('centralid'), _('identifiant'), _("email"), _('admin'), _("checker"), \
    _("contact bib (hors checker)"), _('contact pour')])

    BDD_CHOICES =('', ''),

    for i in [n for n in range(100)]:
        if os.path.isfile('{:02d}.db'.format(i)):
            p = Project.objects.using('{:02d}'.format(i)).all().order_by('pk')[0].name
            BDD_CHOICES += ('{:02d}'.format(i), p),

    c =1

    for bddelmt in BDD_CHOICES[1:]:

        for uterelmt in Utilisateur.objects.using(bddelmt[0]).all():
            if BddAdmin.objects.using(bddelmt[0]).filter(contact =uterelmt.mail):
                ad ="x"
                adlist ="@ admin - "
            else:
                ad =""
            if Utilisateur.objects.using(bddelmt[0]).get(username =uterelmt.username).mail ==\
            Library.objects.using(bddelmt[0]).get(name ="checker").contact or \
            Utilisateur.objects.using(bddelmt[0]).get(username =uterelmt.username).mail ==\
            Library.objects.using(bddelmt[0]).get(name ="checker").contact_bis or \
            Utilisateur.objects.using(bddelmt[0]).get(username =uterelmt.username).mail ==\
            Library.objects.using(bddelmt[0]).get(name ="checker").contact_ter:
                bibcheck ="x"
                bibchecklist ="@ checker - "
            else:
                bibcheck =""

            bibnotcheck, bibnotchecklist ="", ""
            for libelmt in Library.objects.using(bddelmt[0]).all().exclude(name ="checker"):
                if Utilisateur.objects.using(bddelmt[0]).get(username =uterelmt.username).mail ==libelmt.contact:
                    bibnotcheck ="x"
                    bibnotchecklist +="@ " + str(Library.objects.using(bddelmt[0]).get(name =libelmt.name).name) +" - "
                if Utilisateur.objects.using(bddelmt[0]).get(username =uterelmt.username).mail ==libelmt.contact_bis:
                    bibnotcheck ="x"
                    bibnotchecklist +="@ " + str(Library.objects.using(bddelmt[0]).get(name =libelmt.name).name) +" - "
                if Utilisateur.objects.using(bddelmt[0]).get(username =uterelmt.username).mail ==libelmt.contact_ter:
                    bibnotcheck ="x"
                    bibnotchecklist +="@ " + str(Library.objects.using(bddelmt[0]).get(name =libelmt.name).name) +" - "
            list =adlist + bibchecklist + bibnotchecklist

            writer.writerow([c, bddelmt[0], Utilisateur.objects.using(bddelmt[0]).get(username =uterelmt.username).id, \
            User.objects.get(username =uterelmt.username, email = uterelmt.mail).id, \
            Utilisateur.objects.using(bddelmt[0]).get(username =uterelmt.username).username, \
            Utilisateur.objects.using(bddelmt[0]).get(username =uterelmt.username).mail, ad, bibcheck, \
            bibnotcheck, list])

            adlist, bibchecklist, bibnotchecklist ="", "", "" # remise à zéro des compteurs

    return response
