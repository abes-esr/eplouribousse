from django.shortcuts import render

from django.http import HttpResponse

from .models import *

from .forms import *

from .excluchoices import EXCLUSION_CHOICES

from django.core.mail import send_mail

from django.db.models.functions import Now

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from django.core.files.storage import FileSystemStorage

from django.contrib.auth.decorators import login_required

from django.utils.translation import ugettext as _

from django.contrib.auth.models import User

def lang(request):
    return render(request, 'epl/language.html', {})

def pdfedition(request, sid, lid):

    filename = sid + '_' + lid + '.pdf'
    dirfile = "/tmp/" + filename

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename="{}".format(dirfile), pagesize=landscape(A4))
    elements = []

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    project = Project.objects.all().order_by('pk')[0].name
    libname = Library.objects.get(lid =lid).name
    title = ItemRecord.objects.get(sid =sid, lid =lid).title
    sid = ItemRecord.objects.get(sid =sid, lid =lid).sid
    cn = ItemRecord.objects.get(sid =sid, lid =lid).cn
    issn = ItemRecord.objects.get(sid =sid, lid =lid).issn
    pubhist = ItemRecord.objects.get(sid =sid, lid =lid).pubhist
    instructions = Instruction.objects.filter(sid =sid).order_by('line')
    properinstructions = Instruction.objects.filter(sid =sid, name =libname)
    otherinstructions = Instruction.objects.filter(sid =sid, oname =libname)
    libinstructions = properinstructions.union(otherinstructions).order_by('line')
    controlbd = Instruction.objects.get(sid =sid, bound ='x', name ='checker').descr
    controlnotbd = Instruction.objects.exclude(bound ='x').get(sid =sid, name ='checker').descr
    mothercollection = Library.objects.get(lid =ItemRecord.objects.get(sid =sid, rank =1).lid).name

    datap =[
    [_('Projet'), project],
    [_("Titre"), Paragraph(title, styles['Normal'])],
    [_("Collection"), str(libname + "    ----->    " + _('cote') + " : " + cn)],
    ]

    tp =Table(datap)

    table_stylep = TableStyle([('ALIGN', (0, 0), (-1,-1), 'LEFT'),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),])

    tp.setStyle(table_stylep)

    elements.append(tp)

    datas =[
    [str(_('issn') + " : " + issn), str(_('ppn') + " : " + sid), str(_('historique de la publication') + " : " + pubhist)]
    ]

    ts=Table(datas)

    table_styles = TableStyle([('ALIGN', (0, 0), (-1,-1), 'LEFT'),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),])

    ts.setStyle(table_styles)

    elements.append(ts)

    datacoll =[]

    for e in ItemRecord.objects.filter(sid =sid).order_by("rank"):
        if e.rank ==1:
            datacoll.append([e.rank, Library.objects.get(lid =e.lid).name, _("collection mère")])
        elif e.rank ==0:
            datacoll.append([e.rank, Library.objects.get(lid =e.lid).name, e.excl])
        else:
            datacoll.append([e.rank, Library.objects.get(lid =e.lid).name, _("a pris part")])

    tcoll=Table(datacoll)

    table_stylecoll = TableStyle([('ALIGN', (0, 0), (-1,-1), 'LEFT'),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),])

    tcoll.setStyle(table_stylecoll)

    elements.append(tcoll)

    data = [
    ["", "", "", "", "", "", ""],
    ['#', _('bibliothèque'), _('relié ?'), _('bib. remédiée'), _('segment'), _('exception'), _('améliorable')]
    ]
    Table(data, colWidths=None, rowHeights=None, style=None, splitByRow=1, repeatRows=0, repeatCols=0, rowSplitRange=None, spaceBefore=None, spaceAfter=None)
    for i in instructions:
        data.append([i.line, i.name, i.bound, i.oname, i.descr, Paragraph(i.exc, styles['Normal']), Paragraph(i.degr, styles['Normal'])])

    t=Table(data)

    table_style = TableStyle([('ALIGN', (1, 1), (6, 1), 'CENTER'),
    ('INNERGRID', (0,1), (-1,-1), 0.25, colors.black),
    ('BOX', (0,1), (-1,-1), 0.25, colors.black),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),])
    k =1
    for i in libinstructions:
        row = i.line + 1
        k +=1 #row number
        table_style.add('TEXTCOLOR', (0, row ), (6, row), colors.red)
    table_style.add('ALIGN', (0, 1), (-7, -1), 'CENTER')
    table_style.add('ALIGN', (0, 2), (-5, -1), 'CENTER')
    table_style.add('ALIGN', (1, 1), (-6, -1), 'LEFT')

    t.setStyle(table_style)

    elements.append(t)

    doc.build(elements)

    fs = FileSystemStorage("/tmp")
    with fs.open(filename) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)
        return response

    return response

def edallpdf(request, lid):

    filename = lid + '.pdf'
    dirfile = "/tmp/" + filename

    libname = Library.objects.get(lid =lid).name

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename="{}".format(dirfile), pagesize=landscape(A4))
    elements = []

    #For the lid identified library, getting ressources whose the resulting \
    #collection has been entirely completed and may consequently be edited.
    #Trick : These ressources have two instructions with name = 'checker' :
    #This is like "tobeedited" (see below)

    l = ItemRecord.objects.filter(lid =lid).exclude(rank =0)

    #Initializing a list of ressources to edit :
    resslist = []

    for e in l:
        nl = Instruction.objects.filter(sid =e.sid)
        k = nl.filter(name = "checker")
        if len(k) ==2:
            resslist.append(e)

    for r in resslist:

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        project = Project.objects.all().order_by('pk')[0].name
        title = ItemRecord.objects.get(sid =r.sid, lid =lid).title
        sid = ItemRecord.objects.get(sid =r.sid, lid =lid).sid
        cn = ItemRecord.objects.get(sid =sid, lid =lid).cn
        issn = ItemRecord.objects.get(sid =r.sid, lid =lid).issn
        pubhist = ItemRecord.objects.get(sid =r.sid, lid =lid).pubhist
        instructions = Instruction.objects.filter(sid =r.sid).order_by('line')
        properinstructions = Instruction.objects.filter(sid =r.sid, name =libname)
        otherinstructions = Instruction.objects.filter(sid =r.sid, oname =libname)
        libinstructions = properinstructions.union(otherinstructions).order_by('line')
        controlbd = Instruction.objects.get(sid =r.sid, bound ='x', name ='checker').descr
        controlnotbd = Instruction.objects.exclude(bound ='x').get(sid =r.sid, name ='checker').descr
        mothercollection = Library.objects.get(lid =ItemRecord.objects.get(sid =r.sid, rank =1).lid).name

        datap =[
        [_('Projet'), project],
        [_("Titre"), Paragraph(title, styles['Normal'])],
        [_("Collection"), str(libname + "    ----->    " + _('cote') + " : " + cn)],
        ]

        tp =Table(datap)

        table_stylep = TableStyle([('ALIGN', (0, 0), (-1,-1), 'LEFT'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),])

        tp.setStyle(table_stylep)

        elements.append(tp)

        datas =[
        [str(_('issn') + " : " + issn), str(_('ppn') + " : " + sid), str(_('historique de la publication') + " : " + pubhist)]
        ]

        ts=Table(datas)

        table_styles = TableStyle([('ALIGN', (0, 0), (-1,-1), 'LEFT'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),])

        ts.setStyle(table_styles)

        elements.append(ts)

        datacoll =[]

        for e in ItemRecord.objects.filter(sid =sid).order_by("rank"):
            if e.rank ==1:
                datacoll.append([e.rank, Library.objects.get(lid =e.lid).name, _("collection mère")])
            elif e.rank ==0:
                datacoll.append([e.rank, Library.objects.get(lid =e.lid).name, e.excl])
            else:
                datacoll.append([e.rank, Library.objects.get(lid =e.lid).name, _("a pris part")])

        tcoll=Table(datacoll)

        table_stylecoll = TableStyle([('ALIGN', (0, 0), (-1,-1), 'LEFT'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),])

        tcoll.setStyle(table_stylecoll)

        elements.append(tcoll)

        data = [
        ["", "", "", "", "", "", ""],
        ['#', _('bibliothèque'), _('relié ?'), _('bib. remédiée'), _('segment'), _('exception'), _('améliorable')]
        ]
        Table(data, colWidths=None, rowHeights=None, style=None, splitByRow=1, repeatRows=0, repeatCols=0, rowSplitRange=None, spaceBefore=None, spaceAfter=None)
        for i in instructions:
            data.append([i.line, i.name, i.bound, i.oname, i.descr, Paragraph(i.exc, styles['Normal']), Paragraph(i.degr, styles['Normal'])])

        t=Table(data)

        table_style = TableStyle([('ALIGN', (1, 1), (6, 1), 'CENTER'),
        ('INNERGRID', (0,1), (-1,-1), 0.25, colors.black),
        ('BOX', (0,1), (-1,-1), 0.25, colors.black),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),])
        k =1
        for i in libinstructions:
            row = i.line + 1
            k +=1 #row number
            table_style.add('TEXTCOLOR', (0, row ), (6, row), colors.red)
        table_style.add('ALIGN', (0, 1), (-7, -1), 'CENTER')
        table_style.add('ALIGN', (0, 2), (-5, -1), 'CENTER')
        table_style.add('ALIGN', (1, 1), (-6, -1), 'LEFT')

        t.setStyle(table_style)

        elements.append(t)

        elements.append(PageBreak())

    doc.build(elements)

    fs = FileSystemStorage("/tmp")
    with fs.open(filename) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)
        return response

    return response

def ranktotake(request, lid):

    #Getting ressources whose this lid must but has not yet taken rank :
    reclist = list(ItemRecord.objects.filter(lid = lid, rank = 99))
    resslist = []
    for e in reclist:
        itemlist = list(ItemRecord.objects.filter(sid = e.sid).exclude(rank =0))
        if len(itemlist) > 1:
            resslist.append(e)
    l = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/to_rank_list.html', { 'toranklist' : resslist, \
    'lid' : lid, 'name' : libname, 'size' : l})


def notintime(request, sid, lid):

    lib = Library.objects.get(lid = lid)
    ress = ItemRecord.objects.get(sid =sid, rank =1).title
    return render(request, 'epl/notintime.html', { 'library' : lib, 'title' : ress, 'lid' : lid, 'sid' : sid, })


@login_required
def takerank(request, sid, lid):

    #Authentication control :
    if not request.user.email ==Library.objects.get(lid =lid).contact:
        return home(request)

    do = notintime(request, sid, lid)

    #Control (takerank only if still possible ; status still ==0 for all attached libraries ; lid not "999999999")
    try:
        if len(list(ItemRecord.objects.filter(sid =sid).exclude(status =0))):
            return do
        elif lid =="999999999":
            return do
    except:
        z =1 #This is just to continue

    # For position form :
    i = ItemRecord.objects.get(sid = sid, lid = lid)
    f = PositionForm(request.POST, instance=i)
    if f.is_valid():
        if len(ItemRecord.objects.filter(sid =sid).exclude(status =0)) ==0:
            if i.excl !='':
                i.rank =0
            f.save()
            flag =0
        else:
            flag =1
    else:
        flag =0

    # Item records list :
    itemlist = ItemRecord.objects.filter(sid =  sid)
    itemlist = list(itemlist)

    # Ressource data :
    ress = itemlist[0]

    # Library data :
    lib = Library.objects.get(lid = lid)

    # Other status modification if all libraries have taken rank (as of now status =0) :
    # 0 --> 1 : item whose lid identified library must begin bound elements instructions on the sid identified serial (rank =1, no arbitration)
    # ordering by pk for identical ranks upper than 1.
    if len(ItemRecord.objects.filter(sid =sid, rank =99)) ==0 and len(ItemRecord.objects.filter(sid =sid, rank =1)) ==1 and len(ItemRecord.objects.filter(sid =sid).exclude(rank =0)) >1:
        k = ItemRecord.objects.filter(sid =sid).exclude(rank =0).exclude(rank =99).order_by("rank", "pk")[0]
        if k.status !=1:
            k.status =1
            k.save()

    return render(request, 'epl/ranking.html',\
     { 'ressource' : ress, 'items' : itemlist,
     'library' : lib, 'form' : f, 'lid' : lid, 'flag' : flag, })


@login_required
def addinstr(request, sid, lid):

    #Authentication control :
    if not request.user.email ==Library.objects.get(lid =lid).contact:
        return home(request)

    do = notintime(request, sid, lid)

    #Control (addinstr only if it's up to the considered lid)
    try:
        if lid !="999999999":
            if ItemRecord.objects.get(sid =sid, lid =lid).status not in [1, 3]:
                return do

        else: # i.e. lid =="999999999"
            if len(list((Instruction.objects.filter(sid =sid)).filter(name ='checker'))) ==2:
                return do
            elif len(list((Instruction.objects.filter(sid =sid)).filter(name ='checker'))) ==1:
                if len(list(ItemRecord.objects.filter(sid =sid).exclude(rank =0))) != len(list(ItemRecord.objects.filter(sid =sid, status =4))):
                    return do
            else: # i.e. len(list((Instruction.objects.filter(sid =sid)).filter(name ='checker'))) ==0
                if len(list(ItemRecord.objects.filter(sid =sid).exclude(rank =0))) != len(list(ItemRecord.objects.filter(sid =sid, status =2))):
                    return do
    except:
        z =1 #This is just to continue


    #Ressource data :
    itemlist = ItemRecord.objects.filter(sid = sid).exclude(rank =0).order_by("rank", 'pk')
    ress = itemlist[0]

    #Library data :
    lib = Library.objects.get(lid = lid)

    # Library list ordered by 'rank' (except "checker" which must be the last one)
    # to get from the precedent item list above :
    liblist = []
    for e in itemlist:
        liblist.append(Library.objects.get(lid = e.lid))
    liblist.append(Library.objects.get(name = 'checker'))

    #Remedied library list :
    remliblist = []
    for e in itemlist:
        remliblist.append(Library.objects.get(lid = e.lid))
    if (Library.objects.get(lid =lid)).name != 'checker':
        remliblist.remove(Library.objects.get(name = lib.name))

    #Info :
    info =""

    #Stage (bound or not bound) :
    if len(list((Instruction.objects.filter(sid =sid)).filter(name ='checker'))) ==0:
        bd =_('éléments reliés')
    elif len(list((Instruction.objects.filter(sid =sid)).filter(name ='checker'))) ==1:
        bd =_('éléments non reliés')

    if lid =="999999999":
        do = endinstr(request, sid, lid)
        return do

    else:
        #Instruction form instanciation and validation :
        i = Instruction(sid = sid, name = lib.name)
        f = InstructionForm(request.POST, instance =i)
        q = "x"
        if f.is_valid():
            if len(list((Instruction.objects.filter(sid =sid)).\
            filter(name ='checker'))):
                q =" "
            else:
                q ="x"
            i.bound =q
            #A line may only be registered once :
            if not len(Instruction.objects.filter(sid =sid, name =lib.name, bound =i.bound, oname =i.oname, descr =i.descr, exc =i.exc, degr =i.degr)):
                i.line +=1
                i.time =Now()
                f.save()
            else:
                info = _("Vous ne pouvez pas valider deux fois la même ligne d'instruction.")

        #Renumbering instruction lines :
        try:
            instr = Instruction.objects.filter(sid = sid).order_by('line', '-pk')
            j, k =0, 1
            while j <= len(instr):
                instr[j].line = k
                instr[j].save()
                j +=1
                k +=1
        except:
            pass
        instrlist = Instruction.objects.filter(sid = sid).order_by('line')

        try:
            pklastone = Instruction.objects.filter(sid = sid).latest('pk').pk
        except:
            pklastone =0

    return render(request, 'epl/addinstruction.html', { 'ressource' : ress, \
    'library' : lib, 'instructions' : instrlist , 'form' : f, 'librarylist' : \
    liblist, 'remedied_lib_list' : remliblist, 'sid' : sid, 'stage' : bd, 'info' : info, \
    'lid' : lid, 'expected' : q, 'lastone' : pklastone,})

@login_required
def delinstr(request, sid, lid):

    #Authentication control :
    if not request.user.email ==Library.objects.get(lid =lid).contact:
        return home(request)

    do = notintime(request, sid, lid)

    #Control (delinstr only if it's up to the considered library == same conditions as for addinstr if lid not "999999999")
    try:
        if lid !="999999999":
            if ItemRecord.objects.get(sid = sid, lid =lid).status not in [1, 3]:
                return do

        else: # i.e. lid =="999999999"
            return do

    except:
        z =1 #This is just to continue

    #Ressource data :
    itemlist = ItemRecord.objects.filter(sid = sid).exclude(rank =0).order_by("rank", 'pk')
    ress = itemlist[0]

    #Library data :
    lib = Library.objects.get(lid = lid)

    # Library list ordered by 'rank' (except "checker" which must be the last one)
    # to get from the precedent item list above :
    liblist = []
    for e in itemlist:
        liblist.append(Library.objects.get(lid = e.lid))
    liblist.append(Library.objects.get(name = 'checker'))

    #Remedied library list :
    remliblist = []
    for e in itemlist:
        remliblist.append(Library.objects.get(lid = e.lid))
    if (Library.objects.get(lid =lid)).name != 'checker':
        remliblist.remove(Library.objects.get(name = lib.name))

    #Info :
    info =""

    #Stage (bound or not bound) :
    if len(list((Instruction.objects.filter(sid =sid)).filter(name ='checker'))) ==0:
        bd =_('éléments reliés')
        # ress_stage ='reliés'
        expected = "x"
    elif len(list((Instruction.objects.filter(sid =sid)).filter(name ='checker'))) ==1:
        bd =_('éléments non reliés')
        # ress_stage ='non reliés'
        expected = " "
    else:   # (==2)
        bd = _("instructions terminées")

    answer = ""

    i = Instruction(sid = sid, name = lib.name)
    f = InstructionForm(request.POST, instance=i) # for deletion of an instruction line
    if f.is_valid():
        try:
            j = Instruction.objects.get(sid =sid, bound = expected, name =lib.name, line =i.line)
            j.delete()
        except:
            answer = _(" <=== Suppression non permise (vérifiez les conditions requises) ")

    #Renumbering instruction lines :
    try:
        instr = Instruction.objects.filter(sid = sid).order_by('line', '-pk')
        j, k =0, 1
        while j <= len(instr):
            instr[j].line = k
            instr[j].save()
            j +=1
            k +=1
    except:
        pass
    instrlist = Instruction.objects.filter(sid = sid).order_by('line')


    #Library list ordered by 'rank' to get from the precedent item list above :
    liblist = []
    for e in itemlist:
        liblist.append(Library.objects.get(lid = e.lid))
    liblist.append(Library.objects.get(name = 'checker'))

    return render(request, 'epl/delinstruction.html', { 'ressource' : ress, \
    'library' : lib, 'instructions' : instrlist , 'form' : f, 'librarylist' : \
    liblist, 'remedied_lib_list' : remliblist, 'sid' : sid, 'stage' : bd, 'info' : info, \
    'lid' : lid, 'expected' : expected, 'answer' : answer,})

@login_required
def endinstr(request, sid, lid):

    #Authentication control :
    if not request.user.email ==Library.objects.get(lid =lid).contact:
        return home(request)

    do = notintime(request, sid, lid)

    #Control (endinstr only if it's up to the considered library == same conditions as for addinstr)
    try:
        if lid !="999999999":
            if ItemRecord.objects.get(sid = sid, lid =lid).status not in [1, 3]:
                return do

        else: # i.e. lid =="999999999"
            if len(list((Instruction.objects.filter(sid =sid)).filter(name ='checker'))) ==2:
                return do
            elif len(list((Instruction.objects.filter(sid =sid)).filter(name ='checker'))) ==1:
                if len(list(ItemRecord.objects.filter(sid =sid).exclude(rank =0))) != len(list(ItemRecord.objects.filter(sid =sid, status =4))):
                    return do
            else: # i.e. len(list((Instruction.objects.filter(sid =sid)).filter(name ='checker'))) ==0
                if len(list(ItemRecord.objects.filter(sid =sid).exclude(rank =0))) != len(list(ItemRecord.objects.filter(sid =sid, status =2))):
                    return do
    except:
        z =1 #This is just to continue

    #Ressource data :
    itemlist = ItemRecord.objects.filter(sid = sid).exclude(rank =0).order_by("rank", 'pk')
    ress = itemlist[0]

    #Library data :
    lib = Library.objects.get(lid = lid)

    # Library list ordered by 'rank' (except "checker" which must be the last one)
    # to get from the precedent item list above :
    liblist = []
    for e in itemlist:
        liblist.append(Library.objects.get(lid = e.lid))
    liblist.append(Library.objects.get(name = 'checker'))

    #Remedied library list :
    remliblist = []
    for e in itemlist:
        remliblist.append(Library.objects.get(lid = e.lid))
    if (Library.objects.get(lid =lid)).name != 'checker':
        remliblist.remove(Library.objects.get(name = lib.name))

    #Info :
    info =""

    #Stage (bound or not bound) :
    if len(list((Instruction.objects.filter(sid =sid)).filter(name ='checker'))) ==0:
        bd =_('éléments reliés')
        # ress_stage ='reliés'
        expected = "x"
    elif len(list((Instruction.objects.filter(sid =sid)).filter(name ='checker'))) ==1:
        bd =_('éléments non reliés')
        # ress_stage ='non reliés'
        expected = " "
    else:   # (==2)
        bd = _("instructions terminées")
        expected = _("ni relié, ni non reliés")

    answer = ""

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
            if len(Instruction.objects.filter(sid =sid, name ='checker')) ==0:
                checkerinstruction.bound ="x"
            if len(Instruction.objects.filter(sid =sid, name ='checker')) ==1:
                checkerinstruction.bound =" "
            checkerinstruction.descr =Now()
            checkerinstruction.save()

            #Renumbering instruction lines :
            try:
                instr = Instruction.objects.filter(sid = sid).order_by('line', '-pk')
                j, k =0, 1
                while j <= len(instr):
                    instr[j].line = k
                    instr[j].save()
                    j +=1
                    k +=1
            except:
                pass

            instrlist = Instruction.objects.filter(sid = sid).order_by('line')

            #Status changing :
            j = ItemRecord.objects.get(sid =sid, rank =1)
            if len(Instruction.objects.filter(sid =sid, name ='checker')) ==1:
                if j.status !=3:
                    j.status = 3
                    j.save()
                    #Message data :
                    subject = "eplouribousse : " + str(sid) + " / " + str(nextlid)
                    host = str(request.get_host())
                    message = _("Votre tour est venu d'instruire la fiche eplouribousse pour le ppn ") + str(sid) +\
                    " : " + "https://" + host + "/add/" + str(sid) + '/' + str(nextlid)
                    dest = nextlib.contact
                    dest = [dest]
                    exp = Library.objects.get(lid ="999999999").contact
                    send_mail(subject, message, exp, dest, fail_silently=True, )

            if len(Instruction.objects.filter(sid =sid, name ='checker')) ==2:
                for e in ItemRecord.objects.filter(sid =sid, status =4):
                    e.status = 5
                    e.save()

            do = instrtodo(request, lid)
            return do

        elif u.is_valid() and t.checkin =="Notify": #In this case BDD administrator will be informed of errors in the instructions.
            # Change all ItemRecords status (except those with rank =0) for the considered sid to status =6
            for e in ItemRecord.objects.filter(sid =sid).exclude(rank =0):
                e.status =6
                e.save()

            #Message data to the BDD administrator(s):
            subject = "eplouribousse : " + str(sid) + " / " + "status = 6"
            message = _("Le statut est passé à 6 pour les enregistrements des bibliothèques participant à la résultante de la ressource citée en objet ; une intervention dans la base de données est attendue de votre part. Merci !")
            destprov = BddAdmin.objects.all()
            dest =[]
            for d in destprov:
                dest.append(d.contact)
            exp = Library.objects.get(lid ="999999999").contact
            send_mail(subject, message, exp, dest, fail_silently=True, )

            do = instrtodo(request, lid)
            return do

    else: #lid !="999999999"
        if z.is_valid() and y.flag ==True:
            if len(Instruction.objects.filter(sid =sid, name ='checker')) ==0:
                if ItemRecord.objects.filter(sid =sid, status =0).exclude(lid =lid).exclude(rank =0).exists():
                    nextitem = ItemRecord.objects.filter(sid =sid, status =0).exclude(lid =lid).exclude(rank =0).order_by('rank', 'pk')[0]
                    nextlid = nextitem.lid
                    nextlib = Library.objects.get(lid =nextlid)
                    j, k = ItemRecord.objects.get(sid =sid, lid =lid), ItemRecord.objects.get(sid =sid, lid =nextlid)
                    if j.status !=2:
                        j.status, k.status = 2, 1
                        j.save()
                        k.save()
                else:
                    #(No nextitem, the whole pool of libraries finished instructing the current form, i.e. bound or not bound.)
                    nextlid = Library.objects.get(lid ="999999999").lid
                    nextlib = Library.objects.get(lid =nextlid)
                    j = ItemRecord.objects.get(sid =sid, lid =lid)
                    if j.status !=2:
                        j.status = 2
                        j.save()

            elif len(Instruction.objects.filter(sid =sid, name ='checker')) ==1:
                if ItemRecord.objects.filter(sid =sid, status =2).exclude(lid =lid).exclude(rank =0).exists():
                    nextitem = ItemRecord.objects.filter(sid =sid, status =2).exclude(lid =lid).exclude(rank =0).order_by('rank', 'pk')[0]
                    nextlid = nextitem.lid
                    nextlib = Library.objects.get(lid =nextlid)
                    j, k = ItemRecord.objects.get(sid =sid, lid =lid), ItemRecord.objects.get(sid =sid, lid =nextlid)
                    if j.status !=4:
                        j.status, k.status = 4, 3
                        j.save()
                        k.save()
                else:
                    #(No nextitem, the whole pool of libraries finished instructing the current form, i.e. bound or not bound.)
                    nextlid = Library.objects.get(lid ="999999999").lid
                    nextlib = Library.objects.get(lid =nextlid)
                    j = ItemRecord.objects.get(sid =sid, lid =lid)
                    if j.status !=4:
                        j.status = 4
                        j.save()

            #Message data :
            subject = "eplouribousse : " + str(sid) + " / " + str(nextlid)
            host = str(request.get_host())
            message = _("Votre tour est venu d'instruire la fiche eplouribousse pour le ppn ") + str(sid) +\
            " : " + "https://" + host + "/add/" + str(sid) + '/' + str(nextlid)
            dest = nextlib.contact
            dest = [dest]
            exp = Library.objects.get(lid ="999999999").contact
            send_mail(subject, message, exp, dest, fail_silently=True, )

            do = instrtodo(request, lid)
            return do

        if z.is_valid() and y.flag ==False:
            info =_("N'oubliez pas de cocher avant de valider :")

    instrlist = Instruction.objects.filter(sid = sid).order_by('line')

    return render(request, 'epl/endinstruction.html', { 'ressource' : ress, \
    'library' : lib, 'instructions' : instrlist , 'librarylist' : \
    liblist, 'remedied_lib_list' : remliblist, 'sid' : sid, 'stage' : bd, 'info' : info, \
    'lid' : lid, 'checkform' : z, 'checkerform' : u, 'expected' : expected,})


def instrtodo(request, lid):

    if lid !="999999999":
        # Ressources whose the lid identified library has to deal with (status =1 or 3)
        l = ItemRecord.objects.filter(lid =lid).exclude(status =0).exclude(status =2).exclude(status =4).exclude(status =5).exclude(status =6)

    elif lid =="999999999":

        l = []

        for e in ItemRecord.objects.filter(status =2, rank =1):
            if len(ItemRecord.objects.filter(sid =e.sid, status =2)) == len(ItemRecord.objects.filter(sid =e.sid).exclude(rank =0)) and len(Instruction.objects.filter(sid =e.sid, name= "checker")) ==0:
                l.append(ItemRecord.objects.get(sid =e.sid, rank =1)) #yehh ... rank =1 that's the trick !

        for e in ItemRecord.objects.filter(status =4, rank =1):
            if len(ItemRecord.objects.filter(sid =e.sid, status =4)) == len(ItemRecord.objects.filter(sid =e.sid).exclude(rank =0)) and len(Instruction.objects.filter(sid =e.sid, name= "checker")) ==1:
                l.append(ItemRecord.objects.get(sid =e.sid, rank =1)) #yehh ... rank =1 that's the trick !

    size = len(l)

    #Getting library name :
    libname = Library.objects.get(lid =lid).name

    lidchecker = "999999999"

    return render(request, 'epl/instrtodo.html', { 'ressourcelist' : \
    l, 'lid' : lid, 'size' : size, 'name' : libname, 'lidchecker' : lidchecker, })


def instroneb(request, lid):

    if lid !="999999999":
        # Ressources whose the lid identified library has rank =1 and has to deal with bound elements (status =1)
        l = ItemRecord.objects.filter(lid =lid, rank =1).exclude(status =0).exclude(status =2).exclude(status =3).exclude(status =4).exclude(status =5).exclude(status =6)

    elif lid =="999999999":
        do = home(request)
        return do

    size = len(l)

    #Getting library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/instrtodobd1.html', { 'ressourcelist' : \
    l, 'lid' : lid, 'size' : size, 'name' : libname })

def instrotherb(request, lid):

    if lid !="999999999":
        # Ressources whose the lid identified library has rank !=1 and has to deal with bound elements (status =1)
        l = ItemRecord.objects.filter(lid =lid).exclude(rank =1).exclude(status =0).exclude(status =2).exclude(status =3).exclude(status =4).exclude(status =5).exclude(status =6)

    elif lid =="999999999":
        do = home(request)
        return do

    size = len(l)

    #Getting library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/instrtodobdnot1.html', { 'ressourcelist' : \
    l, 'lid' : lid, 'size' : size, 'name' : libname })

def instronenotb(request, lid):

    if lid !="999999999":
        # Ressources whose the lid identified library has rank =1 and has to deal with not bound elements (status =3)
        l = ItemRecord.objects.filter(lid =lid, rank =1).exclude(status =0).exclude(status =1).exclude(status =2).exclude(status =4).exclude(status =5).exclude(status =6)

    elif lid =="999999999":
        do = home(request)
        return do

    size = len(l)

    #Getting library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/instrtodonotbd1.html', { 'ressourcelist' : \
    l, 'lid' : lid, 'size' : size, 'name' : libname })

def instrothernotb(request, lid):

    if lid !="999999999":
        # Ressources whose the lid identified library has rank !=1 and has to deal with not bound elements (status =3)
        l = ItemRecord.objects.filter(lid =lid).exclude(rank =1).exclude(status =0).exclude(status =1).exclude(status =2).exclude(status =4).exclude(status =5).exclude(status =6)

    elif lid =="999999999":
        do = home(request)
        return do

    size = len(l)

    #Getting library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/instrtodonotbdnot1.html', { 'ressourcelist' : \
    l, 'lid' : lid, 'size' : size, 'name' : libname })


def arbitration(request, lid):

    #For the lid identified library, getting ressources whose at \
    #least 2 libraries, including the considered one, took rank =1 \
    #(even if other libraries have not yet taken rank)
    #or all libraries have taken rank, none of them the rank 1

    #Initialization of the ressources to arbitrate :
    resslista = []
    resslistb = []

    for e in ItemRecord.objects.filter(lid =lid, rank = 1, status =0):
        sid = e.sid
        if ItemRecord.objects.exclude(lid =lid).filter(sid =sid, rank = 1):
            resslista.append(e)

    for e in ItemRecord.objects.filter(lid =lid, status =0).exclude(rank =1).exclude(rank =0).exclude(rank =99):
        sid = e.sid
        if len(ItemRecord.objects.filter(sid =sid).exclude(lid =lid).filter(rank =1)) ==0 and len(ItemRecord.objects.filter(sid =sid).exclude(lid =lid).exclude(rank =0).exclude(rank =99)) !=0:
            resslistb.append(e)

    resslist = resslista + resslistb

    size = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/arbitration.html', { 'ressourcelist' : resslist\
    , 'size' : size, 'lid' : lid, 'name' : libname })


def tobeedited(request, lid):

    #For the lid identified library, getting ressources whose the resulting \
    #collection has been entirely completed and may consequently be edited.
    #Trick : These ressources have two instructions with name = 'checker' :

    l = ItemRecord.objects.filter(lid =lid).exclude(rank =0)

    #Initializing a list of ressources to edit :
    resslist = []

    for e in l:
        nl = Instruction.objects.filter(sid =e.sid)
        k = nl.filter(name = "checker")
        if len(k) ==2:
            resslist.append(e)

    size = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/to_edit_list.html', { 'ressourcelist' : \
    resslist, 'size' : size, 'name' : libname, 'lid' : lid })


def edition(request, sid, lid):

    #edition of the resulting collection for the considered sid and lid :

    #Control (edition only if yet possible)
    if len(Instruction.objects.filter(sid =sid, name ="checker")) ==2:
        #Getting an item record from which we can obtain ressource data :
        issn = ItemRecord.objects.get(sid =sid, lid =lid, status =5).issn
        title = ItemRecord.objects.get(sid =sid, lid =lid, status =5).title
        pubhist = ItemRecord.objects.get(sid =sid, lid =lid, status =5).pubhist


        #Getting instructions for the considered ressource :
        instrlist = Instruction.objects.filter(sid =sid).order_by('line')
        l = list(instrlist)

        #Getting library name for the considered library (will be used to
        #highlight the instruction of the considered library) :
        name = (Library.objects.get(lid =lid)).name

        mothercollection = Library.objects.get(lid =ItemRecord.objects.get(sid =sid, rank =1).lid).name

        return render(request, 'epl/edition.html',\
                 { 'instructionlist' : l, 'sid' : sid, 'issn' : issn, \
                 'title' : title, 'publicationhistory' : pubhist, 'lid' : lid, \
                 'name' : name, 'mother' :mothercollection,})

    else:
        do = notintime(request, sid, lid)
        return do


def indicators(request):

    #Indicators :

    #Number of rankings (exclusions included) :
    rkall = len(ItemRecord.objects.exclude(rank =99))

    #Number of rankings (exclusions excluded) :
    rkright = len(ItemRecord.objects.exclude(rank =99).exclude(rank =0))

    #Number of exclusions :
    exclus = len(ItemRecord.objects.filter(rank =0))

    #Exclusions details
    dict ={}
    for e in EXCLUSION_CHOICES:
        exclusion =str(e[0])
        value =len(ItemRecord.objects.filter(excl =e[0]))
        dict[exclusion] =value

    #Collections involved in arbitration for claiming 1st rank and number of serials concerned
    c1st, s1st =0,0
    for i in ItemRecord.objects.filter(rank =1, status =0):
        if len(ItemRecord.objects.filter(rank =1, sid =i.sid)) >1:
            c1st +=1
            s1st +=1/len(ItemRecord.objects.filter(rank =1, sid =i.sid))
    s1st = int(s1st)

    #Collections involved in arbitration for 1st rank not claimed by any of the libraries
    cnone, snone =0,0
    for i in ItemRecord.objects.exclude(rank =0).exclude(rank =1).exclude(rank =99):
        if len(ItemRecord.objects.filter(sid =i.sid).exclude(rank =0).exclude(rank =1).\
        exclude(rank =99)) >1 and len(ItemRecord.objects.filter(sid =i.sid)) ==\
        len(ItemRecord.objects.filter(sid =i.sid).exclude(rank =0).exclude(rank =1).exclude(rank =99)):
            cnone +=1
            snone +=1/len(ItemRecord.objects.filter(sid =i.sid).exclude(rank =0).exclude(rank =1).\
            exclude(rank =99))
    snone = int(snone)

    #Collections involved in arbitration for any of the two reasons and number of serials concerned
    ctotal = c1st + cnone
    stotal = s1st + snone

    #Number of collections :
    coll = len(ItemRecord.objects.all())

    #Number of potential candidates :
    cand =0
    for e in ItemRecord.objects.all():
        if len(ItemRecord.objects.filter(sid =e.sid)) >1:
            cand +=1/len(ItemRecord.objects.filter(sid =e.sid))
    cand = int(cand)

    #from which strict duplicates :
    dupl =0
    for e in ItemRecord.objects.all():
        if len(ItemRecord.objects.filter(sid =e.sid)) ==2:
            dupl +=1/len(ItemRecord.objects.filter(sid =e.sid))
    dupl = int(dupl)

    #triplets :
    tripl =0
    for e in ItemRecord.objects.all():
        if len(ItemRecord.objects.filter(sid =e.sid)) ==3:
            tripl +=1/len(ItemRecord.objects.filter(sid =e.sid))
    tripl = int(tripl)

    #quadruplets :
    qudrpl =0
    for e in ItemRecord.objects.all():
        if len(ItemRecord.objects.filter(sid =e.sid)) ==4:
            qudrpl +=1/len(ItemRecord.objects.filter(sid =e.sid))
    qudrpl = int(qudrpl)

    #Unicas :
    isol =0
    for e in ItemRecord.objects.all():
        if len(ItemRecord.objects.filter(sid =e.sid)) ==1:
            isol +=1/len(ItemRecord.objects.filter(sid =e.sid))
    isol = int(isol)

    #Number of descarded ressources for exclusion reason :
    discard =0
    for i in ItemRecord.objects.filter(rank =0):
        if len(ItemRecord.objects.filter(rank =0)) ==len(ItemRecord.objects.filter(sid =i.sid)):
            discard +=1/len(ItemRecord.objects.filter(rank =0))
    discard = int(discard)

    #Number of ressources whose instruction of bound elements may begin :
    bdmaybeg = len(ItemRecord.objects.filter(rank =1, status =1))

    #Number of ressources whose bound elements are currently instructed  :
    bdonway = len(ItemRecord.objects.filter(rank =1, status =2))

    #Number of ressources whose instruction of not bound elements may begin :
    notbdmaymeg = len(ItemRecord.objects.filter(rank =1, status =3))

    #Number of ressources whose not bound elements are currently instructed  :
    notbdonway = len(ItemRecord.objects.filter(rank =1, status =4))

    #Number of ressources completely instructed :
    fullinstr = len(ItemRecord.objects.filter(rank =1, status =5))

    #Number of failing sheets :
    fail = len(ItemRecord.objects.filter(status =6, rank =1))

    #Number of instructions :
    instr = len(Instruction.objects.all())

    return render(request, 'epl/indicators.html', {'rkall' : rkall, 'rkright' : \
    rkright, 'exclus' : exclus, 'bdmaybeg' : bdmaybeg, 'notbdmaymeg' : notbdmaymeg, 'fullinstr' : fullinstr, \
    'fail' : fail, 'instr' : instr, 'bdonway' : bdonway, 'notbdonway' : notbdonway, 'dict' : dict, 'c1st' : c1st, \
    's1st' : s1st, 'cnone' : cnone, 'snone' : snone, 'ctotal' : ctotal, 'stotal' : stotal, \
     'coll' : coll, 'cand' : cand, 'dupl' : dupl, 'isol' : isol, 'discard' : discard, \
     'tripl' : tripl, 'qudrpl' : qudrpl, })

def home(request):

    "Homepage"

    project = Project.objects.all().order_by('pk')[0].name

    #Feature input :
    i = Feature()
    f = FeatureForm(request.POST, instance =i)
    if f.is_valid():
        lid = Library.objects.get(name =i.libname).lid
        feature =i.feaname
        if not Feature.objects.filter(feaname = i.feaname, libname =i.libname):
            i.save() # This will be just for information (to know if
                     # some {library, feature} has not been used yet)
        if feature =='ranking':
            do = ranktotake(request, lid)
            return do
        elif feature =='arbitration':
            do = arbitration(request, lid)
            return do
        elif feature =='instrtodo':
            do = instrtodo(request, lid)
            return do
        elif feature =='edition':
            do = tobeedited(request, lid)
            return do

    return render(request, 'epl/home.html', {'form' : f, 'project' : project, })
