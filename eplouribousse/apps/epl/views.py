from django.shortcuts import render

from django.http import HttpResponse

from .models import *

from .forms import *

from django.core.mail import send_mail

from django.db.models.functions import Now

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch
from reportlab.platypus import Table, TableStyle

def pdfedition(request, sid, lid):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    filename = sid + '_' + lid + '.pdf'
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    libname = Library.objects.get(lid =lid).name
    title = ItemRecord.objects.get(sid =sid, lid =lid).title
    sid = ItemRecord.objects.get(sid =sid, lid =lid).sid
    issn = ItemRecord.objects.get(sid =sid, lid =lid).issn
    pubhist = ItemRecord.objects.get(sid =sid, lid =lid).pubhist
    instructions = Instruction.objects.filter(sid =sid).order_by('line')
    properinstructions = Instruction.objects.filter(sid =sid, name =libname)
    otherinstructions = Instruction.objects.filter(sid =sid, oname =libname)
    libinstructions = properinstructions.union(otherinstructions).order_by('line')
    controlbd = Instruction.objects.get(sid =sid, bound ='x', name ='admin').descr
    controlnotbd = Instruction.objects.get(sid =sid, bound =' ', name ='admin').descr
    mothercollection = Library.objects.get(lid =ItemRecord.objects.get(sid =sid, rank =1).lid).name

    p.drawString(50, 780, 'Bibliothèque')
    p.drawString(200, 780, ':')
    p.drawString(210, 780, libname)
    p.drawString(50, 760, 'Titre de la ressource')
    p.drawString(200, 760, ':')
    p.drawString(210, 760, title)
    p.drawString(50, 740, sid)
    p.drawString(130, 740, ' <--- ppn / issn ---> ')
    p.drawString(250, 740, issn)
    p.drawString(50, 720, 'Historique de la publication')
    p.drawString(200, 720, ':')
    p.drawString(210, 720, pubhist)
    p.drawString(50, 700, 'Collection mère')
    p.drawString(200, 700, ':')
    p.drawString(210, 700, mothercollection)

    data = [['#', 'bibliothèque', 'relié ?', 'bib. remédiée', 'segment', 'exception', 'dégradé' ]]
    Table(data, colWidths=None, rowHeights=None, style=None, splitByRow=1,repeatRows=0, repeatCols=0, rowSplitRange=None, spaceBefore=None, spaceAfter=None)
    for i in instructions:
        data.append([i.line, i.name, i.bound, i.oname, i.descr, i.exc, i.degr])
    t=Table(data)
    table_style = TableStyle([('ALIGN', (0, 0), (6, 0), 'CENTER'),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),])
    k =1
    for i in libinstructions:
        row = i.line
        k +=1 #Number of rows
        table_style.add('TEXTCOLOR', (0, row ), (6, row), colors.red)
    table_style.add('ALIGN', (0, 0), (0, k), 'CENTER')
    table_style.add('ALIGN', (2, 0), (2, k), 'CENTER')

    t.setStyle(table_style)

    width, height = A4
    t.wrapOn(p, width, height)
    t.drawOn(p, 0.5*inch, 4.0*inch)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
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


def takerank(request, sid, lid):

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


def notintime(request, sid, lid):

    lib = Library.objects.get(lid = lid)
    ress = ItemRecord.objects.get(sid =sid, lid =lid).title
    return render(request, 'epl/notintime.html', { 'library' : lib, 'title' : ress, 'lid' : lid, 'sid' : sid, })


def addinstr(request, sid, lid):

    #Control (addinstr only if it must be)
    try:
        if (len(list((Instruction.objects.filter(sid =sid)).filter(name ='admin'))) ==2 \
        or (len(list((Instruction.objects.filter(sid =sid)).filter(name ='admin'))) ==0 \
        and not ItemRecord.objects.get(sid = sid, lid =lid).status ==1) \
        or ((len(list((Instruction.objects.filter(sid =sid)).filter(name ='admin'))) ==1 \
        and not ItemRecord.objects.get(sid = sid, lid =lid).status ==3))):
            do = notintime(request, sid, lid)
            return do
    except:
        z =1 #This is just to continue

    #Ressource data :
    itemlist = ItemRecord.objects.filter(sid = sid).exclude(rank =0).order_by("rank", 'pk')
    ress = itemlist[0]

    #Library data :
    lib = Library.objects.get(lid = lid)

    # Library list ordered by 'rank' (except "admin" which must be the last one)
    # to get from the precedent item list above :
    liblist = []
    for e in itemlist:
        liblist.append(Library.objects.get(lid = e.lid))
    liblist.append(Library.objects.get(name = 'admin'))

    #Remedied library list :
    remliblist = []
    for e in itemlist:
        remliblist.append(Library.objects.get(lid = e.lid))
    if (Library.objects.get(lid =lid)).name != 'admin':
        remliblist.remove(Library.objects.get(name = lib.name))

    #Info :
    info =""

    #Stage (bound or not bound) :
    if len(list((Instruction.objects.filter(sid =sid)).filter(name ='admin'))) ==0:
        bd ='reliés'
    elif len(list((Instruction.objects.filter(sid =sid)).filter(name ='admin'))) ==1:
        bd ='non reliés'

    if lid =="999999999":
        do = endinstr(request, sid, lid)
        return do

    else:
        #Instruction form instanciation and validation :
        i = Instruction(sid = sid, name = lib.name)
        f = InstructionForm(request.POST, instance =i)
        q = "x"
        if f.is_valid():
            i.line +=1
            if len(list((Instruction.objects.filter(sid =sid)).\
            filter(name ='admin'))):
                q =" "
            else:
                q ="x"
            i.bound =q
            #A line may only be registered once :
            if not len(Instruction.objects.filter(sid =sid, name =lib.name, bound =i.bound, oname =i.oname, descr =i.descr, exc =i.exc, degr =i.degr)):
                f.save()
            else:
                info = "Vous ne pouvez pas valider deux fois la même ligne d'instruction."

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


def delinstr(request, sid, lid):

    #Ressource data :
    itemlist = ItemRecord.objects.filter(sid = sid).exclude(rank =0).order_by("rank", 'pk')
    ress = itemlist[0]

    #Library data :
    lib = Library.objects.get(lid = lid)

    # Library list ordered by 'rank' (except "admin" which must be the last one)
    # to get from the precedent item list above :
    liblist = []
    for e in itemlist:
        liblist.append(Library.objects.get(lid = e.lid))
    liblist.append(Library.objects.get(name = 'admin'))

    #Remedied library list :
    remliblist = []
    for e in itemlist:
        remliblist.append(Library.objects.get(lid = e.lid))
    if (Library.objects.get(lid =lid)).name != 'admin':
        remliblist.remove(Library.objects.get(name = lib.name))

    #Info :
    info =""

    #Stage (bound or not bound) :
    if len(list((Instruction.objects.filter(sid =sid)).filter(name ='admin'))) ==0:
        bd ='reliés'
        # ress_stage ='reliés'
        expected = "x"
    elif len(list((Instruction.objects.filter(sid =sid)).filter(name ='admin'))) ==1:
        bd ='non reliés'
        # ress_stage ='non reliés'
        expected = " "
    else:   # (==2)
        bd = "XXXXX (instructions terminées)"

    answer = ""

    i = Instruction(sid = sid, name = lib.name)
    f = InstructionForm(request.POST, instance=i) # for deletion of an instruction line
    if f.is_valid():
        try:
            j = Instruction.objects.get(sid =sid, bound = expected, name =lib.name, line =i.line)
            j.delete()
        except:
            answer = " <=== Suppression non permise (vérifiez les conditions requises) "

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
    liblist.append(Library.objects.get(name = 'admin'))

    return render(request, 'epl/delinstruction.html', { 'ressource' : ress, \
    'library' : lib, 'instructions' : instrlist , 'form' : f, 'librarylist' : \
    liblist, 'remedied_lib_list' : remliblist, 'sid' : sid, 'stage' : bd, 'info' : info, \
    'lid' : lid, 'expected' : expected, 'answer' : answer,})


def endinstr(request, sid, lid):

    #Ressource data :
    itemlist = ItemRecord.objects.filter(sid = sid).exclude(rank =0).order_by("rank", 'pk')
    ress = itemlist[0]

    #Library data :
    lib = Library.objects.get(lid = lid)

    # Library list ordered by 'rank' (except "admin" which must be the last one)
    # to get from the precedent item list above :
    liblist = []
    for e in itemlist:
        liblist.append(Library.objects.get(lid = e.lid))
    liblist.append(Library.objects.get(name = 'admin'))

    #Remedied library list :
    remliblist = []
    for e in itemlist:
        remliblist.append(Library.objects.get(lid = e.lid))
    if (Library.objects.get(lid =lid)).name != 'admin':
        remliblist.remove(Library.objects.get(name = lib.name))

    #Info :
    info =""

    #Stage (bound or not bound) :
    if len(list((Instruction.objects.filter(sid =sid)).filter(name ='admin'))) ==0:
        bd ='reliés'
        # ress_stage ='reliés'
        expected = "x"
    elif len(list((Instruction.objects.filter(sid =sid)).filter(name ='admin'))) ==1:
        bd ='non reliés'
        # ress_stage ='non reliés'
        expected = " "
    else:   # (==2)
        bd = "XXXXX (instructions terminées)"
        expected = "ni relié, ni non reliés"

    answer = ""

    y = Flag()
    z = CheckForm(request.POST, instance =y)

    t = Check()
    u = AdminCheckForm(request.POST or None, instance =t)


    if lid =="999999999":
        nextlib = liblist[0]
        nextlid = nextlib.lid
        if u.is_valid() and t.checkin =="Visa":
            admininstruction = Instruction(sid =sid, name ="admin")
            admininstruction.line =0
            if len(Instruction.objects.filter(sid =sid, name ='admin')) ==0:
                admininstruction.bound ="x"
            if len(Instruction.objects.filter(sid =sid, name ='admin')) ==1:
                admininstruction.bound =" "
            admininstruction.descr =Now()
            admininstruction.save()

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
            if len(Instruction.objects.filter(sid =sid, name ='admin')) ==1:
                if j.status !=3:
                    j.status = 3
                    j.save()
                    #Message data :
                    subject = "eplouribousse : " + str(sid) + " / " + str(nextlid)
                    host = str(request.get_host())
                    message = "Votre tour est venu d'instruire la fiche eplouribousse pour le ppn " + str(sid) +\
                    " : " + "https://" + host + "/epl/addinstruction/" + str(sid) + '/' + str(nextlid)
                    dest = nextlib.contact
                    dest = [dest]
                    exp = Library.objects.get(lid ="999999999").contact
                    send_mail(subject, message, exp, dest, fail_silently=True, )
		            
            if len(Instruction.objects.filter(sid =sid, name ='admin')) ==2:
                for e in ItemRecord.objects.filter(status =4):
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
            message = "Le statut des enregistrements est passé à 6 pour les enregistrements des bibliothèques participant à la résultante de la ressoucre citée en objet ; une intervention dans base est attendue de votre part. Merci !"
            destprov = BddAdmin.objects.all()
            dest =[]
            for d in destprov:
                dest.append(d.contact)
            exp = Library.objects.get(lid ="999999999").contact
            send_mail(
                subject,
                message,
                exp,
                dest,
                fail_silently=True,
            )

            do = instrtodo(request, lid)
            return do

    else: #lid !="999999999"
        if ItemRecord.objects.filter(sid =sid, status =0).exclude(lid =lid).exclude(rank =0).order_by('rank', 'pk').exists():
            nextlid = ItemRecord.objects.filter(sid =sid, status =0).exclude(lid =lid).exclude(rank =0).order_by('rank', 'pk')[0].lid
            nextlib = Library.objects.get(lid =nextlid)
        else:
            nextlid = Library.objects.get(lid ="999999999").lid
            nextlib = Library.objects.get(lid =nextlid)
        if z.is_valid() and y.flag ==True:
            if len(Instruction.objects.filter(sid =sid, name ='admin')) ==0:
                if ItemRecord.objects.filter(sid =sid, status =0).exclude(lid =lid).exclude(rank =0).order_by('rank', 'pk').exists():
                    nextitem = ItemRecord.objects.filter(sid =sid, status =0).exclude(lid =lid).exclude(rank =0).order_by('rank', 'pk')[0]
                    nextlid = nextitem.lid
                    j, k = ItemRecord.objects.get(sid =sid, lid =lid), ItemRecord.objects.get(sid =sid, lid =nextlid)
                    if j.status !=2:
                        j.status, k.status = 2, 1
                        j.save()
                        k.save()
                else:
                    #(No nextitem, the whole pool of libraries finished instructing the current form, i.e. bound or not bound.)
                    j = ItemRecord.objects.get(sid =sid, lid =lid)
                    if j.status !=2:
                        j.status = 2
                        j.save()

            elif len(Instruction.objects.filter(sid =sid, name ='admin')) ==1:
                if ItemRecord.objects.filter(sid =sid, status =2).exclude(lid =lid).exclude(rank =0).order_by('rank', 'pk').exists():
                    nextitem = ItemRecord.objects.filter(sid =sid, status =2).exclude(lid =lid).exclude(rank =0).order_by('rank', 'pk')[0]
                    nextlid = nextitem.lid
                    j, k = ItemRecord.objects.get(sid =sid, lid =lid), ItemRecord.objects.get(sid =sid, lid =nextlid)
                    if j.status !=4:
                        j.status, k.status = 4, 3
                        j.save()
                        k.save()
                else:
                    #(No nextitem, the whole pool of libraries finished instructing the current form, i.e. bound or not bound.)
                    j = ItemRecord.objects.get(sid =sid, lid =lid)
                    if j.status !=4:
                        j.status = 4
                        j.save()

            #Message data :
            subject = "eplouribousse : " + str(sid) + " / " + str(nextlid)
            host = str(request.get_host())
            message = "Votre tour est venu d'instruire la fiche eplouribousse pour le ppn " + str(sid) +\
            " : " + "https://" + host + "/epl/addinstruction/" + str(sid) + '/' + str(nextlid)
            dest = nextlib.contact
            dest = [dest]
            exp = Library.objects.get(lid ="999999999").contact
            send_mail(
                subject,
                message,
                exp,
                dest,
                fail_silently=True,
            )

            do = instrtodo(request, lid)
            return do

        if z.is_valid() and y.flag ==False:
            info ="N'avez-vous pas oublié de cocher ?"

    instrlist = Instruction.objects.filter(sid = sid).order_by('line')

    return render(request, 'epl/endinstruction.html', { 'ressource' : ress, \
    'library' : lib, 'instructions' : instrlist , 'librarylist' : \
    liblist, 'remedied_lib_list' : remliblist, 'sid' : sid, 'stage' : bd, 'info' : info, \
    'lid' : lid, 'checkform' : z, 'admincheckform' : u, 'expected' : expected,})


def instrtodo(request, lid):

    if lid !="999999999":
        # Ressources whose the lid identified library has to deal with (status =1 or 3)
        l = ItemRecord.objects.filter(lid =lid).exclude(status =0).exclude(status =2).exclude(status =4).exclude(status =5).exclude(status =6)

    elif lid =="999999999":

        l = []

        for e in ItemRecord.objects.filter(status =2, rank =1):
            if len(ItemRecord.objects.filter(sid =e.sid, status =2)) == len(ItemRecord.objects.filter(sid =e.sid).exclude(rank =0)) and len(Instruction.objects.filter(sid =e.sid, name= "admin")) ==0:
                l.append(ItemRecord.objects.get(sid =e.sid, rank =1)) #yehh ... rank =1 that's the trick !

        for e in ItemRecord.objects.filter(status =4, rank =1):
            if len(ItemRecord.objects.filter(sid =e.sid, status =4)) == len(ItemRecord.objects.filter(sid =e.sid).exclude(rank =0)) and len(Instruction.objects.filter(sid =e.sid, name= "admin")) ==1:
                l.append(ItemRecord.objects.get(sid =e.sid, rank =1)) #yehh ... rank =1 that's the trick !

    size = len(l)

    #Getting library name :
    libname = Library.objects.get(lid =lid).name

    lidadmin = "999999999"

    return render(request, 'epl/instrtodo.html', { 'ressourcelist' : \
    l, 'lid' : lid, 'size' : size, 'name' : libname, 'lidadmin' : lidadmin, })


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
    #Trick : These ressources have two instructions with name = 'admin' :

    l = ItemRecord.objects.filter(lid =lid)

    #Initializing a list of ressources to edit :
    resslist = []

    for e in l:
        nl = Instruction.objects.filter(sid =e.sid)
        k = nl.filter(name = "admin")
        if len(k) ==2:
            resslist.append(e)

    size = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/to_edit_list.html', { 'ressourcelist' : \
    resslist, 'size' : size, 'name' : libname, 'lid' : lid })


def edition(request, sid, lid):

    #edition of the resulting collection for the considered sid and lid :

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


def indicators(request):

    #Indicators :

    #Number of rankings (exclusions included) :
    rkall = len(ItemRecord.objects.exclude(rank =99))

    #Number of rankings (exclusions excluded) :
    rkright = len(ItemRecord.objects.exclude(rank =99).exclude(rank =0))

    #Number of exclusions :
    exclus = len(ItemRecord.objects.filter(rank =0))

    #Number of exclusions by 'Abonnement en cours' :
    currsubs = len(ItemRecord.objects.filter(rank =0, excl ='Abonnement en cours'))

    #Number of exclusions by 'Dépôt légal' :
    legald = len(ItemRecord.objects.filter(rank =0, excl ='Dépôt légal'))

    #Number of exclusions by 'Entièrement patrimonial' :
    fullpat = len(ItemRecord.objects.filter(rank =0, excl ='Entièrement patrimonial'))

    #Number of exclusions by 'Fait partie d'un PCP (Plan de conservation partagée)' :
    sharedpreserv = len(ItemRecord.objects.filter(rank =0, excl ="Fait partie d'un plan de conservation partagée"))

    #Number of exclusions by 'Autre' :
    other = len(ItemRecord.objects.filter(rank =0, excl ="Autre (Commenter)"))

    #Number of ressources whose instruction may begin :
    maybeg = len(ItemRecord.objects.filter(rank =1, status =1))

    #Number of ressources whose bound elements have been completely instructed :
    boundinstr = len(ItemRecord.objects.filter(rank =1, status =3))

    #Number of ressources completely instructed :
    fullinstr = len(ItemRecord.objects.filter(rank =1, status =5))

    #Number of failing sheets :
    fail = len(ItemRecord.objects.filter(status =6, rank =1))

    #Number of instructions :
    instr = len(Instruction.objects.all())

    return render(request, 'epl/indicators.html', {'rkall' : rkall, 'rkright' : \
    rkright, 'exclus' : exclus, 'currsubs' : currsubs, 'legald' : legald, \
    'fullpat' : fullpat, 'sharedpreserv' : sharedpreserv, 'other' : other, \
    'maybeg' : maybeg, 'boundinstr' : boundinstr, 'fullinstr' : fullinstr, \
    'fail' : fail, 'instr' : instr,})


def home(request):

    "Homepage"

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

    return render(request, 'epl/home.html', {'form' : f, })
