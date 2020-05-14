epl_version ="Version 1.2.6 (Chrodechilde)"
date_version ="May 12, 2020"
# Mise au niveau de :
# epl_version ="Version 1.3.6 beta (~Ultrogothe)"
# date_version ="May 12, 2020"


from django.shortcuts import render

from .models import *

from .forms import *

from django.core.mail import send_mail

from django.db.models.functions import Now

from django.contrib.auth.decorators import login_required

from django.utils.translation import ugettext as _

from django.contrib.auth.models import User

from django.contrib.auth import logout

idfeature =0 #identification de la fonctionnalité (0 pour accueil, 1 pour positionnement, 2 pour arbitrage, 3 pour instr et 4 pour ed)
idview =1 #identification des fonctions de listes (voir les vues correspondantes)
dil =Library.objects.exclude(lid ="999999999")[0].lid # comme lid
dilx =Library.objects.exclude(lid ="999999999")[1].lid # comme xlid
tes_lloc =Library.objects.all() # comme coll_set
lastrked =None

try:
    replymail =ReplyMail.objects.all().order_by('pk')[0].sendermail
except:
    replymail =BddAdmin.objects.all().order_by('pk')[0].contact


def logstatus(request):
    if request.user.is_authenticated:
        k = request.user.get_username()
    else:
        k =0
    return k


def home(request):

    k = logstatus(request)
    version =epl_version

    "Homepage"

    project = Project.objects.all().order_by('pk')[0].name

    #Feature input :
    i = Feature()
    form = FeatureForm(request.POST, instance =i)
    if form.is_valid():
        lid = Library.objects.get(name =i.libname).lid
        feature =i.feaname
        # if not Feature.objects.filter(feaname = i.feaname, libname =i.libname):
        i.save()
        if lid =="999999999":
            if feature =='instrtodo':
                return instrtodo(request, lid)
            else:
                return checkinstr(request)
        else:
            if feature =='ranking':
                return ranktotake(request, lid)
            elif feature =='arbitration':
                return arbitration(request, lid)
            elif feature =='instrtodo':
                return instrtodo(request, lid)
            elif feature =='edition':
                return tobeedited(request, lid)

    return render(request, 'epl/home.html', locals())


def about(request):
    version =epl_version
    date =date_version
    return render(request, 'epl/about.html', locals())


def router(request):

    if idfeature ==0:
        return home(request)
    if idfeature ==1:
        if idview ==0:
            return ranktotake(request, dil)
        if idview ==1:
            return xranktotake(request, dil, dilx)
        # if idview ==2:
        #     return modifranklist(request, dil)
        # Le choix de supprimer le bloc ci-dessus tient à ce que les modifications de rang sont normalement réalisés à l'unité ;
        # il est donc plus intéressant de revenir à la dernière liste de positionnement. En conséquence la modification des varables
        # globales a été annulée dans la vue modifranklist(request, dil)
    if idfeature ==2:
        if idview ==0:
            return arbitration(request, dil)
        if idview ==1:
            return xarbitration(request, dil, dilx)
        if idview ==2:
            return x1arb(request, dil, dilx)
        if idview ==3:
            return x0arb(request, dil, dilx)
        if idview ==4:
            return arbrk1(request, dil)
        if idview ==5:
            return arbnork1(request, dil)
    if idfeature ==3:
        if idview ==0:
            return instrtodo(request, dil)
        if idview ==1:
            return xinstrlist(request, dil, dilx)
        if idview ==2:
            return xckbd(request, tes_lloc)
        if idview ==3:
            return xcknbd(request, tes_lloc)
        if idview ==4:
            return xckall(request, tes_lloc)
    if idfeature ==4:
        if idview ==0:
            return tobeedited(request, dil)
        if idview ==1:
            return mothered(request, dil)
        if idview ==2:
            return notmothered(request, dil)
        if idview ==3:
            return xmothered(request, dil, dilx)
        if idview ==4:
            return xnotmothered(request, dil, dilx)

    return render(request, 'epl/router.html', locals())


def lang(request):
    k = logstatus(request)
    version =epl_version

    return render(request, 'epl/language.html', locals())


def logout_view(request):

    "Homepage sepcial disconnected"

    logout(request)

    # Redirect to a success page.

    version =epl_version
    project = Project.objects.all().order_by('pk')[0].name

    #Feature input :
    i = Feature()
    form = FeatureForm(request.POST, instance =i)
    if form.is_valid():
        lid = Library.objects.get(name =i.libname).lid
        feature =i.feaname
        # if not Feature.objects.filter(feaname = i.feaname, libname =i.libname):
        i.save()
        if lid =="999999999":
            if feature =='instrtodo':
                return instrtodo(request, lid)
            else:
                return checkinstr(request)
        else:
            if feature =='ranking':
                return ranktotake(request, lid)
            elif feature =='arbitration':
                return arbitration(request, lid)
            elif feature =='instrtodo':
                return instrtodo(request, lid)
            elif feature =='edition':
                return tobeedited(request, lid)

    return render(request, 'epl/disconnect.html', locals())


def notintime(request, sid, lid):

    k = logstatus(request)
    version =epl_version

    library = Library.objects.get(lid = lid).name
    if lid =="999999999":
        try:
            title = ItemRecord.objects.get(sid =sid, rank =1).title
        except:
            title = sid
    else:
        title = ItemRecord.objects.get(sid =sid, lid =lid).title
    return render(request, 'epl/notintime.html', locals())


def indicators(request):

    k = logstatus(request)
    version =epl_version

    #Indicators :

    #Number of rankings (exclusions included) :
    rkall = len(ItemRecord.objects.exclude(rank =99))

    #Number of rankings (exclusions excluded) :
    rkright = len(ItemRecord.objects.exclude(rank =99).exclude(rank =0))

    #Number of exclusions :
    exclus = len(ItemRecord.objects.filter(rank =0))

    #number of libraries :
    nlib = len(Library.objects.all())

    #Exclusions details
    dict ={}
    for e in EXCLUSION_CHOICES:
        exclusion =str(e[0])
        value =len(ItemRecord.objects.filter(excl =e[0]))
        dict[exclusion] =value
    del dict['']

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
        if len(ItemRecord.objects.filter(sid =i.sid, rank =99)) ==0 and \
        len(ItemRecord.objects.filter(sid =i.sid, rank =1)) ==0 and \
        len(ItemRecord.objects.filter(sid =i.sid).exclude(rank =0)) >1:
            cnone +=1
            snone +=1/len(ItemRecord.objects.filter(sid =i.sid).exclude(rank =0))
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

    #candidate collections :
    candcoll =coll - isol

    #Number of descarded ressources for exclusion reason :
    discard =0
    for i in ItemRecord.objects.filter(rank =0):
        if len(ItemRecord.objects.filter(sid =i.sid).exclude(rank =0)) ==1:
            discard +=1/(len(ItemRecord.objects.filter(sid =i.sid, rank =0)))
    discard = int(discard)

    #Number of ressources whose instruction of bound elements may begin :
    bdmaybeg = len(ItemRecord.objects.filter(rank =1, status =1))

    #Number of ressources whose bound elements are currently instructed  :
    bdonway = len(ItemRecord.objects.filter(rank =1, status =2))

    #Number of ressources whose instruction of not bound elements may begin :
    notbdmaybeg = len(ItemRecord.objects.filter(rank =1, status =3))

    #Number of ressources whose not bound elements are currently instructed  :
    notbdonway = len(ItemRecord.objects.filter(rank =1, status =4))

    #Number of ressources completely instructed :
    fullinstr = len(ItemRecord.objects.filter(rank =1, status =5))

    #Number of failing sheets :
    fail = len(ItemRecord.objects.filter(status =6, rank =1))

    #Number of instructions :
    instr = len(Instruction.objects.all())

    return render(request, 'epl/indicators.html', locals())


@login_required
def takerank(request, sid, lid):

    k = logstatus(request)
    version =epl_version

    #Authentication control :
    if not request.user.email in [Library.objects.get(lid =lid).contact, Library.objects.get(lid =lid).contact_bis, Library.objects.get(lid =lid).contact_ter]:
        return home(request)

    #Control (takerank only if still possible ; status still ==0 for all attached libraries ;
    #status ==1 and no instruction yet ; lid not "999999999")

    if len(list(ItemRecord.objects.filter(sid =sid).exclude(status =0).exclude(status =1))):
        return notintime(request, sid, lid)
    elif len(list(ItemRecord.objects.filter(sid =sid, status =1))) and len(list(Instruction.objects.filter(sid = sid))):
        return notintime(request, sid, lid)
    elif lid =="999999999":
        return notintime(request, sid, lid)

    # For position form :
    i = ItemRecord.objects.get(sid = sid, lid = lid)
    f = PositionForm(request.POST, instance=i)
    if f.is_valid():
        #last controls before modifications :
        if (len(list(ItemRecord.objects.filter(sid = sid, status =1))) and not len(list(Instruction.objects.filter(sid = sid)))) or\
        len(list(ItemRecord.objects.filter(sid = sid).exclude(status =0))) ==0:
            global lastrked
            lastrked =i
            # if len(ItemRecord.objects.filter(sid =sid).exclude(status =0)) ==0:
            if i.excl !='':
                i.rank =0
            f.save()
            # Other status modification if all libraries have taken rank :
            # Status = 1 : item whose lid identified library must begin bound elements instructions on the sid identified serial (rank =1, no arbitration)
            # ordering by pk for identical ranks upper than 1.
            if len(ItemRecord.objects.filter(sid =sid, rank =99)) ==0 and len(ItemRecord.objects.filter(sid =sid, rank =1)) ==1 and len(ItemRecord.objects.filter(sid =sid).exclude(rank =0)) >1:
                p = ItemRecord.objects.filter(sid =sid).exclude(rank =0).exclude(rank =99).order_by("rank", "pk")[0]
                if p.status !=1:
                    p.status =1
                    p.save()
        else:
            return notintime(request, sid, lid)

        return router(request)

    # Item records list :
    itemlist = ItemRecord.objects.filter(sid =  sid)
    itemlist = list(itemlist)

    # restricted Item records list (without excluded collections) :
    r_itemlist = ItemRecord.objects.filter(sid =  sid).exclude(rank =0)
    r_itemlist = list(r_itemlist)

    # Ressource data :
    ress = itemlist[0]

    # Library data :
    lib = Library.objects.get(lid = lid)

    periscope = "https://periscope.sudoc.fr/?ppnviewed=" + str(sid) + "&orderby=SORT_BY_PCP&collectionStatus=&tree="
    for i in r_itemlist[:-1]:
        periscope = periscope + i.lid + "%2C"
    periscope = periscope + r_itemlist[-1].lid

    return render(request, 'epl/ranking.html', locals())


@login_required
def addinstr(request, sid, lid):

    k = logstatus(request)
    version =epl_version

    q = "x"
    if len(list((Instruction.objects.filter(sid =sid)).filter(name ='checker'))):
        q =" "
    else:
        q ="x"

    #Authentication control :
    if not request.user.email in [Library.objects.get(lid =lid).contact, Library.objects.get(lid =lid).contact_bis, Library.objects.get(lid =lid).contact_ter]:
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
        # q = "x"
        if f.is_valid():
            # if len(list((Instruction.objects.filter(sid =sid)).\
            # filter(name ='checker'))):
            #     q =" "
            # else:
            #     q ="x"
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
            j, l =0, 1
            while j <= len(instr):
                instr[j].line = l
                instr[j].save()
                j +=1
                l +=1
        except:
            pass
        instrlist = Instruction.objects.filter(sid = sid).order_by('line')

        try:
            pklastone = Instruction.objects.filter(sid = sid).latest('pk').pk
        except:
            pklastone =0

    return render(request, 'epl/addinstruction.html', locals())

@login_required
def delinstr(request, sid, lid):

    k = logstatus(request)
    version =epl_version

    #Authentication control :
    if not request.user.email in [Library.objects.get(lid =lid).contact, Library.objects.get(lid =lid).contact_bis, Library.objects.get(lid =lid).contact_ter]:
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

    #Info :
    info =""

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
        j, l =0, 1
        while j <= len(instr):
            instr[j].line = l
            instr[j].save()
            j +=1
            l +=1
    except:
        pass
    instrlist = Instruction.objects.filter(sid = sid).order_by('line')


    #Library list ordered by 'rank' to get from the precedent item list above :
    liblist = []
    for e in itemlist:
        liblist.append(Library.objects.get(lid = e.lid))
    liblist.append(Library.objects.get(name = 'checker'))

    return render(request, 'epl/delinstruction.html', locals())

@login_required
def endinstr(request, sid, lid):

    k = logstatus(request)
    version =epl_version

    #Authentication control :
    if not request.user.email in [Library.objects.get(lid =lid).contact, Library.objects.get(lid =lid).contact_bis, Library.objects.get(lid =lid).contact_ter]:
        return home(request)

    #Control (endinstr only if it's up to the considered library == same conditions as for addinstr)
    try:
        if lid !="999999999":
            if ItemRecord.objects.get(sid = sid, lid =lid).status not in [1, 3]:
                return notintime(request, sid, lid)

        else: # i.e. lid =="999999999"
            if len(list((Instruction.objects.filter(sid =sid)).filter(name ='checker'))) ==2:
                return notintime(request, sid, lid)
            elif len(list((Instruction.objects.filter(sid =sid)).filter(name ='checker'))) ==1:
                if len(list(ItemRecord.objects.filter(sid =sid).exclude(rank =0))) != len(list(ItemRecord.objects.filter(sid =sid, status =4))):
                    return notintime(request, sid, lid)
            else: # i.e. len(list((Instruction.objects.filter(sid =sid)).filter(name ='checker'))) ==0
                if len(list(ItemRecord.objects.filter(sid =sid).exclude(rank =0))) != len(list(ItemRecord.objects.filter(sid =sid, status =2))):
                    return notintime(request, sid, lid)
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
            time =Now()
            checkerinstruction.descr =time
            checkerinstruction.time =time
            checkerinstruction.save()

            #Renumbering instruction lines :
            try:
                instr = Instruction.objects.filter(sid = sid).order_by('line', '-pk')
                j, g =0, 1
                while j <= len(instr):
                    instr[j].line = g
                    instr[j].save()
                    j +=1
                    g +=1
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
                    dest = [nextlib.contact]
                    if nextlib.contact_bis:
                        dest.append(nextlib.contact_bis)
                    if nextlib.contact_ter:
                        dest.append(nextlib.contact_ter)
                    send_mail(subject, message, replymail, dest, fail_silently=True, )

            if len(Instruction.objects.filter(sid =sid, name ='checker')) ==2:
                for e in ItemRecord.objects.filter(sid =sid, status =4):
                    e.status = 5
                    e.save()
            return router(request)

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
            return router(request)

    else: #lid !="999999999"
        if z.is_valid() and y.flag ==True:
            if len(Instruction.objects.filter(sid =sid, name ='checker')) ==0:
                if ItemRecord.objects.filter(sid =sid, status =0).exclude(lid =lid).exclude(rank =0).exists():
                    nextitem = ItemRecord.objects.filter(sid =sid, status =0).exclude(lid =lid).exclude(rank =0).order_by('rank', 'pk')[0]
                    nextlid = nextitem.lid
                    nextlib = Library.objects.get(lid =nextlid)
                    j, g = ItemRecord.objects.get(sid =sid, lid =lid), ItemRecord.objects.get(sid =sid, lid =nextlid)
                    if j.status !=2:
                        j.status, g.status = 2, 1
                        j.save()
                        g.save()
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
                    j, g = ItemRecord.objects.get(sid =sid, lid =lid), ItemRecord.objects.get(sid =sid, lid =nextlid)
                    if j.status !=4:
                        j.status, g.status = 4, 3
                        j.save()
                        g.save()
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
            dest = [nextlib.contact]
            if nextlib.contact_bis:
                dest.append(nextlib.contact_bis)
            if nextlib.contact_ter:
                dest.append(nextlib.contact_ter)
            send_mail(subject, message, replymail, dest, fail_silently=True, )
            return router(request)

        if z.is_valid() and y.flag ==False:
            info =_("Vous n'avez pas coché !")

    instrlist = Instruction.objects.filter(sid = sid).order_by('line')

    return render(request, 'epl/endinstruction.html', locals())


def ranktotake(request, lid):

    k = logstatus(request)
    version =epl_version

    global idfeature, idview, dil
    idfeature, idview, dil =1, 0, lid

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

    nlib = len(Library.objects.exclude(lid ="999999999"))

    return render(request, 'epl/to_rank_list.html', locals())


def modifranklist(request, lid):

    k = logstatus(request)
    version =epl_version

    # global idfeature, idview, dil
    # idfeature, idview, dil =1, 2, lid
    # cf. remarque dans la vue router(request)

    # reclist = list(ItemRecord.objects.filter(lid = lid, status =0).exclude(rank = 99))
    reclist = list(ItemRecord.objects.filter(lid = lid).exclude(rank = 99)\
    .exclude(status =2).exclude(status =3).exclude(status =4).\
    exclude(status =5).exclude(status =6))
    resslist = []
    for e in reclist:
        if len(list(ItemRecord.objects.filter(sid = e.sid, status =1))) and not len(list(Instruction.objects.filter(sid = e.sid))):
            resslist.append(e)
        elif len(list(ItemRecord.objects.filter(sid = e.sid).exclude(status =0))) ==0:
            resslist.append(e)
    l = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name

    nlib = len(Library.objects.exclude(lid ="999999999"))

    return render(request, 'epl/modifrklist.html', locals())


def filter_rklist(request, lid):

    k = logstatus(request)
    version =epl_version

    "Filter rk list"

    libname = (Library.objects.get(lid =lid)).name

    libch = ('checker','checker'),
    if Library.objects.all().exclude(name ='checker').exclude(name =libname):
        for l in Library.objects.all().exclude(name ='checker').exclude(name =libname).order_by('name'):
            libch += (l.name, l.name),

    class XlibForm(forms.Form):
        name = forms.ChoiceField(required = True, widget=forms.Select, choices=libch[1:], label =_("Autre bibliothèque impliquée"))

    form = XlibForm(request.POST or None)
    if form.is_valid():
        xlib = form.cleaned_data['name']
        xlid = Library.objects.get(name =xlib).lid
        return xranktotake(request, lid, xlid)

    return render(request, 'epl/filter_rklist.html', locals())


def xranktotake(request, lid, xlid):

    k = logstatus(request)
    version =epl_version

    global idfeature, idview, dil, dilx
    idfeature, idview, dil, dilx =1, 1, lid, xlid

    #Getting ressources whose this lid must but has not yet taken rank :
    reclist = list(ItemRecord.objects.filter(lid = lid, rank = 99))
    resslist = []
    for e in reclist:
        itemlist = list(ItemRecord.objects.filter(sid = e.sid).exclude(rank =0))
        if len(itemlist) > 1 and list(ItemRecord.objects.filter(sid = e.sid, lid = xlid).exclude(rank =0)):
            resslist.append(e)
    l = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name
    xlibname = Library.objects.get(lid =xlid).name

    return render(request, 'epl/xto_rank_list.html', locals())


def arbitration(request, lid):

    k = logstatus(request)
    version =epl_version

    global idfeature, idview, dil
    idfeature, idview, dil =2, 0, lid

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
        if len(ItemRecord.objects.filter(sid =sid, rank =1)) ==0 and \
        len(ItemRecord.objects.filter(sid =sid, rank =99)) ==0 and \
        len(ItemRecord.objects.filter(sid =sid).exclude(rank =0)) >1:
            resslistb.append(e)

    resslist = resslista + resslistb

    size = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name

    nlib = len(Library.objects.exclude(lid ="999999999"))


    return render(request, 'epl/arbitration.html', locals())


def arbrk1(request, lid):

    k = logstatus(request)
    version =epl_version

    global idfeature, idview, dil
    idfeature, idview, dil =2, 4, lid

    #For the lid identified library, getting ressources whose at \
    #least 2 libraries, including the considered one, took rank =1 \
    #(even if other libraries have not yet taken rank)
    #or all libraries have taken rank, none of them the rank 1

    #Initialization of the ressources to arbitrate :
    resslist = []

    for e in ItemRecord.objects.filter(lid =lid, rank = 1, status =0):
        sid = e.sid
        if ItemRecord.objects.exclude(lid =lid).filter(sid =sid, rank = 1):
            resslist.append(e)

    size = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/arbrk1.html', locals())


def arbnork1(request, lid):

    k = logstatus(request)
    version =epl_version

    global idfeature, idview, dil
    idfeature, idview, dil =2, 2, lid

    #For the lid identified library, getting ressources whose at \
    #least 2 libraries, including the considered one, took rank =1 \
    #(even if other libraries have not yet taken rank)
    #or all libraries have taken rank, none of them the rank 1

    #Initialization of the ressources to arbitrate :
    resslist = []

    for e in ItemRecord.objects.filter(lid =lid, status =0).exclude(rank =1).exclude(rank =0).exclude(rank =99):
        sid = e.sid
        if len(ItemRecord.objects.filter(sid =sid, rank =1)) ==0 and \
        len(ItemRecord.objects.filter(sid =sid, rank =99)) ==0 and \
        len(ItemRecord.objects.filter(sid =sid).exclude(rank =0)) >1:
            resslist.append(e)

    size = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/arbnork1.html', locals())


def filter_arblist(request, lid):

    k = logstatus(request)
    version =epl_version

    "Filter arb list"

    libname = (Library.objects.get(lid =lid)).name

    libch = ('checker','checker'),
    if Library.objects.all().exclude(name ='checker').exclude(name =libname):
        for l in Library.objects.all().exclude(name ='checker').exclude(name =libname).order_by('name'):
            libch += (l.name, l.name),

    class XlibForm(forms.Form):
        name = forms.ChoiceField(required = True, widget=forms.Select, choices=libch[1:], label =_("Autre bibliothèque impliquée"))

    form = XlibForm(request.POST or None)
    if form.is_valid():
        xlib = form.cleaned_data['name']
        xlid = Library.objects.get(name =xlib).lid
        return xarbitration(request, lid, xlid)

    return render(request, 'epl/filter_arblist.html', locals())


def xarbitration(request, lid, xlid):

    k = logstatus(request)
    version =epl_version

    global idfeature, idview, dil, dilx
    idfeature, idview, dil, dilx =2, 1, lid, xlid

    #For the lid identified library, getting ressources whose at \
    #least 2 libraries, including the considered one, took rank =1 \
    #(even if other libraries have not yet taken rank)
    #or all libraries have taken rank, none of them the rank 1

    #Initialization of the ressources to arbitrate :
    resslista = []
    resslistb = []

    for e in ItemRecord.objects.filter(lid =lid, rank = 1, status =0):
        sid = e.sid
        if ItemRecord.objects.filter(sid =sid, lid = xlid, rank = 1):
            resslista.append(e)

    for e in ItemRecord.objects.filter(lid =lid, status =0).exclude(rank =1).exclude(rank =0).exclude(rank =99):
        sid = e.sid
        if len(ItemRecord.objects.filter(sid =sid, rank =1)) ==0 and \
        len(ItemRecord.objects.filter(sid =sid, rank =99)) ==0 and \
        len(ItemRecord.objects.filter(sid =sid).exclude(rank =0)) >1:
            resslistb.append(e)

    resslist = resslista + resslistb

    size = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name
    xlibname = Library.objects.get(lid =xlid).name


    return render(request, 'epl/xarbitration.html', locals())


def x1arb(request, lid, xlid):

    k = logstatus(request)
    version =epl_version

    global idfeature, idview, dil, dilx
    idfeature, idview, dil, dilx =2, 2, lid, xlid

    #For the lid identified library, getting ressources whose at \
    #least 2 libraries, including the considered one, took rank =1 \
    #(even if other libraries have not yet taken rank)
    #or all libraries have taken rank, none of them the rank 1

    #Initialization of the ressources to arbitrate :
    resslist = []

    for e in ItemRecord.objects.filter(lid =lid, rank = 1, status =0):
        sid = e.sid
        if ItemRecord.objects.filter(sid =sid, lid = xlid, rank = 1):
            resslist.append(e)

    size = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name
    xlibname = Library.objects.get(lid =xlid).name


    return render(request, 'epl/x1arbitration.html', locals())


def x0arb(request, lid, xlid):

    k = logstatus(request)
    version =epl_version

    global idfeature, idview, dil, dilx
    idfeature, idview, dil, dilx =2, 3, lid, xlid

    #For the lid identified library, getting ressources whose at \
    #least 2 libraries, including the considered one, took rank =1 \
    #(even if other libraries have not yet taken rank)
    #or all libraries have taken rank, none of them the rank 1

    #Initialization of the ressources to arbitrate :
    resslist = []

    for e in ItemRecord.objects.filter(lid =lid, status =0).exclude(rank =1).exclude(rank =0).exclude(rank =99):
        sid = e.sid
        if len(ItemRecord.objects.filter(sid =sid, rank =1)) ==0 and \
        len(ItemRecord.objects.filter(sid =sid, rank =99)) ==0 and \
        len(ItemRecord.objects.filter(sid =sid).exclude(rank =0)) >1:
            resslist.append(e)

    size = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name
    xlibname = Library.objects.get(lid =xlid).name


    return render(request, 'epl/x0arbitration.html', locals())


def instrtodo(request, lid):

    k = logstatus(request)
    version =epl_version

    global idfeature, idview, dil
    idfeature, idview, dil =3, 0, lid

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

    nlib = len(Library.objects.exclude(lid ="999999999"))

    lidchecker = "999999999"

    return render(request, 'epl/instrtodo.html', locals())


def instroneb(request, lid):

    k = logstatus(request)
    version =epl_version

    if lid !="999999999":
        # Ressources whose the lid identified library has rank =1 and has to deal with bound elements (status =1)
        l = ItemRecord.objects.filter(lid =lid, rank =1).exclude(status =0).exclude(status =2).exclude(status =3).exclude(status =4).exclude(status =5).exclude(status =6)

    elif lid =="999999999":
        do = home(request)
        return do

    size = len(l)

    #Getting library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/instrtodobd1.html', locals())


def instrotherb(request, lid):

    k = logstatus(request)
    version =epl_version

    if lid !="999999999":
        # Ressources whose the lid identified library has rank !=1 and has to deal with bound elements (status =1)
        l = ItemRecord.objects.filter(lid =lid).exclude(rank =1).exclude(status =0).exclude(status =2).exclude(status =3).exclude(status =4).exclude(status =5).exclude(status =6)

    elif lid =="999999999":
        do = home(request)
        return do

    size = len(l)

    #Getting library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/instrtodobdnot1.html', locals())


def instronenotb(request, lid):

    k = logstatus(request)
    version =epl_version

    if lid !="999999999":
        # Ressources whose the lid identified library has rank =1 and has to deal with not bound elements (status =3)
        l = ItemRecord.objects.filter(lid =lid, rank =1).exclude(status =0).exclude(status =1).exclude(status =2).exclude(status =4).exclude(status =5).exclude(status =6)

    elif lid =="999999999":
        do = home(request)
        return do

    size = len(l)

    #Getting library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/instrtodonotbd1.html', locals())


def instrothernotb(request, lid):

    k = logstatus(request)
    version =epl_version

    if lid !="999999999":
        # Ressources whose the lid identified library has rank !=1 and has to deal with not bound elements (status =3)
        l = ItemRecord.objects.filter(lid =lid).exclude(rank =1).exclude(status =0).exclude(status =1).exclude(status =2).exclude(status =4).exclude(status =5).exclude(status =6)

    elif lid =="999999999":
        do = home(request)
        return do

    size = len(l)

    #Getting library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/instrtodonotbdnot1.html', locals())


def instrfilter(request, lid):

    k = logstatus(request)
    version =epl_version

    "Filter instruction list"

    libname = (Library.objects.get(lid =lid)).name

    libch = ('checker','checker'),
    if Library.objects.all().exclude(name ='checker').exclude(name =libname):
        for l in Library.objects.all().exclude(name ='checker').exclude(name =libname).order_by('name'):
            libch += (l.name, l.name),

    class XlibForm(forms.Form):
        name = forms.ChoiceField(required = True, widget=forms.Select, choices=libch[1:], label =_("Autre bibliothèque impliquée"))

    form = XlibForm(request.POST or None)
    if form.is_valid():
        xlib = form.cleaned_data['name']
        xlid = Library.objects.get(name =xlib).lid
        # return xranktotake(request, lid, xlid)
        return xinstrlist(request, lid, xlid)
    return render(request, 'epl/filter_instrlist.html', locals())


def xinstrlist(request, lid, xlid):

    k = logstatus(request)
    version =epl_version

    global idfeature, idview, dil, dilx
    idfeature, idview, dil, dilx =3, 1, lid, xlid

    name = Library.objects.get(lid =lid).name
    xname = Library.objects.get(lid =xlid).name

    lprov = ItemRecord.objects.filter(lid =lid).exclude(status =0).exclude(status =2).exclude(status =4).exclude(status =5).exclude(status =6)

    l =[]
    for e in lprov:
        if ItemRecord.objects.filter(lid =xlid).exclude(rank =0):
            l.append(e)
    size = len(l)

    return render(request, 'epl/xto_instr_list.html', locals())


def tobeedited(request, lid):

    k = logstatus(request)
    version =epl_version

    global idfeature, idview, dil
    idfeature, idview, dil =4, 0, lid

    #For the lid identified library, getting ressources whose the resulting \
    #collection has been entirely completed and may consequently be edited.
    #Trick : These ressources have two instructions with name = 'checker' :

    l = ItemRecord.objects.filter(lid =lid).exclude(rank =0)

    #Initializing a list of ressources to edit :
    resslist = []

    for e in l:
        nl = Instruction.objects.filter(sid =e.sid)
        kd = nl.filter(name = "checker")
        if len(kd) ==2:
            resslist.append(e)

    size = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/to_edit_list.html', locals())


def mothered(request, lid):

    k = logstatus(request)
    version =epl_version

    global idfeature, idview, dil
    idfeature, idview, dil =4, 1, lid

    #For the lid identified library, getting ressources whose the resulting \
    #collection has been entirely completed and may consequently be edited.
    #Trick : These ressources have two instructions with name = 'checker' :

    l = ItemRecord.objects.filter(lid =lid, rank =1)

    #Initializing a list of ressources to edit :
    resslist = []

    for e in l:
        nl = Instruction.objects.filter(sid =e.sid)
        kd = nl.filter(name = "checker")
        if len(kd) ==2:
            resslist.append(e)

    size = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/to_edit_list_mother.html', locals())


def notmothered(request, lid):

    k = logstatus(request)
    version =epl_version

    global idfeature, idview, dil
    idfeature, idview, dil =4, 2, lid

    #For the lid identified library, getting ressources whose the resulting \
    #collection has been entirely completed and may consequently be edited.
    #Trick : These ressources have two instructions with name = 'checker' :

    l = ItemRecord.objects.filter(lid =lid).exclude(rank =1).exclude(rank =0).exclude(rank =99)

    #Initializing a list of ressources to edit :
    resslist = []

    for e in l:
        nl = Instruction.objects.filter(sid =e.sid)
        kd = nl.filter(name = "checker")
        if len(kd) ==2:
            resslist.append(e)

    size = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/to_edit_list_notmother.html', locals())


def filter_edlist(request, lid):

    k = logstatus(request)
    version =epl_version

    "Filter"

    name = (Library.objects.get(lid =lid)).name

    libch = ('checker','checker'),
    if Library.objects.all().exclude(name ='checker').exclude(name =name):
        for l in Library.objects.all().exclude(name ='checker').exclude(name =name).order_by('name'):
            libch += (l.name, l.name),

    class EditionForm(forms.Form):
        rk_ch = (("a", _("Collection mère")), ("b", _("Collection non mère")),)
        rank = forms.ChoiceField(required = True, widget=forms.Select, choices=rk_ch, label =_("Rang des collections de la bibliothèque mentionnée dans l'entête de cette page"))
        lib = forms.ChoiceField(required = True, widget=forms.Select, choices=libch[1:], label =_("Autre bibliothèque impliquée"))

    form = EditionForm(request.POST or None)
    if form.is_valid():
        rank = form.cleaned_data['rank']
        xlib = form.cleaned_data['lib']
        xlid = Library.objects.get(name =xlib).lid
        if lid == xlid:
            if rank =="a":
                return mothered(request, lid)
            else:
                return notmothered(request, lid)
        else: # lid != xlid
            if rank =="a":
                return xmothered(request, lid, xlid)
            else:
                return xnotmothered(request, lid, xlid)

    return render(request, 'epl/filter_edlist.html', locals())


def xmothered(request, lid, xlid):

    k = logstatus(request)
    version =epl_version

    global idfeature, idview, dil, dilx
    idfeature, idview, dil, dilx =4, 3, lid, xlid

    l = ItemRecord.objects.filter(lid =lid, rank =1)

    #Initializing a list of ressources to edit :
    resslist = []

    for e in l:
        nl = Instruction.objects.filter(sid =e.sid)
        kd = nl.filter(name = "checker")
        if len(kd) ==2 and Instruction.objects.filter(sid =e.sid, name =Library.objects.get(lid =xlid)):
            resslist.append(e)

    size = len(resslist)

    name = Library.objects.get(lid =lid).name
    xname = Library.objects.get(lid =xlid).name

    return render(request, 'epl/xto_edit_list_mother.html', locals())


def xnotmothered(request, lid, xlid):

    k = logstatus(request)
    version =epl_version

    global idfeature, idview, dil, dilx
    idfeature, idview, dil, dilx =4, 4, lid, xlid

    l = ItemRecord.objects.filter(lid =lid).exclude(rank =1).exclude(rank =0).exclude(rank =99)

    #Initializing a list of ressources to edit :
    resslist = []

    for e in l:
        nl = Instruction.objects.filter(sid =e.sid)
        kd = nl.filter(name = "checker")
        if len(kd) ==2 and Instruction.objects.filter(sid =e.sid, name =Library.objects.get(lid =xlid)):
            resslist.append(e)

    size = len(resslist)

    name = Library.objects.get(lid =lid).name
    xname = Library.objects.get(lid =xlid).name

    return render(request, 'epl/xto_edit_list_notmother.html', locals())


def edition(request, sid, lid):

    k = logstatus(request)
    version =epl_version

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

        return render(request, 'epl/edition.html', locals())

    else:
        return notintime(request, sid, lid)


def checkinstr(request):

    k = logstatus(request)
    version =epl_version

    project = Project.objects.all().order_by('pk')[0].name

    return render(request, 'epl/checker.html', locals())


def checkerfilter(request):

    k = logstatus(request)
    version =epl_version

    form = InstructionCheckerFilter(request.POST or None)
    if form.is_valid():
        coll_set = form.cleaned_data['name']
        phase_set = form.cleaned_data['phase']
        l = []
        if len(phase_set) ==2:
            return xckall(request, coll_set)
        elif phase_set[0] =='bound':
            return xckbd(request, coll_set)
        else:
            return xcknbd(request, coll_set)

    return render(request, 'epl/filter_ck_instrlist.html', locals())


def xckbd(request, coll_set):

    k = logstatus(request)
    version =epl_version

    global idfeature, idview, tes_lloc
    idfeature, idview, tes_lloc =3, 2, coll_set

    l = []

    for e in ItemRecord.objects.filter(status =2, rank =1):
        if len(ItemRecord.objects.filter(sid =e.sid, status =2)) == len(ItemRecord.objects.filter(sid =e.sid).exclude(rank =0)) and len(Instruction.objects.filter(sid =e.sid, name= "checker")) ==0:
            for coll in coll_set:
                if ItemRecord.objects.filter(lid =Library.objects.get(name =coll).lid, sid =e.sid).exclude(rank =0):
                    if ItemRecord.objects.get(sid =e.sid, rank =1) not in l:
                        l.append(ItemRecord.objects.get(sid =e.sid, rank =1)) #yehh ... rank =1 that's the trick !
    size = len(l)

    return render(request, 'epl/xckbd.html', locals())


def xcknbd(request, coll_set):

    k = logstatus(request)
    version =epl_version

    global idfeature, idview, tes_lloc
    idfeature, idview, tes_lloc =3, 3, coll_set

    l = []

    for e in ItemRecord.objects.filter(status =4, rank =1):
        if len(ItemRecord.objects.filter(sid =e.sid, status =4)) == len(ItemRecord.objects.filter(sid =e.sid).exclude(rank =0)) and len(Instruction.objects.filter(sid =e.sid, name= "checker")) ==1:
            for coll in coll_set:
                if ItemRecord.objects.filter(lid =Library.objects.get(name =coll).lid, sid =e.sid).exclude(rank =0):
                    if ItemRecord.objects.get(sid =e.sid, rank =1) not in l:
                        l.append(ItemRecord.objects.get(sid =e.sid, rank =1)) #yehh ... rank =1 that's the trick !
    size = len(l)

    return render(request, 'epl/xcknbd.html', locals())


def xckall(request, coll_set):

    k = logstatus(request)
    version =epl_version

    global idfeature, idview, tes_lloc
    idfeature, idview, tes_lloc =3, 4, coll_set

    l = []

    for e in ItemRecord.objects.filter(status =2, rank =1):
        if len(ItemRecord.objects.filter(sid =e.sid, status =2)) == len(ItemRecord.objects.filter(sid =e.sid).exclude(rank =0)) and len(Instruction.objects.filter(sid =e.sid, name= "checker")) ==0:
            for coll in coll_set:
                if ItemRecord.objects.filter(lid =Library.objects.get(name =coll).lid, sid =e.sid).exclude(rank =0):
                    if ItemRecord.objects.get(sid =e.sid, rank =1) not in l:
                        l.append(ItemRecord.objects.get(sid =e.sid, rank =1)) #yehh ... rank =1 that's the trick !

    for e in ItemRecord.objects.filter(status =4, rank =1):
        if len(ItemRecord.objects.filter(sid =e.sid, status =4)) == len(ItemRecord.objects.filter(sid =e.sid).exclude(rank =0)) and len(Instruction.objects.filter(sid =e.sid, name= "checker")) ==1:
            for coll in coll_set:
                if ItemRecord.objects.filter(lid =Library.objects.get(name =coll).lid, sid =e.sid).exclude(rank =0):
                    if ItemRecord.objects.get(sid =e.sid, rank =1) not in l:
                        l.append(ItemRecord.objects.get(sid =e.sid, rank =1)) #yehh ... rank =1 that's the trick !
    size = len(l)

    return render(request, 'epl/xckall.html', locals())
