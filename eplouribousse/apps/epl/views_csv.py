import csv
from django.http import HttpResponse
from .models import *
from django.utils.translation import ugettext as _

project = Project.objects.all().order_by('pk')[0].name

def simple_csv(request, lid, xlid, recset, what):

    fea =""
    parsed =recset.split("<ItemRecord: ")

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

    filename = fea + '_' + lid + '_' + xlid + '.csv'
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    writer = csv.writer(response)
    writer.writerow(['#', _('requêté'), _('ppn'), "issn", _('rcr'), _("positionnement"), \
    _("motif d'exclusion"), _("commentaire"), _('bibliothèque'), _("cote"), \
    _("titre"), _("période de publication"), _("état de collection"), \
    _("lacunes"), _("statut")])

    try:
        c =1
        for e in parsed[1:]:
            sid =e[0:9]
            i =ItemRecord.objects.get(sid =sid, lid =lid)
            set =ItemRecord.objects.filter(sid =sid)
            writer.writerow([c, "x", sid, i.issn, lid, i.rank, i.excl, \
            i.comm, Library.objects.get(lid =lid).name, i.cn, i.title, \
            i.pubhist, i.holdstat, i.missing, i.status])
            if xlid =="None":
                for k in set.exclude(lid =lid):
                    writer.writerow([c, "", k.sid, k.issn, k.lid, k.rank, k.excl, \
                    k.comm, Library.objects.get(lid =k.lid).name, k.cn, k.title, \
                    k.pubhist, k.holdstat, k.missing, k.status])
            elif xlid !="None":
                j =ItemRecord.objects.get(sid =sid, lid =xlid)
                writer.writerow([c, "x", sid, j.issn, xlid, j.rank, j.excl, \
                j.comm, Library.objects.get(lid =xlid).name, j.cn, j.title, \
                j.pubhist, j.holdstat, j.missing, j.status])
                for k in set.exclude(lid =lid).exclude(lid =xlid):
                    writer.writerow([c, "", k.sid, k.issn, k.lid, k.rank, k.excl, \
                    k.comm, Library.objects.get(lid =k.lid).name, k.cn, k.title, \
                    k.pubhist, k.holdstat, k.missing, k.status])
            c +=1
        if c ==1:
            writer.writerow([_("(Aucun enregistrement)")])
    except:
        writer.writerow([_("(Aucun enregistrement)")])

    return response
