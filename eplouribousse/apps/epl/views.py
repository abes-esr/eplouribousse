epl_version ="v1.8.5 (Radegonde)"
date_version ="September 3, 2020"
# Mise au niveau de :
# epl_version ="v1.9-beta.5 (~Walderade)"
# date_version ="September 15, 2020"


from django.shortcuts import render

from .models import *

from .forms import *

from django.core.mail import send_mail

from django.db.models.functions import Now

from django.contrib.auth.decorators import login_required

from django.utils.translation import ugettext as _

from django.contrib.auth.models import User

from django.contrib.auth import logout

from django.http import HttpResponseRedirect


client_ip ='127.0.0.1'
idfeature =0 #identification de la fonctionnalité (0 pour accueil, 1 pour positionnement, 2 pour arbitrage, 3 pour instr et 4 pour ed)
idview =1 #identification des fonctions de listes (voir les vues correspondantes)
dil =Library.objects.exclude(lid ="999999999")[0].lid # comme lid
dilx =Library.objects.exclude(lid ="999999999")[1].lid # comme xlid
tes_lloc =Library.objects.all() # comme coll_set
lastrked =None

def serial_title(e):
    """sorting by title"""
    return e.title
def serial_id(e):
    """sorting by sid"""
    return e.sid
def coll_cn(e):
    """sorting by cn, title"""
    return (e.cn, e.title)

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
                return instrtodo(request, lid, 'title')
            else:
                return checkinstr(request)
        else:
            if feature =='ranking':
                return ranktotake(request, lid, 'title')
            elif feature =='arbitration':
                return arbitration(request, lid, 'title')
            elif feature =='instrtodo':
                return instrtodo(request, lid, 'title')
            elif feature =='edition':
                return tobeedited(request, lid, 'title')

    return render(request, 'epl/home.html', locals())


def about(request):

    k = logstatus(request)
    version =epl_version
    date =date_version
    host = str(request.get_host())
    return render(request, 'epl/about.html', locals())


def contact(request):

    k = logstatus(request)
    version =epl_version
    date =date_version
    host = str(request.get_host())

    class ContactForm(forms.Form):
        object_list = (("Demande d'information", _("Demande d'information")), ("Bug", _("Bug")),\
         ("Réclamation", _("Réclamation")), ("Suggestion", _("Suggestion")), ("Avis", _("Avis")),  ("Autre", _("Autre")))
        object = forms.ChoiceField(required = True, widget=forms.Select, choices=object_list, label =_("Objet"))
        email = forms.EmailField(required = True, label =_("Votre adresse mail de contact"))
        email_confirm =forms.EmailField(required = True, label =_("Confirmation de l'adresse mail"))
        content = forms.CharField(required=True, widget=forms.Textarea, label =_("Votre message"))

    form = ContactForm(request.POST or None)
    if form.is_valid():
        recipient = form.cleaned_data['email']
        recipient_confirm = form.cleaned_data['email_confirm']
        subject2 = form.cleaned_data['object']
        body = form.cleaned_data['content']
        if recipient ==recipient_confirm:
            subject2 = "[eplouribousse]" + " - " + subject2
            subject1 = subject2 + " - " + version + " - " + host
            message1 = subject1 + " :\n" + "\n" + body
            message2 = "Votre message a bien été envoyé au développeur de l'application"\
             + ".\n" + "Ne répondez pas au présent message s'il vous plaît" + ".\n" + \
             "Rappel de l'objet de votre message" + " : " + subject2 + \
             "\n" + "Rappel de votre message" + " :\n" + "\n" + \
             _("***** Début *****") + "\n" + body + "\n" + _("*****  Fin  *****")
            dest1 = ["eplouribousse@gmail.com"]
            dest2 = [recipient]
            send_mail(subject1, message1, recipient, dest1, fail_silently=True, )
            send_mail(subject2, message2, replymail, dest2, fail_silently=True, )
            return render(request, 'epl/confirmation.html', locals())
        else:
            info =_("Attention : Les adresses doivent être identiques") + "."
    else:
        if request.method =="POST":
            info =_("Vérifier que les adresses sont correctes") + "."

    return render(request, 'epl/contact.html', locals())


def confirm(request):

    k = logstatus(request)
    version =epl_version

    return render(request, 'epl/confirmation.html', locals())


def router(request):

    if not client_ip ==request.META['REMOTE_ADDR']:
        return home(request)
    else:
        if idfeature ==0:
            return home(request)
        if idfeature ==1:
            if idview ==0:
                return ranktotake(request, dil, 'title')
            if idview ==1:
                return xranktotake(request, dil, dilx, 'title')
            # if idview ==2:
            #     return modifranklist(request, dil)
            # Le choix de supprimer le bloc ci-dessus tient à ce que les modifications de rang sont normalement réalisés à l'unité ;
            # il est donc plus intéressant de revenir à la dernière liste de positionnement. En conséquence la modification des varables
            # globales a été annulée dans la vue modifranklist(request, dil)
        if idfeature ==2:
            if idview ==0:
                return arbitration(request, dil, 'title')
            if idview ==1:
                return xarbitration(request, dil, dilx, 'title')
            if idview ==2:
                return x1arb(request, dil, dilx, 'title')
            if idview ==3:
                return x0arb(request, dil, dilx, 'title')
            if idview ==4:
                return arbrk1(request, dil, 'title')
            if idview ==5:
                return arbnork1(request, dil, 'title')
        if idfeature ==3:
            if idview ==0:
                return instrtodo(request, dil, 'title')
            if idview ==1:
                return xinstrlist(request, dil, dilx, 'title')
            if idview ==2:
                return xckbd(request, tes_lloc)
            if idview ==3:
                return xcknbd(request, tes_lloc)
            if idview ==4:
                return xckall(request, tes_lloc)
        if idfeature ==4:
            if idview ==0:
                return tobeedited(request, dil, 'title')
            if idview ==1:
                return mothered(request, dil, 'title')
            if idview ==2:
                return notmothered(request, dil, 'title')
            if idview ==3:
                return xmothered(request, dil, dilx, 'title')
            if idview ==4:
                return xnotmothered(request, dil, dilx, 'title')

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
                return instrtodo(request, lid, 'title')
            else:
                return checkinstr(request)
        else:
            if feature =='ranking':
                return ranktotake(request, lid, 'title')
            elif feature =='arbitration':
                return arbitration(request, lid, 'title')
            elif feature =='instrtodo':
                return instrtodo(request, lid, 'title')
            elif feature =='edition':
                return tobeedited(request, lid, 'title')

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

    #Number of real candidates (collections)
    realcandcoll =candcoll - exclus

    #Number of real candidates (ressources)
    realcand =cand - discard

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


def search(request):

    k = logstatus(request)
    version =epl_version

    libch = ('checker','checker'),
    for l in Library.objects.all().exclude(name ='checker').order_by('name'):
        libch += (l.name, l.name),

    class SearchForm(forms.Form):
        sid = forms.CharField(required = True, label =_("ppn"))
        lib = forms.ChoiceField(required = True, widget=forms.Select, choices=libch, label =_("Votre bibliothèque"))

    l =0
    form = SearchForm(request.POST or None)
    if form.is_valid():
        sid = form.cleaned_data['sid']
        lib = form.cleaned_data['lib']
        lid = Library.objects.get(name =lib).lid
        n = len(ItemRecord.objects.filter(sid =sid))
        ranklist =[] # if n==0
        progress =0
        action, laction =0,0
        alteraction, lalteraction =0,0
        if ItemRecord.objects.filter(sid =sid):
            # Bibliographic data :
            title = ItemRecord.objects.filter(sid =sid)[0].title
            issn = ItemRecord.objects.filter(sid =sid)[0].issn
            pubhist = ItemRecord.objects.filter(sid =sid)[0].pubhist
        if ItemRecord.objects.filter(sid =sid, lid =lid):
            l =1
            # ItemRecord data :
            holdstat = ItemRecord.objects.get(sid =sid, lid = lid).holdstat
            missing = ItemRecord.objects.get(sid =sid, lid = lid).missing
            cn = ItemRecord.objects.get(sid =sid, lid = lid).cn

        if n ==1:
            bil =Library.objects.get(lid =ItemRecord.objects.get(sid =sid).lid).name

        elif n >1:
            #Getting instructions for the considered ressource :
            instrlist = Instruction.objects.filter(sid = sid).order_by('line')

            try:
                pklastone = Instruction.objects.filter(sid = sid).latest('pk').pk
            except:
                pklastone =0

            #Attachements :
            attchmt =ItemRecord.objects.filter(sid =sid).order_by('-status')
            attlist = [(Library.objects.get(lid =element.lid).name, element) for element in attchmt]

            rklist = ItemRecord.objects.filter(sid =sid).order_by('rank', 'lid')
            ranklist = [(element, Library.objects.get(lid =element.lid).name) for element in rklist]
            if ItemRecord.objects.filter(sid =sid, status =6):
                progress =_("Une anomalie a été constatée au cours de l'instruction de la résultante")
            elif ItemRecord.objects.filter(sid =sid, status =5):
                progress =_("Instruction achevée")
                if ItemRecord.objects.filter(sid =sid, lid =lid).exclude(rank =0):
                    action, laction =_("Edition de la fiche de résultante"), "ed/" + str(sid) + "/" + str(lid)
            elif ItemRecord.objects.filter(sid =sid, lid = lid, status =4):
                if len(ItemRecord.objects.get(sid =sid, status =3)):
                    xname =Library.objects.get(lid =ItemRecord.objects.get(sid =sid, status =3).lid).name
                    progress =_("Instruction des éléments non reliés de la collection")
                else: # tous les enregistrements sont au statut 4
                    progress =_("En attente de validation finale par le contrôleur")
            elif ItemRecord.objects.filter(sid =sid, lid = lid, status =3):
                progress =_("Instruction des éléments non reliés de votre collection")
                action, laction =_("Instruction"), "add/" + str(sid) + "/" + str(lid)
            elif ItemRecord.objects.filter(sid =sid, lid = lid, status =2):
                try:
                    xname =Library.objects.get(lid =ItemRecord.objects.get(sid =sid, status =1).lid).name
                    progress =_("Instruction des éléments reliés de la collection")
                    return render(request, 'epl/search.html', locals())
                except: # tous les enregistrements sont au statut 2
                    progress =_("En attente de validation intermédiaire par le contrôleur")
                    return render(request, 'epl/search.html', locals())
            elif ItemRecord.objects.filter(sid =sid, lid = lid, status =1):
                progress =_("Instruction des éléments reliés de votre collection")
                action, laction =_("Instruction"), "add/" + str(sid) + "/" + str(lid)
                if not Instruction.objects.filter(sid =sid):
                    alteraction, lalteraction =_("Modification du rang de votre collection"), "rk/" + str(sid) + "/" + str(lid)
            elif ItemRecord.objects.filter(sid =sid, lid = lid, status =0):
                try:
                    xname =Library.objects.get(lid =ItemRecord.objects.get(sid =sid, status =1).lid).name
                    progress =_("Instruction des éléments reliés de la collection")
                    if not Instruction.objects.filter(sid =sid):
                        alteraction, lalteraction =_("Modification du rang de votre collection"), "rk/" + str(sid) + "/" + str(lid)
                    return render(request, 'epl/search.html', locals())
                except:
                    if len(ItemRecord.objects.filter(sid =sid, rank =1)) >1:
                        progress =_("Concurrence rang 1")
                        action, laction =_("Modification du rang de votre collection"), "rk/" + str(sid) + "/" + str(lid)
                    elif len(ItemRecord.objects.filter(sid =sid).exclude(rank=0)) <2:
                        progress =_("Ressource non candidate du fait d'exclusion")
                    elif ItemRecord.objects.filter(sid =sid, rank =99):
                        if ItemRecord.objects.filter(sid =sid, lid =lid, rank =99):
                            progress =_("Vous devez positionnez votre collection")
                            action, laction =_("Positionnement de votre collection"), "rk/" + str(sid) + "/" + str(lid)
                        else:
                            progress =_("Votre collection est déjà positionnée ; modification encore possible")
                            alteraction, lalteraction =_("Modification du rang de votre collection"), "rk/" + str(sid) + "/" + str(lid)
                    else: # Arbitration, no rank =1
                        progress =_("Absence de rang 1")
                        action, laction =_("Modification du rang de votre collection"), "rk/" + str(sid) + "/" + str(lid)
                    return render(request, 'epl/search.html', locals())
            else: #lid ="999999999"
                if ItemRecord.objects.filter(sid =sid, status =5):
                    progress =_("Instruction achevée")
                    alteraction, lalteraction =_("Edition des résultantes par bibliothèque"), "home/"
                elif ItemRecord.objects.filter(sid =sid, status =4):
                    if not ItemRecord.objects.filter(sid =sid, status =3):
                        progress =_("Validation finale")
                        action, laction =_("Vérification finale"), "add/" + str(sid) + "/" + str(lid)
                    else:
                        xname =Library.objects.get(lid =ItemRecord.objects.get(sid =sid, status =3).lid).name
                        progress =_("Instruction des éléments non reliés de la collection")
                elif ItemRecord.objects.filter(sid =sid, status =3):
                    xname =Library.objects.get(lid =ItemRecord.objects.get(sid =sid, status =3).lid).name
                    progress =_("Instruction des éléments non reliés de la collection")
                elif ItemRecord.objects.filter(sid =sid, status =2):
                    if not ItemRecord.objects.filter(sid =sid, status =1):
                        progress =_("Validation intermédiaire")
                        action, laction =_("Vérification intermédiaire"), "add/" + str(sid) + "/" + str(lid)
                    else:
                        xname =Library.objects.get(lid =ItemRecord.objects.get(sid =sid, status =1).lid).name
                        progress =_("Instruction des éléments reliés de la collection")
                elif ItemRecord.objects.filter(sid =sid, status =1):
                    xname =Library.objects.get(lid =ItemRecord.objects.get(sid =sid, status =1).lid).name
                    progress =_("Instruction des éléments reliés de la collection")
                else: # tous les enregistrements ont le statut =0
                    if len(ItemRecord.objects.filter(sid =sid, rank =1)) >1:
                        progress =_("Concurrence rang 1")
                    elif len(ItemRecord.objects.filter(sid =sid).exclude(rank=0)) <2:
                        progress =_("Ressource non candidate du fait d'exclusion")
                    elif ItemRecord.objects.filter(sid =sid, rank =99):
                        progress =_("Positionnement")
                    else: # Arbitration, no rank =1
                        progress =_("Absence de rang 1")

    return render(request, 'epl/search.html', locals())


@login_required
def takerank(request, sid, lid):

    k = logstatus(request)
    version =epl_version

    #Authentication control :
    if not request.user.email in [Library.objects.get(lid =lid).contact, Library.objects.get(lid =lid).contact_bis, Library.objects.get(lid =lid).contact_ter]:
        return home(request)

    #Control (takerank only if still possible ; status still ==0 for all attached libraries ;
    #or status ==1 but no instruction yet ; lid not "999999999")

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

            if len(ItemRecord.objects.filter(sid =sid, status =1)): #Since it's possible when modifying
                for elmt in ItemRecord.objects.filter(sid =sid).exclude(rank =99):
                    if elmt.status !=0:
                        elmt.status =0
                        elmt.save()

            if len(ItemRecord.objects.filter(sid =sid, rank =99)) ==0 and len(ItemRecord.objects.filter(sid =sid, rank =1)) ==1 \
            and len(ItemRecord.objects.filter(sid =sid).exclude(rank =0)) >1:
                p = ItemRecord.objects.filter(sid =sid).exclude(rank =0).exclude(rank =99).order_by("rank", "pk")[0]
                p.status =1
                p.save()

        else:
            return notintime(request, sid, lid)

        return router(request)

    # Item records list :
    itlist = ItemRecord.objects.filter(sid =  sid)
    itemlist = [(element, Library.objects.get(lid =element.lid).name) for element in itlist]
    # itemlist = list(itemlist)

    # restricted Item records list (without excluded collections) :
    r_itemlist = ItemRecord.objects.filter(sid =  sid).exclude(rank =0)
    r_itemlist = list(r_itemlist)

    # Ressource data :
    ress = itemlist[0][0]

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
    length =0

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

        REM_CHOICES =('',''),
        bibliolist =[]
        if Instruction.objects.filter(sid =sid).exclude(name =Library.objects.get(lid =lid).name).exclude(name ='checker'):
            for e in Instruction.objects.filter(sid =sid).exclude(name =Library.objects.get(lid =lid).name).exclude(name ='checker'):
                if (e.exc or e.degr) and Library.objects.get(name =e.name).name not in bibliolist:
                    bibliolist.append(Library.objects.get(name =e.name).name)
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
            if not len(Instruction.objects.filter(sid =sid, name =lib.name, bound =i.bound, oname =i.oname, descr =i.descr, exc =i.exc, degr =i.degr)):
                i.line +=1
                i.time =Now()
                f.save()
                url ="/add/" + str(sid) + "/" + str(lid)
                return HttpResponseRedirect(url)
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

    return render(request, 'epl/addinstruction.html', { 'ressource' : ress, \
    'library' : lib, 'instructions' : instrlist , 'form' : f, 'foname' : foname, 'librarylist' : \
    liblist, 'remedied_lib_list' : remliblist, 'sid' : sid, 'stage' : bd, 'info' : info, \
    'lid' : lid, 'expected' : q, 'lastone' : pklastone, 'k' : k, 'version' : version, 'l' : length, })

@login_required
def selinstr(request, sid, lid):

    k = logstatus(request)
    version =epl_version

    #Authentication control :
    if not request.user.email in [Library.objects.get(lid =lid).contact, Library.objects.get(lid =lid).contact_bis, Library.objects.get(lid =lid).contact_ter]:
        return home(request)

    do = notintime(request, sid, lid)

    #Control (selinstr only if it's up to the considered library == same conditions as for addinstr if lid not "999999999")
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

    LINE_CHOICES =('',''),
    for elmt in Instruction.objects.filter(sid =sid, name =lib.name).order_by('line'):
        if elmt.bound ==expected:
            LINE_CHOICES += (elmt.line, elmt.line),

    class Line_Form(forms.Form):
        row = forms.ChoiceField(required = True, widget=forms.Select, choices=LINE_CHOICES[1:])
    f = Line_Form(request.POST or None)

    if f.is_valid():
        linetomodify = f.cleaned_data['row']
        url ="/mod/" + str(sid) + "/" + str(lid) + "/" + str(linetomodify)
        return HttpResponseRedirect(url)

    instrlist = Instruction.objects.filter(sid = sid).order_by('line')

    #Library list ordered by 'rank' to get from the precedent item list above :
    liblist = []
    for e in itemlist:
        liblist.append(Library.objects.get(lid = e.lid))
    liblist.append(Library.objects.get(name = 'checker'))

    return render(request, 'epl/selinstruction.html', { 'ressource' : ress, \
    'library' : lib, 'instructions' : instrlist , 'form' : f, 'librarylist' : \
    liblist, 'remedied_lib_list' : remliblist, 'sid' : sid, 'stage' : bd, 'info' : info, \
    'lid' : lid, 'expected' : expected, 'answer' : answer, 'k' : k, 'version' : version, })


@login_required
def modinstr(request, sid, lid, linetomodify):

    k = logstatus(request)
    version =epl_version
    length =0

    q = "x"
    if len(list((Instruction.objects.filter(sid =sid)).filter(name ='checker'))):
        q =" "
    else:
        q ="x"

    #Library data :
    lib = Library.objects.get(lid = lid)

    #Authentication control :
    if not request.user.email in [Library.objects.get(lid =lid).contact, Library.objects.get(lid =lid).contact_bis, Library.objects.get(lid =lid).contact_ter]:
        return home(request)

    do = notintime(request, sid, lid)

    #Control (modinstr only if possible)
    try:
        if lid !="999999999":
            if ItemRecord.objects.get(sid =sid, lid =lid).status not in [1, 3]:
                return do
            if Instruction.objects.get(sid =sid, line =linetomodify).name !=lib.name:
                return do
            if Instruction.objects.get(sid =sid, line =linetomodify).bound !=q:
                return do

        else: # i.e. lid =="999999999"
            return do
    except:
        z =1 #This is just to continue


    #Ressource data :
    itemlist = ItemRecord.objects.filter(sid = sid).exclude(rank =0).order_by("rank", 'pk')
    ress = itemlist[0]

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
        i = Instruction(sid = sid, name = lib.name)
        if request.method == 'POST':
            f = InstructionForm(request.POST, instance =i)

            REM_CHOICES =('',''),
            bibliolist =[]
            if Instruction.objects.filter(sid =sid).exclude(name =Library.objects.get(lid =lid).name).exclude(name ='checker'):
                for e in Instruction.objects.filter(sid =sid).exclude(name =Library.objects.get(lid =lid).name).exclude(name ='checker'):
                    if (e.exc or e.degr) and Library.objects.get(name =e.name).name not in bibliolist:
                        bibliolist.append(Library.objects.get(name =e.name).name)
                bibliolist.sort()
                length =len(bibliolist)
            if length:
                for l in bibliolist:
                    REM_CHOICES += (l, l),

            class Instr_Form(forms.Form):
                oname = forms.ChoiceField(required = False, widget=forms.Select\
                (attrs={'title': _("Intitulé de la bibliothèque ayant précédemment déclaré une 'exception' ou un 'améliorable'")})\
                , choices=REM_CHOICES, initial =Instruction.objects.get(sid =sid, line =linetomodify).\
                oname, label =_("Bibliothèque remédiée"),)

            foname = Instr_Form(request.POST or None)

            if f.is_valid():
                if foname.is_valid():
                    i.oname = foname.cleaned_data['oname']
                i.bound =q
                #A line may only be registered once :
                if len(Instruction.objects.exclude(line =linetomodify).filter(sid =sid, name =lib.name, bound =i.bound, oname =i.oname, descr =i.descr, exc =i.exc, degr =i.degr)):
                    info = _("Une autre ligne contient déjà les mêmes données.")
                else:
                    Instruction.objects.get(sid =sid, name =lib.name, line =linetomodify).delete()
                    if i.line <linetomodify:
                        i.line +=1
                        i.time =Now()
                        i.save()
                    else:
                        i.line +=2
                        i.time =Now()
                        i.save()

            instrlist = Instruction.objects.filter(sid = sid).order_by('line')

            try:
                pklastone = Instruction.objects.filter(sid = sid).latest('pk').pk
            except:
                pklastone =0
            if info =="":
                url ="/add/" + str(sid) + "/" + str(lid)
                return HttpResponseRedirect(url) # Renumbering shall be done there.
        else:
            #Instruction form instanciation and validation :
            f = InstructionForm(instance =i, initial = {
            'line' : Instruction.objects.get(sid =sid, line =linetomodify).line - 1,
            # 'oname' : Instruction.objects.get(sid =sid, line =linetomodify).oname,
            'descr' : Instruction.objects.get(sid =sid, line =linetomodify).descr,
            'exc' : Instruction.objects.get(sid =sid, line =linetomodify).exc,
            'degr' : Instruction.objects.get(sid =sid, line =linetomodify).degr,
            })

            REM_CHOICES =('',''),
            bibliolist =[]
            if Instruction.objects.filter(sid =sid).exclude(name =Library.objects.get(lid =lid).name).exclude(name ='checker'):
                for e in Instruction.objects.filter(sid =sid).exclude(name =Library.objects.get(lid =lid).name).exclude(name ='checker'):
                    if (e.exc or e.degr) and Library.objects.get(name =e.name).name not in bibliolist:
                        bibliolist.append(Library.objects.get(name =e.name).name)
                bibliolist.sort()
                length =len(bibliolist)
            if length:
                for l in bibliolist:
                    REM_CHOICES += (l, l),

            class Instr_Form(forms.Form):
                oname = forms.ChoiceField(required = False, widget=forms.Select\
                (attrs={'title': _("Intitulé de la bibliothèque ayant précédemment déclaré une 'exception' ou un 'améliorable'")})\
                , choices=REM_CHOICES, initial =Instruction.objects.get(sid =sid, line =linetomodify).\
                oname, label =_("Bibliothèque remédiée"),)

            foname = Instr_Form()

            instrlist = Instruction.objects.filter(sid = sid).order_by('line')

    return render(request, 'epl/modinstruction.html', { 'ressource' : ress, \
    'library' : lib, 'instructions' : instrlist , 'form' : f, 'foname' : foname, 'librarylist' : \
    liblist, 'remedied_lib_list' : remliblist, 'sid' : sid, 'stage' : bd, 'info' : info, \
    'lid' : lid, 'expected' : q, 'k' : k, 'version' : version, 'l' : length, 'line' : linetomodify, })


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
                j = Instruction.objects.get(sid =sid, bound = expected, name =lib.name, line =todel)
            except:
                answer = _(" <=== Expression invalide (vérifiez les conditions indiquées) ")
        if answer == "":
            for todel in linestodel:
                Instruction.objects.get(sid =sid, name =lib.name, line =todel).delete()
            url ="/add/" + str(sid) + "/" + str(lid)
            return HttpResponseRedirect(url) # Renumbering shall be done there.

    instrlist = Instruction.objects.filter(sid = sid).order_by('line')

    #Library list ordered by 'rank' to get from the precedent item list above :
    liblist = []
    for e in itemlist:
        liblist.append(Library.objects.get(lid = e.lid))
    liblist.append(Library.objects.get(name = 'checker'))

    return render(request, 'epl/delinstruction.html', { 'ressource' : ress, \
    'library' : lib, 'instructions' : instrlist , 'form' : f, 'librarylist' : \
    liblist, 'remedied_lib_list' : remliblist, 'sid' : sid, 'stage' : bd, 'info' : info, \
    'lid' : lid, 'expected' : expected, 'answer' : answer, 'k' : k, 'version' : version, })


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
                    " :\n" + "https://" + host + "/add/" + str(sid) + '/' + str(nextlid)
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
            " :\n" + "https://" + host + "/add/" + str(sid) + '/' + str(nextlid)
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

    return render(request, 'epl/endinstruction.html', { 'ressource' : ress, \
    'library' : lib, 'instructions' : instrlist , 'librarylist' : \
    liblist, 'remedied_lib_list' : remliblist, 'sid' : sid, 'stage' : bd, 'info' : info, \
    'lid' : lid, 'checkform' : z, 'checkerform' : u, 'expected' : expected, 'k' : k, 'version' : version, })


def ranktotake(request, lid, sort):

    k = logstatus(request)
    version =epl_version

    global client_ip, idfeature, idview, dil
    client_ip, idfeature, idview, dil =request.META['REMOTE_ADDR'], 1, 0, lid

    if sort =='sid':
        reclist = list(ItemRecord.objects.filter(lid = lid, rank = 99).order_by('sid'))
    elif sort =='cn':
        reclist = list(ItemRecord.objects.filter(lid = lid, rank = 99).order_by('cn', 'title'))
    else:
        reclist = list(ItemRecord.objects.filter(lid = lid, rank = 99).order_by('title'))

    resslist = []
    for e in reclist:
        itemlist = list(ItemRecord.objects.filter(sid = e.sid).exclude(rank =0))
        if len(itemlist) > 1:
            resslist.append(e)
    l = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name

    nlib = len(Library.objects.exclude(lid ="999999999"))

    return render(request, 'epl/to_rank_list.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'l' : l, 'k' : k, 'nlib' : nlib, \
    'lastrked' : lastrked, 'version' : version, 'sort' : sort, })


def modifranklist(request, lid, sort):

    k = logstatus(request)
    version =epl_version

    # global client_ip, idfeature, idview, dil
    # client_ip, idfeature, idview, dil =request.META['REMOTE_ADDR'], 1, 2, lid
    # cf. remarque dans la vue router(request)

    # reclist = list(ItemRecord.objects.filter(lid = lid, status =0).exclude(rank = 99))
    if sort =='sid':
        reclist = list(ItemRecord.objects.filter(lid = lid).exclude(rank = 99)\
        .exclude(status =2).exclude(status =3).exclude(status =4).\
        exclude(status =5).exclude(status =6).order_by('sid'))
    elif sort =='cn':
        reclist = list(ItemRecord.objects.filter(lid = lid).exclude(rank = 99)\
        .exclude(status =2).exclude(status =3).exclude(status =4).\
        exclude(status =5).exclude(status =6).order_by('cn', 'title'))
    else:
        reclist = list(ItemRecord.objects.filter(lid = lid).exclude(rank = 99)\
        .exclude(status =2).exclude(status =3).exclude(status =4).\
        exclude(status =5).exclude(status =6).order_by('title'))

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

    return render(request, 'epl/modifrklist.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'l' : l, 'k' : k, 'nlib' : nlib, \
    'lastrked' : lastrked, 'version' : version, 'sort' : sort, })


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
        return xranktotake(request, lid, xlid, 'title')

    return render(request, 'epl/filter_rklist.html', locals())


def xranktotake(request, lid, xlid, sort):

    k = logstatus(request)
    version =epl_version

    global client_ip, idfeature, idview, dil, dilx
    client_ip, idfeature, idview, dil, dilx =request.META['REMOTE_ADDR'], 1, 1, lid, xlid

    #Getting ressources whose this lid must but has not yet taken rank :
    if sort =='sid':
        reclist = list(ItemRecord.objects.filter(lid = lid, rank = 99).order_by('sid'))
    elif sort =='cn':
        reclist = list(ItemRecord.objects.filter(lid = lid, rank = 99).order_by('cn', 'title'))
    else:
        reclist = list(ItemRecord.objects.filter(lid = lid, rank = 99).order_by('title'))

    resslist = []
    for e in reclist:
        itemlist = list(ItemRecord.objects.filter(sid = e.sid).exclude(rank =0))
        if len(itemlist) > 1 and list(ItemRecord.objects.filter(sid = e.sid, lid = xlid).exclude(rank =0)):
            resslist.append(e)
    l = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name
    xlibname = Library.objects.get(lid =xlid).name

    return render(request, 'epl/xto_rank_list.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'l' : l, 'k' : k, 'xlibname' : xlibname, \
    'lastrked' : lastrked, 'version' : version, 'sort' : sort, 'xlid' : xlid, })


def arbitration(request, lid, sort):

    k = logstatus(request)
    version =epl_version

    global client_ip, idfeature, idview, dil
    client_ip, idfeature, idview, dil =request.META['REMOTE_ADDR'], 2, 0, lid

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

    if sort =='sid':
        resslist = sorted(resslist, key=serial_id)
    elif sort =='cn':
        resslist = sorted(resslist, key=coll_cn)
    else:
        resslist = sorted(resslist, key=serial_title)

    size = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name

    nlib = len(Library.objects.exclude(lid ="999999999"))


    return render(request, 'epl/arbitration.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'size' : size, 'k' : k, \
    'lastrked' : lastrked, 'version' : version, 'nlib' : nlib, 'sort' : sort, })


def arbrk1(request, lid, sort):

    k = logstatus(request)
    version =epl_version

    global client_ip, idfeature, idview, dil
    client_ip, idfeature, idview, dil =request.META['REMOTE_ADDR'], 2, 4, lid

    #For the lid identified library, getting ressources whose at \
    #least 2 libraries, including the considered one, took rank =1 \
    #(even if other libraries have not yet taken rank)
    #or all libraries have taken rank, none of them the rank 1

    #Initialization of the ressources to arbitrate :
    resslist = []

    if sort =='sid':
        reclist = list(ItemRecord.objects.filter(lid =lid, rank = 1, status =0).order_by('sid'))
    elif sort =='cn':
        reclist = list(ItemRecord.objects.filter(lid =lid, rank = 1, status =0).order_by('cn', 'title'))
    else:
        reclist = list(ItemRecord.objects.filter(lid =lid, rank = 1, status =0).order_by('title'))

    for e in reclist:
        sid = e.sid
        if ItemRecord.objects.exclude(lid =lid).filter(sid =sid, rank = 1):
            resslist.append(e)

    size = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/arbrk1.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'size' : size, 'k' : k, \
    'lastrked' : lastrked, 'version' : version, 'sort' : sort, })


def arbnork1(request, lid, sort):

    k = logstatus(request)
    version =epl_version

    global client_ip, idfeature, idview, dil
    client_ip, idfeature, idview, dil =request.META['REMOTE_ADDR'], 2, 2, lid

    #For the lid identified library, getting ressources whose at \
    #least 2 libraries, including the considered one, took rank =1 \
    #(even if other libraries have not yet taken rank)
    #or all libraries have taken rank, none of them the rank 1

    #Initialization of the ressources to arbitrate :
    resslist = []

    if sort =='sid':
        reclist = list(ItemRecord.objects.filter(lid =lid, status =0).exclude(rank =1).exclude(rank =0).exclude(rank =99).order_by('sid'))
    elif sort =='cn':
        reclist = list(ItemRecord.objects.filter(lid =lid, status =0).exclude(rank =1).exclude(rank =0).exclude(rank =99).order_by('cn', 'title'))
    else:
        reclist = list(ItemRecord.objects.filter(lid =lid, status =0).exclude(rank =1).exclude(rank =0).exclude(rank =99).order_by('title'))

    for e in reclist:
        sid = e.sid
        if len(ItemRecord.objects.filter(sid =sid, rank =1)) ==0 and \
        len(ItemRecord.objects.filter(sid =sid, rank =99)) ==0 and \
        len(ItemRecord.objects.filter(sid =sid).exclude(rank =0)) >1:
            resslist.append(e)

    size = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/arbnork1.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'size' : size, 'k' : k, \
    'lastrked' : lastrked, 'version' : version, 'sort' : sort, })


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
        return xarbitration(request, lid, xlid, 'title')

    return render(request, 'epl/filter_arblist.html', locals())


def xarbitration(request, lid, xlid, sort):

    k = logstatus(request)
    version =epl_version

    global client_ip, idfeature, idview, dil, dilx
    client_ip, idfeature, idview, dil, dilx =request.META['REMOTE_ADDR'], 2, 1, lid, xlid

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

    l = resslista + resslistb

    if sort =='sid':
        resslist = sorted(l, key=serial_id)
    elif sort =='cn':
        resslist = sorted(l, key=coll_cn)
    else:
        resslist = sorted(l, key=serial_title)

    size = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name
    xlibname = Library.objects.get(lid =xlid).name


    return render(request, 'epl/xarbitration.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'size' : size, 'k' : k, 'xlibname' : xlibname, \
    'xlid' : xlid, 'lastrked' : lastrked, 'version' : version, 'sort' : sort, })


def x1arb(request, lid, xlid, sort):

    k = logstatus(request)
    version =epl_version

    global client_ip, idfeature, idview, dil, dilx
    client_ip, idfeature, idview, dil, dilx =request.META['REMOTE_ADDR'], 2, 2, lid, xlid

    #For the lid identified library, getting ressources whose at \
    #least 2 libraries, including the considered one, took rank =1 \
    #(even if other libraries have not yet taken rank)
    #or all libraries have taken rank, none of them the rank 1

    #Initialization of the ressources to arbitrate :
    resslist = []

    if sort =='sid':
        reclist = list(ItemRecord.objects.filter(lid =lid, rank = 1, status =0).order_by('sid'))
    elif sort =='cn':
        reclist = list(ItemRecord.objects.filter(lid =lid, rank = 1, status =0).order_by('cn', 'title'))
    else:
        reclist = list(ItemRecord.objects.filter(lid =lid, rank = 1, status =0).order_by('title'))

    for e in reclist:
        sid = e.sid
        if ItemRecord.objects.filter(sid =sid, lid = xlid, rank = 1):
            resslist.append(e)

    size = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name
    xlibname = Library.objects.get(lid =xlid).name


    return render(request, 'epl/x1arbitration.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'size' : size, 'k' : k, 'xlibname' : xlibname, \
    'lastrked' : lastrked, 'version' : version, 'sort' : sort, 'xlid' : xlid, })


def x0arb(request, lid, xlid, sort):

    k = logstatus(request)
    version =epl_version

    global client_ip, idfeature, idview, dil, dilx
    client_ip, idfeature, idview, dil, dilx =request.META['REMOTE_ADDR'], 2, 3, lid, xlid

    #For the lid identified library, getting ressources whose at \
    #least 2 libraries, including the considered one, took rank =1 \
    #(even if other libraries have not yet taken rank)
    #or all libraries have taken rank, none of them the rank 1

    #Initialization of the ressources to arbitrate :
    resslist = []

    if sort =='sid':
        reclist = list(ItemRecord.objects.filter(lid =lid, status =0).exclude(rank =1).exclude(rank =0).exclude(rank =99).order_by('sid'))
    elif sort =='cn':
        reclist = list(ItemRecord.objects.filter(lid =lid, status =0).exclude(rank =1).exclude(rank =0).exclude(rank =99).order_by('cn', 'title'))
    else:
        reclist = list(ItemRecord.objects.filter(lid =lid, status =0).exclude(rank =1).exclude(rank =0).exclude(rank =99).order_by('title'))

    for e in reclist:
        sid = e.sid
        if len(ItemRecord.objects.filter(sid =sid, rank =1)) ==0 and \
        len(ItemRecord.objects.filter(sid =sid, rank =99)) ==0 and \
        len(ItemRecord.objects.filter(sid =sid).exclude(rank =0)) >1:
            resslist.append(e)

    size = len(resslist)

    #Library name :
    libname = Library.objects.get(lid =lid).name
    xlibname = Library.objects.get(lid =xlid).name


    return render(request, 'epl/x0arbitration.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'size' : size, 'k' : k, 'xlibname' : xlibname, \
    'lastrked' : lastrked, 'version' : version, 'sort' : sort, 'xlid' : xlid, })


def instrtodo(request, lid, sort):

    k = logstatus(request)
    version =epl_version

    global client_ip, idfeature, idview, dil
    client_ip, idfeature, idview, dil =request.META['REMOTE_ADDR'], 3, 0, lid

    if lid !="999999999":
        # Ressources whose the lid identified library has to deal with (status =1 or 3)
        if sort =='sid':
            l = list(ItemRecord.objects.filter(lid =lid).exclude(status =0).exclude(status =2).\
            exclude(status =4).exclude(status =5).exclude(status =6).order_by('sid'))
        elif sort =='cn':
            l = list(ItemRecord.objects.filter(lid =lid).exclude(status =0).exclude(status =2).\
            exclude(status =4).exclude(status =5).exclude(status =6).order_by('cn', 'title'))
        else:
            l = list(ItemRecord.objects.filter(lid =lid).exclude(status =0).exclude(status =2).\
            exclude(status =4).exclude(status =5).exclude(status =6).order_by('title'))

    elif lid =="999999999":

        l = []

        for e in ItemRecord.objects.filter(status =2, rank =1):
            if len(ItemRecord.objects.filter(sid =e.sid, status =2)) == len(ItemRecord.objects.filter(sid =e.sid).exclude(rank =0)) and len(Instruction.objects.filter(sid =e.sid, name= "checker")) ==0:
                l.append(ItemRecord.objects.get(sid =e.sid, rank =1)) #yehh ... rank =1 that's the trick !

        for e in ItemRecord.objects.filter(status =4, rank =1):
            if len(ItemRecord.objects.filter(sid =e.sid, status =4)) == len(ItemRecord.objects.filter(sid =e.sid).exclude(rank =0)) and len(Instruction.objects.filter(sid =e.sid, name= "checker")) ==1:
                l.append(ItemRecord.objects.get(sid =e.sid, rank =1)) #yehh ... rank =1 that's the trick !

    if sort =='sid':
        l = sorted(l, key=serial_id)
    elif sort =='cn':
        l = sorted(l, key=coll_cn)
    else:
        l = sorted(l, key=serial_title)

    size = len(l)

    #Getting library name :
    libname = Library.objects.get(lid =lid).name

    nlib = len(Library.objects.exclude(lid ="999999999"))

    lidchecker = "999999999"

    return render(request, 'epl/instrtodo.html', locals())


def instroneb(request, lid, sort):

    k = logstatus(request)
    version =epl_version

    if lid !="999999999":
        # Ressources whose the lid identified library has rank =1 and has to deal with bound elements (status =1)
        if sort =='sid':
            l = list(ItemRecord.objects.filter(lid =lid, rank =1).exclude(status =0).exclude(status =2).exclude(status =3)\
            .exclude(status =4).exclude(status =5).exclude(status =6).order_by('sid'))
        elif sort =='cn':
            l = list(ItemRecord.objects.filter(lid =lid, rank =1).exclude(status =0).exclude(status =2).exclude(status =3)\
            .exclude(status =4).exclude(status =5).exclude(status =6).order_by('cn', 'title'))
        else:
            l = list(ItemRecord.objects.filter(lid =lid, rank =1).exclude(status =0).exclude(status =2).exclude(status =3)\
            .exclude(status =4).exclude(status =5).exclude(status =6).order_by('title'))

    elif lid =="999999999":
        do = home(request)
        return do

    size = len(l)

    #Getting library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/instrtodobd1.html', locals())


def instrotherb(request, lid, sort):

    k = logstatus(request)
    version =epl_version

    if lid !="999999999":
        # Ressources whose the lid identified library has rank !=1 and has to deal with bound elements (status =1)
        if sort =='sid':
            l = list(ItemRecord.objects.filter(lid =lid).exclude(rank =1).\
            exclude(status =0).exclude(status =2).exclude(status =3).exclude(status =4)\
            .exclude(status =5).exclude(status =6).order_by('sid'))
        elif sort =='cn':
            l = list(ItemRecord.objects.filter(lid =lid).exclude(rank =1).\
            exclude(status =0).exclude(status =2).exclude(status =3).exclude(status =4)\
            .exclude(status =5).exclude(status =6).order_by('cn', 'title'))
        else:
            l = list(ItemRecord.objects.filter(lid =lid).exclude(rank =1).\
            exclude(status =0).exclude(status =2).exclude(status =3).exclude(status =4)\
            .exclude(status =5).exclude(status =6).order_by('title'))

    elif lid =="999999999":
        do = home(request)
        return do

    size = len(l)

    #Getting library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/instrtodobdnot1.html', locals())


def instronenotb(request, lid, sort):

    k = logstatus(request)
    version =epl_version

    if lid !="999999999":
        # Ressources whose the lid identified library has rank =1 and has to deal with not bound elements (status =3)
        if sort =='sid':
            l = list(ItemRecord.objects.filter(lid =lid, rank =1).exclude(status =0).\
            exclude(status =1).exclude(status =2).exclude(status =4).exclude(status =5).exclude(status =6).order_by('sid'))
        elif sort =='cn':
            l = list(ItemRecord.objects.filter(lid =lid, rank =1).exclude(status =0).\
            exclude(status =1).exclude(status =2).exclude(status =4).exclude(status =5).exclude(status =6).order_by('cn', 'title'))
        else:
            l = list(ItemRecord.objects.filter(lid =lid, rank =1).exclude(status =0).\
            exclude(status =1).exclude(status =2).exclude(status =4).exclude(status =5).exclude(status =6).order_by('title'))

    elif lid =="999999999":
        do = home(request)
        return do

    size = len(l)

    #Getting library name :
    libname = Library.objects.get(lid =lid).name

    return render(request, 'epl/instrtodonotbd1.html', locals())


def instrothernotb(request, lid, sort):

    k = logstatus(request)
    version =epl_version

    if lid !="999999999":
        # Ressources whose the lid identified library has rank !=1 and has to deal with not bound elements (status =3)
        if sort =='sid':
            l = list(ItemRecord.objects.filter(lid =lid).exclude(rank =1).exclude(status =0).\
            exclude(status =1).exclude(status =2).exclude(status =4).exclude(status =5).exclude(status =6).order_by('sid'))
        elif sort =='cn':
            l = list(ItemRecord.objects.filter(lid =lid).exclude(rank =1).exclude(status =0).\
            exclude(status =1).exclude(status =2).exclude(status =4).exclude(status =5).exclude(status =6).order_by('cn', 'title'))
        else:
            l = list(ItemRecord.objects.filter(lid =lid).exclude(rank =1).exclude(status =0).\
            exclude(status =1).exclude(status =2).exclude(status =4).exclude(status =5).exclude(status =6).order_by('title'))

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
        return xinstrlist(request, lid, xlid, 'title')
    return render(request, 'epl/filter_instrlist.html', locals())


def xinstrlist(request, lid, xlid, sort):

    k = logstatus(request)
    version =epl_version

    if lid =="999999999":
        return notintime(request, "-?-", lid)

    global client_ip, idfeature, idview, dil, dilx
    client_ip, idfeature, idview, dil, dilx =request.META['REMOTE_ADDR'], 3, 1, lid, xlid

    name = Library.objects.get(lid =lid).name
    xname = Library.objects.get(lid =xlid).name

    if sort =='sid':
        lprov = list(ItemRecord.objects.filter(lid =lid).exclude(status =0).exclude(status =2).\
        exclude(status =4).exclude(status =5).exclude(status =6).order_by('sid'))
    elif sort =='cn':
        lprov = list(ItemRecord.objects.filter(lid =lid).exclude(status =0).exclude(status =2).\
        exclude(status =4).exclude(status =5).exclude(status =6).order_by('cn', 'title'))
    else:
        lprov = list(ItemRecord.objects.filter(lid =lid).exclude(status =0).exclude(status =2).\
        exclude(status =4).exclude(status =5).exclude(status =6).order_by('title'))

    l =[]
    for e in lprov:
        if ItemRecord.objects.filter(lid =xlid).exclude(rank =0):
            l.append(e)

    size = len(l)

    return render(request, 'epl/xto_instr_list.html', locals())


def tobeedited(request, lid, sort):

    k = logstatus(request)
    version =epl_version

    global client_ip, idfeature, idview, dil
    client_ip, idfeature, idview, dil =request.META['REMOTE_ADDR'], 4, 0, lid

    #For the lid identified library, getting ressources whose the resulting \
    #collection has been entirely completed and may consequently be edited.
    #Trick : These ressources have two instructions with name = 'checker' :

    if sort =='sid':
        l = list(ItemRecord.objects.filter(lid =lid).exclude(rank =0).order_by('sid'))
    elif sort =='cn':
        l = list(ItemRecord.objects.filter(lid =lid).exclude(rank =0).order_by('cn', 'title'))
    else:
        l = list(ItemRecord.objects.filter(lid =lid).exclude(rank =0).order_by('title'))

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


def mothered(request, lid, sort):

    k = logstatus(request)
    version =epl_version

    global client_ip, idfeature, idview, dil
    client_ip, idfeature, idview, dil =request.META['REMOTE_ADDR'], 4, 1, lid

    #For the lid identified library, getting ressources whose the resulting \
    #collection has been entirely completed and may consequently be edited.
    #Trick : These ressources have two instructions with name = 'checker' :

    if sort =='sid':
        l = list(ItemRecord.objects.filter(lid =lid, rank =1).order_by('sid'))
    elif sort =='cn':
        l = list(ItemRecord.objects.filter(lid =lid, rank =1).order_by('cn', 'title'))
    else:
        l = list(ItemRecord.objects.filter(lid =lid, rank =1).order_by('title'))

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


def notmothered(request, lid, sort):

    k = logstatus(request)
    version =epl_version

    global client_ip, idfeature, idview, dil
    client_ip, idfeature, idview, dil =request.META['REMOTE_ADDR'], 4, 2, lid

    #For the lid identified library, getting ressources whose the resulting \
    #collection has been entirely completed and may consequently be edited.
    #Trick : These ressources have two instructions with name = 'checker' :

    if sort =='sid':
        l = list(ItemRecord.objects.filter(lid =lid).exclude(rank =1).exclude(rank =0).exclude(rank =99).order_by('sid'))
    elif sort =='cn':
        l = list(ItemRecord.objects.filter(lid =lid).exclude(rank =1).exclude(rank =0).exclude(rank =99).order_by('cn', 'title'))
    else:
        l = list(ItemRecord.objects.filter(lid =lid).exclude(rank =1).exclude(rank =0).exclude(rank =99).order_by('title'))

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
                return mothered(request, lid, 'title')
            else:
                return notmothered(request, lid, 'title')
        else: # lid != xlid
            if rank =="a":
                return xmothered(request, lid, xlid, 'title')
            else:
                return xnotmothered(request, lid, xlid, 'title')

    return render(request, 'epl/filter_edlist.html', locals())


def xmothered(request, lid, xlid, sort):

    k = logstatus(request)
    version =epl_version

    global client_ip, idfeature, idview, dil, dilx
    client_ip, idfeature, idview, dil, dilx =request.META['REMOTE_ADDR'], 4, 3, lid, xlid

    if sort =='sid':
        l = list(ItemRecord.objects.filter(lid =lid, rank =1).order_by('sid'))
    elif sort =='cn':
        l = list(ItemRecord.objects.filter(lid =lid, rank =1).order_by('cn', 'title'))
    else:
        l = list(ItemRecord.objects.filter(lid =lid, rank =1).order_by('title'))

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


def xnotmothered(request, lid, xlid, sort):

    k = logstatus(request)
    version =epl_version

    global client_ip, idfeature, idview, dil, dilx
    client_ip, idfeature, idview, dil, dilx =request.META['REMOTE_ADDR'], 4, 4, lid, xlid

    if sort =='sid':
        l = list(ItemRecord.objects.filter(lid =lid).exclude(rank =1).exclude(rank =0).exclude(rank =99).order_by('sid'))
    elif sort =='cn':
        l = list(ItemRecord.objects.filter(lid =lid).exclude(rank =1).exclude(rank =0).exclude(rank =99).order_by('cn', 'title'))
    else:
        l = list(ItemRecord.objects.filter(lid =lid).exclude(rank =1).exclude(rank =0).exclude(rank =99).order_by('title'))

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

    global client_ip, idfeature, idview, tes_lloc
    client_ip, idfeature, idview, tes_lloc =request.META['REMOTE_ADDR'], 3, 2, coll_set

    l = []

    reclist = list(ItemRecord.objects.filter(status =2, rank =1).order_by('title'))

    for e in reclist:
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

    global client_ip, idfeature, idview, tes_lloc
    client_ip, idfeature, idview, tes_lloc =request.META['REMOTE_ADDR'], 3, 3, coll_set

    l = []

    reclist = list(ItemRecord.objects.filter(status =4, rank =1).order_by('title'))

    for e in reclist:
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

    global client_ip, idfeature, idview, tes_lloc
    client_ip, idfeature, idview, tes_lloc =request.META['REMOTE_ADDR'], 3, 4, coll_set

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

    l = sorted(l, key=serial_title)

    size = len(l)

    return render(request, 'epl/xckall.html', locals())
