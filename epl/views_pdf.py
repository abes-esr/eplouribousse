from django.shortcuts import render

from django.http import HttpResponse

from .models import *

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from django.core.files.storage import FileSystemStorage

from django.utils.translation import ugettext as _

from .decorators import edmode4, edmode5, edmode7

styles = getSampleStyleSheet()

@edmode5
def pdfedition(request, bdd, sid, lid):

    project = Project.objects.using(bdd).all().order_by('pk')[0].name

    filename = bdd + '_' + sid + '_' + lid + '.pdf'
    dirfile = "/tmp/" + filename

    doc = SimpleDocTemplate(filename="{}".format(dirfile), pagesize=landscape(A4))
    elements = []

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    libname = Library.objects.using(bdd).get(lid =lid).name
    title = ItemRecord.objects.using(bdd).get(sid =sid, lid =lid).title
    sid = ItemRecord.objects.using(bdd).get(sid =sid, lid =lid).sid
    cn = ItemRecord.objects.using(bdd).get(sid =sid, lid =lid).cn
    issn = ItemRecord.objects.using(bdd).get(sid =sid, lid =lid).issn
    pubhist = ItemRecord.objects.using(bdd).get(sid =sid, lid =lid).pubhist
    instructions = Instruction.objects.using(bdd).filter(sid =sid).order_by('line')
    properinstructions = Instruction.objects.using(bdd).filter(sid =sid, name =libname)
    otherinstructions = Instruction.objects.using(bdd).filter(sid =sid, oname =libname)
    libinstructions = properinstructions.union(otherinstructions).order_by('line')
    controlbd = Instruction.objects.using(bdd).get(sid =sid, bound ='x', name ='checker').descr
    controlnotbd = Instruction.objects.using(bdd).exclude(bound ='x').get(sid =sid, name ='checker').descr
    mothercollection = Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =sid, rank =1).lid).name

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

    datacoll.append([_("rang"), _("bibliothèque"), _("info"), _("commentaire")])

    for e in ItemRecord.objects.using(bdd).filter(sid =sid).order_by("rank"):
        if e.rank ==1:
            datacoll.append([e.rank, Library.objects.using(bdd).get(lid =e.lid).name, _("collection mère"), e.comm])
        elif e.rank ==0:
            datacoll.append([e.rank, Library.objects.using(bdd).get(lid =e.lid).name, e.excl, e.comm])
        else:
            datacoll.append([e.rank, Library.objects.using(bdd).get(lid =e.lid).name, _("a pris part"), e.comm])

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

@edmode4
def edallpdf(request, bdd, lid):

    project = Project.objects.using(bdd).all().order_by('pk')[0].name

    filename = bdd + '_' + lid + '.pdf'
    dirfile = "/tmp/" + filename

    libname = Library.objects.using(bdd).get(lid =lid).name

    doc = SimpleDocTemplate(filename="{}".format(dirfile), pagesize=landscape(A4))
    elements = []

    #For the lid identified library, getting ressources whose the resulting \
    #collection has been entirely completed and may consequently be edited.
    #Trick : These ressources have two instructions with name = 'checker' :
    #This is like "tobeedited" (see below)

    l = ItemRecord.objects.using(bdd).filter(lid =lid).exclude(rank =0)

    #Initializing a list of ressources to edit :
    resslist = []

    for e in l:
        nl = Instruction.objects.using(bdd).filter(sid =e.sid)
        k = nl.filter(name = "checker")
        if len(k) ==2:
            resslist.append(e)

    for r in resslist:

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        title = ItemRecord.objects.using(bdd).get(sid =r.sid, lid =lid).title
        sid = ItemRecord.objects.using(bdd).get(sid =r.sid, lid =lid).sid
        cn = ItemRecord.objects.using(bdd).get(sid =sid, lid =lid).cn
        issn = ItemRecord.objects.using(bdd).get(sid =r.sid, lid =lid).issn
        pubhist = ItemRecord.objects.using(bdd).get(sid =r.sid, lid =lid).pubhist
        instructions = Instruction.objects.using(bdd).filter(sid =r.sid).order_by('line')
        properinstructions = Instruction.objects.using(bdd).filter(sid =r.sid, name =libname)
        otherinstructions = Instruction.objects.using(bdd).filter(sid =r.sid, oname =libname)
        libinstructions = properinstructions.union(otherinstructions).order_by('line')
        controlbd = Instruction.objects.using(bdd).get(sid =r.sid, bound ='x', name ='checker').descr
        controlnotbd = Instruction.objects.using(bdd).exclude(bound ='x').get(sid =r.sid, name ='checker').descr
        mothercollection = Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =r.sid, rank =1).lid).name

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

        datacoll.append([_("rang"), _("bibliothèque"), _("info"), _("commentaire")])

        for e in ItemRecord.objects.using(bdd).filter(sid =sid).order_by("rank"):
            if e.rank ==1:
                datacoll.append([e.rank, Library.objects.using(bdd).get(lid =e.lid).name, _("collection mère"), e.comm])
            elif e.rank ==0:
                datacoll.append([e.rank, Library.objects.using(bdd).get(lid =e.lid).name, e.excl, e.comm])
            else:
                datacoll.append([e.rank, Library.objects.using(bdd).get(lid =e.lid).name, _("a pris part"), e.comm])

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

@edmode4
def motherpdf(request, bdd, lid):

    project = Project.objects.using(bdd).all().order_by('pk')[0].name

    filename = bdd + '_' + lid + '.pdf'
    dirfile = "/tmp/" + filename

    libname = Library.objects.using(bdd).get(lid =lid).name

    doc = SimpleDocTemplate(filename="{}".format(dirfile), pagesize=landscape(A4))
    elements = []

    #For the lid identified library, getting ressources whose the resulting \
    #collection has been entirely completed and may consequently be edited.
    #Trick : These ressources have two instructions with name = 'checker' :
    #This is like "tobeedited" (see below) Mother collection (rank =1)

    l = ItemRecord.objects.using(bdd).filter(lid =lid, rank =1)

    #Initializing a list of ressources to edit :
    resslist = []

    for e in l:
        nl = Instruction.objects.using(bdd).filter(sid =e.sid)
        k = nl.filter(name = "checker")
        if len(k) ==2:
            resslist.append(e)

    for r in resslist:

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        title = ItemRecord.objects.using(bdd).get(sid =r.sid, lid =lid).title
        sid = ItemRecord.objects.using(bdd).get(sid =r.sid, lid =lid).sid
        cn = ItemRecord.objects.using(bdd).get(sid =sid, lid =lid).cn
        issn = ItemRecord.objects.using(bdd).get(sid =r.sid, lid =lid).issn
        pubhist = ItemRecord.objects.using(bdd).get(sid =r.sid, lid =lid).pubhist
        instructions = Instruction.objects.using(bdd).filter(sid =r.sid).order_by('line')
        properinstructions = Instruction.objects.using(bdd).filter(sid =r.sid, name =libname)
        otherinstructions = Instruction.objects.using(bdd).filter(sid =r.sid, oname =libname)
        libinstructions = properinstructions.union(otherinstructions).order_by('line')
        controlbd = Instruction.objects.using(bdd).get(sid =r.sid, bound ='x', name ='checker').descr
        controlnotbd = Instruction.objects.using(bdd).exclude(bound ='x').get(sid =r.sid, name ='checker').descr
        mothercollection = Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =r.sid, rank =1).lid).name

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

        datacoll.append([_("rang"), _("bibliothèque"), _("info"), _("commentaire")])

        for e in ItemRecord.objects.using(bdd).filter(sid =sid).order_by("rank"):
            if e.rank ==1:
                datacoll.append([e.rank, Library.objects.using(bdd).get(lid =e.lid).name, _("collection mère"), e.comm])
            elif e.rank ==0:
                datacoll.append([e.rank, Library.objects.using(bdd).get(lid =e.lid).name, e.excl, e.comm])
            else:
                datacoll.append([e.rank, Library.objects.using(bdd).get(lid =e.lid).name, _("a pris part"), e.comm])

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

@edmode4
def notmotherpdf(request, bdd, lid):

    project = Project.objects.using(bdd).all().order_by('pk')[0].name

    filename = bdd + '_' + lid + '.pdf'
    dirfile = "/tmp/" + filename

    libname = Library.objects.using(bdd).get(lid =lid).name

    doc = SimpleDocTemplate(filename="{}".format(dirfile), pagesize=landscape(A4))
    elements = []

    #For the lid identified library, getting ressources whose the resulting \
    #collection has been entirely completed and may consequently be edited.
    #Trick : These ressources have two instructions with name = 'checker' :
    #This is like "tobeedited" (see below) Not mother collection (rank not 1)

    l = ItemRecord.objects.using(bdd).filter(lid =lid).exclude(rank =1).exclude(rank =0).exclude(rank =99)

    #Initializing a list of ressources to edit :
    resslist = []

    for e in l:
        nl = Instruction.objects.using(bdd).filter(sid =e.sid)
        k = nl.filter(name = "checker")
        if len(k) ==2:
            resslist.append(e)

    for r in resslist:

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        title = ItemRecord.objects.using(bdd).get(sid =r.sid, lid =lid).title
        sid = ItemRecord.objects.using(bdd).get(sid =r.sid, lid =lid).sid
        cn = ItemRecord.objects.using(bdd).get(sid =sid, lid =lid).cn
        issn = ItemRecord.objects.using(bdd).get(sid =r.sid, lid =lid).issn
        pubhist = ItemRecord.objects.using(bdd).get(sid =r.sid, lid =lid).pubhist
        instructions = Instruction.objects.using(bdd).filter(sid =r.sid).order_by('line')
        properinstructions = Instruction.objects.using(bdd).filter(sid =r.sid, name =libname)
        otherinstructions = Instruction.objects.using(bdd).filter(sid =r.sid, oname =libname)
        libinstructions = properinstructions.union(otherinstructions).order_by('line')
        controlbd = Instruction.objects.using(bdd).get(sid =r.sid, bound ='x', name ='checker').descr
        controlnotbd = Instruction.objects.using(bdd).exclude(bound ='x').get(sid =r.sid, name ='checker').descr
        mothercollection = Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =r.sid, rank =1).lid).name

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

        datacoll.append([_("rang"), _("bibliothèque"), _("info"), _("commentaire")])

        for e in ItemRecord.objects.using(bdd).filter(sid =sid).order_by("rank"):
            if e.rank ==1:
                datacoll.append([e.rank, Library.objects.using(bdd).get(lid =e.lid).name, _("collection mère"), e.comm])
            elif e.rank ==0:
                datacoll.append([e.rank, Library.objects.using(bdd).get(lid =e.lid).name, e.excl, e.comm])
            else:
                datacoll.append([e.rank, Library.objects.using(bdd).get(lid =e.lid).name, _("a pris part"), e.comm])

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

@edmode7
def xmotherpdf(request, bdd, lid, xlid):

    project = Project.objects.using(bdd).all().order_by('pk')[0].name

    filename = bdd + '_' + lid + '.pdf'
    dirfile = "/tmp/" + filename

    libname = Library.objects.using(bdd).get(lid =lid).name

    doc = SimpleDocTemplate(filename="{}".format(dirfile), pagesize=landscape(A4))
    elements = []

    #For the lid identified library, getting ressources whose the resulting \
    #collection has been entirely completed and may consequently be edited.
    #Trick : These ressources have two instructions with name = 'checker' :
    #This is like "tobeedited" (see below)

    l = ItemRecord.objects.using(bdd).filter(lid =lid, rank =1)

    #Initializing a list of ressources to edit :
    resslist = []

    for e in l:
        nl = Instruction.objects.using(bdd).filter(sid =e.sid)
        kd = nl.filter(name = "checker")
        if len(kd) ==2 and Instruction.objects.using(bdd).filter(sid =e.sid, name =Library.objects.using(bdd).get(lid =xlid)):
            resslist.append(e)

    for r in resslist:

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        title = ItemRecord.objects.using(bdd).get(sid =r.sid, lid =lid).title
        sid = ItemRecord.objects.using(bdd).get(sid =r.sid, lid =lid).sid
        cn = ItemRecord.objects.using(bdd).get(sid =sid, lid =lid).cn
        issn = ItemRecord.objects.using(bdd).get(sid =r.sid, lid =lid).issn
        pubhist = ItemRecord.objects.using(bdd).get(sid =r.sid, lid =lid).pubhist
        instructions = Instruction.objects.using(bdd).filter(sid =r.sid).order_by('line')
        properinstructions = Instruction.objects.using(bdd).filter(sid =r.sid, name =libname)
        otherinstructions = Instruction.objects.using(bdd).filter(sid =r.sid, oname =libname)
        libinstructions = properinstructions.union(otherinstructions).order_by('line')
        controlbd = Instruction.objects.using(bdd).get(sid =r.sid, bound ='x', name ='checker').descr
        controlnotbd = Instruction.objects.using(bdd).exclude(bound ='x').get(sid =r.sid, name ='checker').descr
        mothercollection = Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =r.sid, rank =1).lid).name

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

        datacoll.append([_("rang"), _("bibliothèque"), _("info"), _("commentaire")])

        for e in ItemRecord.objects.using(bdd).filter(sid =sid).order_by("rank"):
            if e.rank ==1:
                datacoll.append([e.rank, Library.objects.using(bdd).get(lid =e.lid).name, _("collection mère"), e.comm])
            elif e.rank ==0:
                datacoll.append([e.rank, Library.objects.using(bdd).get(lid =e.lid).name, e.excl, e.comm])
            else:
                datacoll.append([e.rank, Library.objects.using(bdd).get(lid =e.lid).name, _("a pris part"), e.comm])

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

@edmode7
def xnotmotherpdf(request, bdd, lid, xlid):

    project = Project.objects.using(bdd).all().order_by('pk')[0].name

    filename = bdd + '_' + lid + '.pdf'
    dirfile = "/tmp/" + filename

    libname = Library.objects.using(bdd).get(lid =lid).name

    doc = SimpleDocTemplate(filename="{}".format(dirfile), pagesize=landscape(A4))
    elements = []

    #For the lid identified library, getting ressources whose the resulting \
    #collection has been entirely completed and may consequently be edited.
    #Trick : These ressources have two instructions with name = 'checker' :
    #This is like "tobeedited" (see below)

    l = ItemRecord.objects.using(bdd).filter(lid =lid).exclude(rank =1).exclude(rank =0)

    #Initializing a list of ressources to edit :
    resslist = []

    for e in l:
        nl = Instruction.objects.using(bdd).filter(sid =e.sid)
        kd = nl.filter(name = "checker")
        if len(kd) ==2 and Instruction.objects.using(bdd).filter(sid =e.sid, name =Library.objects.using(bdd).get(lid =xlid)):
            resslist.append(e)

    for r in resslist:

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        title = ItemRecord.objects.using(bdd).get(sid =r.sid, lid =lid).title
        sid = ItemRecord.objects.using(bdd).get(sid =r.sid, lid =lid).sid
        cn = ItemRecord.objects.using(bdd).get(sid =sid, lid =lid).cn
        issn = ItemRecord.objects.using(bdd).get(sid =r.sid, lid =lid).issn
        pubhist = ItemRecord.objects.using(bdd).get(sid =r.sid, lid =lid).pubhist
        instructions = Instruction.objects.using(bdd).filter(sid =r.sid).order_by('line')
        properinstructions = Instruction.objects.using(bdd).filter(sid =r.sid, name =libname)
        otherinstructions = Instruction.objects.using(bdd).filter(sid =r.sid, oname =libname)
        libinstructions = properinstructions.union(otherinstructions).order_by('line')
        controlbd = Instruction.objects.using(bdd).get(sid =r.sid, bound ='x', name ='checker').descr
        controlnotbd = Instruction.objects.using(bdd).exclude(bound ='x').get(sid =r.sid, name ='checker').descr
        mothercollection = Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =r.sid, rank =1).lid).name

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

        datacoll.append([_("rang"), _("bibliothèque"), _("info"), _("commentaire")])

        for e in ItemRecord.objects.using(bdd).filter(sid =sid).order_by("rank"):
            if e.rank ==1:
                datacoll.append([e.rank, Library.objects.using(bdd).get(lid =e.lid).name, _("collection mère"), e.comm])
            elif e.rank ==0:
                datacoll.append([e.rank, Library.objects.using(bdd).get(lid =e.lid).name, e.excl, e.comm])
            else:
                datacoll.append([e.rank, Library.objects.using(bdd).get(lid =e.lid).name, _("a pris part"), e.comm])

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
