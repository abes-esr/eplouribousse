epl_version ="v1.20.0 (Wulfégonde)"
date_version ="March 23, 2021"
# Mise au niveau de :
epl_version ="v1.21-beta.2 (~Berchilde)"
date_version ="April 16, 2021"
#branche = multi

from django.shortcuts import render

from .models import *

from .forms import *

from django.core.mail import send_mail

from django.db.models.functions import Now

from django.contrib.auth.decorators import login_required

from django.utils.translation import ugettext as _

from django.contrib.auth.models import User

from django.contrib.auth import logout

from django.http import HttpResponseRedirect, HttpResponse


lastrked =None
webmaster =""
try:
    webmasterstr = ReplyMail.objects.all().order_by('pk')[1].sendermail
    zz =1
except:
    pass

try:
    replymail =ReplyMail.objects.all().order_by('pk')[0].sendermail
except:
    replymail =BddAdmin.objects.all().order_by('pk')[0].contact


def serial_title(e):
    """sorting by title"""
    return e.title
def serial_id(e):
    """sorting by sid"""
    return e.sid
def coll_cn(e):
    """sorting by cn, title"""
    return (e.cn, e.title)


def selectbdd(request):

    version =epl_version
    i, k =0, 1
    BDD_CHOICES =('',_('Sélectionnez votre projet')),

    while k ==1:
        try:
            BDD_CHOICES += ('{:02d}'.format(i), Project.objects.using('{:02d}'.format(i)).all().order_by('pk')[0].name),
            i +=1
        except:
            k =0
    # BDD_CHOICES =BDD_CHOICES[1:]

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

    return render(request, 'epl/selectbdd.html', locals())


def logstatus(request):
    if request.user.is_authenticated:
        k = request.user.get_username()
    else:
        k =0
    return k


def home(request, bdd):

    k =logstatus(request)
    version =epl_version

    "Homepage"

    project = Project.objects.using(bdd).all().order_by('pk')[0].name

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
        if not Feature.objects.using(bdd).filter(feaname =feature, libname =i.libname):
            i.save(using=bdd)

        if lid =="999999999":
            if feature =='instrtodo':
                return instrtodo(request, bdd, lid, 'title')
            else:
                return checkinstr(request, bdd)
        else:
            if feature =='ranking':
                return ranktotake(request, bdd, lid, 'title')
            elif feature =='arbitration':
                return arbitration(request, bdd, lid, 'title')
            elif feature =='instrtodo':
                return instrtodo(request, bdd, lid, 'title')
            elif feature =='edition':
                return tobeedited(request, bdd, lid, 'title')

    return render(request, 'epl/home.html', locals())


def about(request, bdd):

    k =logstatus(request)
    version =epl_version
    date =date_version
    host = str(request.get_host())
    return render(request, 'epl/about.html', locals())


def contact(request, bdd):

    k =logstatus(request)
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




def webmstr(request, bdd):

    k =logstatus(request)
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
            message2 = "Votre message a bien été envoyé au webmaster"\
             + ".\n" + "Ne répondez pas au présent message s'il vous plaît" + ".\n" + \
             "Rappel de l'objet de votre message" + " : " + subject2 + \
             "\n" + "Rappel de votre message" + " :\n" + "\n" + \
             _("***** Début *****") + "\n" + body + "\n" + _("*****  Fin  *****")
            dest1 = [wbmstr]
            dest2 = [recipient]
            send_mail(subject1, message1, recipient, dest1, fail_silently=True, )
            send_mail(subject2, message2, replymail, dest2, fail_silently=True, )
            return render(request, 'epl/confirmation.html', locals())
        else:
            info =_("Attention : Les adresses doivent être identiques") + "."
    else:
        if request.method =="POST":
            info =_("Vérifier que les adresses sont correctes") + "."

    return render(request, 'epl/webmaster.html', locals())


def confirm(request, bdd):

    k =logstatus(request)
    version =epl_version

    return render(request, 'epl/confirmation.html', locals())


def router(request, bdd, lid):

    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        return home(request, bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
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

    return render(request, 'epl/router.html', locals())


def lang(request, bdd):
    k =logstatus(request)
    version =epl_version

    return render(request, 'epl/language.html', locals())


def logout_view(request, bdd):

    "Homepage special disconnected"

    logout(request)

    # Redirect to a success page.

    version =epl_version

    project = Project.objects.using(bdd).all().order_by('pk')[0].name

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
        if not Feature.objects.using(bdd).filter(feaname =feature, libname =i.libname):
            i.save(using=bdd)

        if lid =="999999999":
            if feature =='instrtodo':
                return instrtodo(request, bdd, lid, 'title')
            else:
                return checkinstr(request, bdd)
        else:
            if feature =='ranking':
                return ranktotake(request, bdd, lid, 'title')
            elif feature =='arbitration':
                return arbitration(request, bdd, lid, 'title')
            elif feature =='instrtodo':
                return instrtodo(request, bdd, lid, 'title')
            elif feature =='edition':
                return tobeedited(request, bdd, lid, 'title')

    return render(request, 'epl/disconnect.html', locals())


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

    #number of libraries :
    nlib = len(Library.objects.using(bdd).all())

    #Exclusions details
    dict ={}
    EXCLUSION_CHOICES = ('', ''),
    for e in Exclusion.objects.using(bdd).all().order_by('label'):
        EXCLUSION_CHOICES += (e.label, e.label),
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

    #Collections involved in arbitration for 1st rank not claimed by any of the libraries
    cnone, snone =0,[]
    for i in ItemRecord.objects.using(bdd).exclude(rank =0).exclude(rank =1).exclude(rank =99):
        if len(ItemRecord.objects.using(bdd).filter(sid =i.sid, rank =99)) ==0 and \
        len(ItemRecord.objects.using(bdd).filter(sid =i.sid, rank =1)) ==0 and \
        len(ItemRecord.objects.using(bdd).filter(sid =i.sid).exclude(rank =0)) >1:
            cnone +=1
            if i.sid not in snone:
                snone.append(i.sid)
    snone = len(snone)

    #Collections involved in arbitration for any of the two reasons and number of serials concerned
    ctotal = c1st + cnone
    stotal = s1st + snone

    #Number of collections :
    coll = len(ItemRecord.objects.using(bdd).all())

    #Number of potential candidates :
    cand =[]
    for e in ItemRecord.objects.using(bdd).all():
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid)) >1 and not e.sid in cand:
            cand.append(e.sid)
    cand = len(cand)

    #from which strict duplicates :
    dupl =[]
    for e in ItemRecord.objects.using(bdd).all():
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid)) ==2 and not e.sid in dupl:
            dupl.append(e.sid)
    dupl = len(dupl)

    #triplets :
    tripl =[]
    for e in ItemRecord.objects.using(bdd).all():
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid)) ==3 and not e.sid in tripl:
            tripl.append(e.sid)
    tripl = len(tripl)

    #quadruplets :
    qudrpl =[]
    for e in ItemRecord.objects.using(bdd).all():
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid)) ==4 and not e.sid in qudrpl:
            qudrpl.append(e.sid)
    qudrpl = len(qudrpl)

    #Unicas :
    isol =[]
    for e in ItemRecord.objects.using(bdd).all():
        if len(ItemRecord.objects.using(bdd).filter(sid =e.sid)) ==1 and not e.sid in isol:
            isol.append(e.sid)
    isol = len(isol)

    #candidate collections :
    candcoll =coll - isol

    #Number of descarded ressources for exclusion reason :
    discard =[]
    for i in ItemRecord.objects.using(bdd).filter(rank =0):
        if len(ItemRecord.objects.using(bdd).filter(sid =i.sid).exclude(rank =0)) ==1 and not i.sid in discard:
            discard.append(i.sid)
    discard = len(discard)

    #Number of real candidates (collections)
    realcandcoll =candcoll - (exclus + discard)

    #Number of ressources whose instruction of bound elements may begin :
    bdmaybeg = len(ItemRecord.objects.using(bdd).filter(rank =1, status =1))

    #Number of ressources whose bound elements are currently instructed  :
    bdonway = len(ItemRecord.objects.using(bdd).filter(rank =1, status =2))

    #Number of ressources whose instruction of not bound elements may begin :
    notbdmaybeg = len(ItemRecord.objects.using(bdd).filter(rank =1, status =3))

    #Number of ressources whose not bound elements are currently instructed  :
    notbdonway = len(ItemRecord.objects.using(bdd).filter(rank =1, status =4))

    #Number of ressources completely instructed :
    fullinstr = len(ItemRecord.objects.using(bdd).filter(rank =1, status =5))

    #Number of failing sheets :
    fail = len(ItemRecord.objects.using(bdd).filter(status =6, rank =1))

    #Number of instructions :
    instr = len(Instruction.objects.using(bdd).all())

    #Fiches incomplètement instruites, défectueuses ou dont le traitement peut débuter mais n'a pas débuté
    incomp = bdmaybeg + bdonway + notbdmaybeg + notbdonway + fail

    #Ressources pour lesquelles le positionnement doit être complété (hors arbitrage)
    stocomp =[]
    for i in ItemRecord.objects.using(bdd).filter(rank =99):
        if len(ItemRecord.objects.using(bdd).filter(sid =i.sid).exclude(rank =0)) >1 and not i.sid in stocomp:
            stocomp.append(i.sid)
    stocomp = len(stocomp)

    #Number of real candidates (ressources)
    realcand =stocomp + incomp + fullinstr

    #Absolute achievement :
    absolute_real = round(10000*(fullinstr + discard)/cand)/100

    #Relative achievement :
    relative_real = round(10000*fullinstr/realcand)/100

    return render(request, 'epl/indicators.html', locals())


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
                    action, laction =_("Edition de la fiche de résultante"), "/ed/" + str(sid) + "/" + str(lid)
            elif higher_status ==4:
                if len(ItemRecord.objects.using(bdd).filter(sid =sid, status =4)) ==len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)):
                    progress =_("En attente de validation finale par le contrôleur")
                    if lid =="999999999":
                        action, laction =_("Validation finale"), "/end/" + str(sid) + "/" + str(lid)
                else:
                    if lid !="999999999":
                        if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid, status =3):
                            if Instruction.objects.using(bdd).filter(sid =sid, bound =" ", name =Library.objects.using(bdd).get(lid =lid).name):
                                progress =_("Instruction des non reliés en cours pour votre collection")
                            else:
                                progress =_("Instruction des non reliés à débuter pour votre collection")
                            action, laction =_("Instruction"), "/add/" + str(sid) + "/" + str(lid)
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
                        action, laction =_("Instruction"), "/add/" + str(sid) + "/" + str(lid)
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
                        action, laction =_("Validation intermédiaire"), "/end/" + str(sid) + "/" + str(lid)
                else:
                    if lid !="999999999":
                        if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid, status =1):
                            if Instruction.objects.using(bdd).filter(sid =sid, bound ="x", name =Library.objects.using(bdd).get(lid =lid).name):
                                progress =_("Instruction des reliés en cours pour votre collection")
                            else:
                                progress =_("Instruction des reliés à débuter pour votre collection")
                            action, laction =_("Instruction"), "/add/" + str(sid) + "/" + str(lid)
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
                        action, laction =_("Instruction"), "/add/" + str(sid) + "/" + str(lid)
                    else:
                        xname =Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =sid, status =1).lid).name
                        if Instruction.objects.using(bdd).filter(sid =sid, bound ="x", name =xname):
                            progress =_("Instruction des reliés en cours pour : ")
                        else:
                            progress =_("Instruction des reliés en cours ; à débuter pour : ")
                    if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid) and len(Instruction.objects.using(bdd).filter(sid =sid)) ==0:
                        alteraction, lalteraction =_("Modification éventuelle du rang de votre collection"), "/rk/" + str(sid) + "/" + str(lid)
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
                             action, laction =_("Repositionnement éventuel de votre collection"), "/rk/" + str(sid) + "/" + str(lid)
                    elif ItemRecord.objects.using(bdd).filter(sid =sid, rank =99) and len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) >1:
                        if ItemRecord.objects.using(bdd).filter(sid =sid, rank =99, lid =lid):
                            progress =_("Positionnement à compléter pour votre collection")
                            action, laction =_("Positionnement de votre collection"), "/rk/" + str(sid) + "/" + str(lid)
                        else:
                            progress =_("Positionnement à compléter pour une ou plusieurs collections")
                            if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid):
                                alteraction, lalteraction =_("Modification éventuelle du rang de votre collection"), "/rk/" + str(sid) + "/" + str(lid)
                    elif len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) >1:
                        if ItemRecord.objects.using(bdd).filter(sid =sid, rank =1, lid =lid):
                            progress =_("Rang 1 revendiqué pour plusieurs collections dont la vôtre")
                            action, laction =_("Repositionnement éventuel de votre collection"), "/rk/" + str(sid) + "/" + str(lid)
                        else:
                            progress =_("Rang 1 revendiqué pour plusieurs collections mais pas la vôtre")
                            if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid):
                                alteraction, lalteraction =_("Modification éventuelle du rang de votre collection"), "/rk/" + str(sid) + "/" + str(lid)
                    else:# len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) ==0:
                        progress =_("Le rang 1 n'a été revendiqué pour aucune collection")
                        if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid):
                            action, laction =_("Repositionnement éventuel de votre collection"), "/rk/" + str(sid) + "/" + str(lid)
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
                pklastone = Instruction.objects.using(bdd).filter(sid = sid).latest('pk').pk
            except:
                pklastone =0

            #Attachements :
            attchmt =ItemRecord.objects.using(bdd).filter(sid =sid).order_by('-status')
            attlist = [(Library.objects.using(bdd).get(lid =element.lid).name, element) for element in attchmt]

            rklist = ItemRecord.objects.using(bdd).filter(sid =sid).order_by('rank', 'lid')
            ranklist = [(element, Library.objects.using(bdd).get(lid =element.lid).name) for element in rklist]

    return render(request, 'epl/search.html', locals())

@login_required
def reinit(request, bdd, sid):

    k =logstatus(request)
    version =epl_version

    info =""

    ressource =ItemRecord.objects.using(bdd).get(sid =sid, rank =1)

    umail, uname = request.user.email, request.user.username

    flag =0

    for u in BddAdmin.objects.using(bdd).all():
        if (u.contact, u.name) ==(umail, uname):
            flag =1

    if flag ==1:
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

                #Message data :
                nextlid =ItemRecord.objects.using(bdd).get(sid =sid, rank =1).lid
                nextlib =Library.objects.using(bdd).get(lid =nextlid)
                subject = "eplouribousse : " + bdd + " / " + str(sid) + " / " + str(nextlid)
                host = str(request.get_host())
                message = _("Votre tour est venu d'instruire la fiche eplouribousse pour le ppn ") + str(sid) + \
                " :\n" + "https://" + host + bdd + "/add/" + str(sid) + '/' + str(nextlid) + \
                " :\n" + _("(Ce message fait suite à une correction apportée par l'administrateur de la base de données)")
                dest = [nextlib.contact]
                if nextlib.contact_bis:
                    dest.append(nextlib.contact_bis)
                if nextlib.contact_ter:
                    dest.append(nextlib.contact_ter)
                send_mail(subject, message, replymail, dest, fail_silently=True, )

                return current_status(request, bdd, sid, "999999999")
            else:
                info =_("Vous n'avez pas coché !")

    else:
        return notintime(request, bdd, sid, lid)

    return render(request, 'epl/reinit.html', locals())


@login_required
def takerank(request, bdd, sid, lid):

    k =logstatus(request)
    version =epl_version

    #Authentication control :
    if not request.user.email in [Library.objects.using(bdd).get(lid =lid).contact, Library.objects.using(bdd).get(lid =lid).contact_bis, Library.objects.using(bdd).get(lid =lid).contact_ter]:
        return home(request, bdd)

    #Control (takerank only if still possible ; status still ==0 for all attached libraries ;
    #or status ==1 but no instruction yet ; lid not "999999999")

    if len(list(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(status =0).exclude(status =1))):
        return notintime(request, bdd, sid, lid)
    elif len(list(ItemRecord.objects.using(bdd).filter(sid =sid, status =1))) and len(list(Instruction.objects.using(bdd).filter(sid = sid))):
        return notintime(request, bdd, sid, lid)
    elif lid =="999999999":
        return notintime(request, bdd, sid, lid)

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
            global lastrked
            lastrked =i
            # if len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(status =0)) ==0:
            if i.excl !='':
                i.rank =0
            f.save(using=bdd)
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
                #Message data :
                nextlib =Library.objects.using(bdd).get(lid =p.lid)
                nextlid =nextlib.lid
                subject = "eplouribousse : " + bdd + " / " + str(sid) + " / " + str(nextlid)
                host = str(request.get_host())
                message = _("Votre tour est venu d'instruire la fiche eplouribousse pour le ppn ") + str(sid) +\
                " :\n" + "https://" + host + bdd + "/add/" + str(sid) + '/' + str(nextlid)
                dest = [nextlib.contact]
                if nextlib.contact_bis:
                    dest.append(nextlib.contact_bis)
                if nextlib.contact_ter:
                    dest.append(nextlib.contact_ter)
                send_mail(subject, message, replymail, dest, fail_silently=True, )


        else:
            return notintime(request, bdd, sid, lid)

        return router(request, bdd, lid)

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

    periscope = "https://periscope.sudoc.fr/?ppnviewed=" + str(sid) + "&orderby=SORT_BY_PCP&collectionStatus=&tree="
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

    #Authentication control :
    if not request.user.email in [Library.objects.using(bdd).get(lid =lid).contact, Library.objects.using(bdd).get(lid =lid).contact_bis, Library.objects.using(bdd).get(lid =lid).contact_ter]:
        return home(request, bdd)

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
                i.line +=1
                i.time =Now()
                f.save(using=bdd)
                url ="/add/" + str(sid) + "/" + str(lid)
                return HttpResponseRedirect(url)
            else:
                info = _("Vous ne pouvez pas valider deux fois la même ligne d'instruction.")

        #Renumbering instruction lines :
        try:
            instr = Instruction.objects.using(bdd).filter(sid = sid).order_by('line', '-pk')
            j, l =0, 1
            while j <= len(instr):
                instr[j].line = l
                instr[j].save(using=bdd)
                j +=1
                l +=1
        except:
            pass
        instrlist = Instruction.objects.using(bdd).filter(sid = sid).order_by('line')

        try:
            pklastone = Instruction.objects.using(bdd).filter(sid = sid).latest('pk').pk
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

    #Authentication control :
    if not request.user.email in [Library.objects.using(bdd).get(lid =lid).contact, Library.objects.using(bdd).get(lid =lid).contact_bis, Library.objects.using(bdd).get(lid =lid).contact_ter]:
        return home(request, bdd)

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
        url ="/mod/" + str(sid) + "/" + str(lid) + "/" + str(linetomodify)
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

    #Authentication control :
    if not request.user.email in [Library.objects.using(bdd).get(lid =lid).contact, Library.objects.using(bdd).get(lid =lid).contact_bis, Library.objects.using(bdd).get(lid =lid).contact_ter]:
        return home(request, bdd)

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
                        i.line +=1
                        i.time =Now()
                        i.save(using=bdd)
                    else:
                        i.line +=2
                        i.time =Now()
                        i.save(using=bdd)

            instrlist = Instruction.objects.using(bdd).filter(sid = sid).order_by('line')

            try:
                pklastone = Instruction.objects.using(bdd).filter(sid = sid).latest('pk').pk
            except:
                pklastone =0
            if info =="":
                url ="/add/" + str(sid) + "/" + str(lid)
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

    #Authentication control :
    if not request.user.email in [Library.objects.using(bdd).get(lid =lid).contact, Library.objects.using(bdd).get(lid =lid).contact_bis, Library.objects.using(bdd).get(lid =lid).contact_ter]:
        return home(request, bdd)

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
            url ="/add/" + str(sid) + "/" + str(lid)
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

    #Authentication control :
    if not request.user.email in [Library.objects.using(bdd).get(lid =lid).contact, Library.objects.using(bdd).get(lid =lid).contact_bis, Library.objects.using(bdd).get(lid =lid).contact_ter]:
        return home(request, bdd)

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
    elif lid != "999999999" and len(Instruction.objects.using(bdd).filter(sid =sid, name ='checker')) ==1:
        if not Instruction.objects.using(bdd).filter(sid =sid, name =Library.objects.using(bdd).get(lid =lid).name, bound =" "):
            answer =_("Votre collection ne comprend pas d'éléments non reliés améliorant la résultante")

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
                instr = Instruction.objects.using(bdd).filter(sid = sid).order_by('line', '-pk')
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
                    #Message data :
                    subject = "eplouribousse : " + bdd + " / " + str(sid) + " / " + str(nextlid)
                    host = str(request.get_host())
                    message = _("Votre tour est venu d'instruire la fiche eplouribousse pour le ppn ") + str(sid) +\
                    " :\n" + "https://" + host + bdd + "/add/" + str(sid) + '/' + str(nextlid)
                    dest = [nextlib.contact]
                    if nextlib.contact_bis:
                        dest.append(nextlib.contact_bis)
                    if nextlib.contact_ter:
                        dest.append(nextlib.contact_ter)
                    send_mail(subject, message, replymail, dest, fail_silently=True, )

            if len(Instruction.objects.using(bdd).filter(sid =sid, name ='checker')) ==2:
                for e in ItemRecord.objects.using(bdd).filter(sid =sid, status =4):
                    e.status = 5
                    e.save(using=bdd)
            return router(request, bdd, lid)

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
            " :\n" + "https://" + host + bdd + "/current_status/" + str(sid) + '/' + str(lid) + \
            "\n" + _("Merci !")
            destprov = BddAdmin.objects.using(bdd).all()
            dest =[]
            for d in destprov:
                dest.append(d.contact)
            exp = request.user.email
            send_mail(subject, message, exp, dest, fail_silently=True, )
            return router(request, bdd, lid)

    else: #lid !="999999999"
        if z.is_valid() and y.flag ==True:

            if len(Instruction.objects.using(bdd).filter(sid =sid, name ='checker')) ==0:
                if not Instruction.objects.using(bdd).filter(sid =sid, name =Library.objects.using(bdd).get(lid =lid).name):
                    blankinst =Instruction(line =1, sid =sid, name =Library.objects.using(bdd).get(lid =lid)\
                    .name, bound ="x", descr =_("-- Néant --"), time =Now())
                    blankinst.save(using=bdd)
                #Renumbering instruction lines :
                try:
                    instr = Instruction.objects.using(bdd).filter(sid = sid).order_by('line', '-pk')
                    j, g =0, 1
                    while j <= len(instr):
                        instr[j].line = g
                        instr[j].save(using=bdd)
                        j +=1
                        g +=1
                except:
                    pass

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
                if not Instruction.objects.using(bdd).filter(sid =sid, name =Library.objects.using(bdd).get(lid =lid).name, bound =" "):
                    blankinst =Instruction(line =2, sid =sid, name =Library.objects.using(bdd).get(lid =lid)\
                    .name, bound =" ", descr =_("-- Néant --"), time =Now())
                    blankinst.save(using=bdd)
                #Renumbering instruction lines :
                try:
                    instr = Instruction.objects.using(bdd).filter(sid = sid).order_by('line', '-pk')
                    j, g =0, 1
                    while j <= len(instr):
                        instr[j].line = g
                        instr[j].save(using=bdd)
                        j +=1
                        g +=1
                except:
                    pass

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

            #Message data :
            subject = "eplouribousse : " + bdd + " / " + str(sid) + " / " + str(nextlid)
            host = str(request.get_host())
            message = _("Votre tour est venu d'instruire la fiche eplouribousse pour le ppn ") + str(sid) +\
            " :\n" + "https://" + host + bdd + "/add/" + str(sid) + '/' + str(nextlid)
            dest = [nextlib.contact]
            if nextlib.contact_bis:
                dest.append(nextlib.contact_bis)
            if nextlib.contact_ter:
                dest.append(nextlib.contact_ter)
            send_mail(subject, message, replymail, dest, fail_silently=True, )
            return router(request, bdd, lid)

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


def ranktotake(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="10"
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="10"
        newestfeature.save(using=bdd)

    reclist = list(ItemRecord.objects.using(bdd).filter(lid = lid, rank = 99).order_by(sort))

    resslist = []
    for e in reclist:
        itemlist = list(ItemRecord.objects.using(bdd).filter(sid = e.sid).exclude(rank =0))
        if len(itemlist) > 1:
            resslist.append(e)
    l = len(resslist)

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name

    nlib = len(Library.objects.using(bdd).exclude(lid ="999999999"))

    global lastrked
    if lastrked !=None and not lastrked.lid ==lid:
        lastrked =None

    return render(request, 'epl/to_rank_list.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'l' : l, 'k' : k, 'nlib' : nlib, \
    'lastrked' : lastrked, 'version' : version, 'sort' : sort, 'webmaster' : webmaster, 'bdd' : bdd, })


def modifranklist(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="12"
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="12"
        newestfeature.save(using=bdd)

    reclist = list(ItemRecord.objects.using(bdd).filter(lid = lid).exclude(rank = 99)\
    .exclude(status =2).exclude(status =3).exclude(status =4).\
    exclude(status =5).exclude(status =6).order_by(sort))

    resslist = []
    for e in reclist:
        if not len(list(Instruction.objects.using(bdd).filter(sid = e.sid))):
            resslist.append(e)
            # Voici ce qu'il y avait auparavant comme traitement :
        # if len(list(ItemRecord.objects.using(bdd).filter(sid = e.sid, status =1))) and not len(list(Instruction.objects.using(bdd).filter(sid = e.sid))):
        #     resslist.append(e)
        # elif len(list(ItemRecord.objects.using(bdd).filter(sid = e.sid).exclude(status =0))) ==0:
        #     resslist.append(e)
    l = len(resslist)

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name

    nlib = len(Library.objects.using(bdd).exclude(lid ="999999999"))

    global lastrked
    if lastrked !=None and not lastrked.lid ==lid:
        lastrked =None

    return render(request, 'epl/modifrklist.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'l' : l, 'k' : k, 'nlib' : nlib, \
    'lastrked' : lastrked, 'version' : version, 'sort' : sort, 'webmaster' : webmaster, 'bdd' : bdd, })


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


def xranktotake(request, bdd, lid, xlid, sort):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="11$" + str(xlid)
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="11$" + str(xlid)
        newestfeature.save(using=bdd)

    #Getting ressources whose this lid must but has not yet taken rank :
    reclist = list(ItemRecord.objects.using(bdd).filter(lid = lid, rank = 99).order_by(sort))

    resslist = []
    for e in reclist:
        itemlist = list(ItemRecord.objects.using(bdd).filter(sid = e.sid).exclude(rank =0))
        if len(itemlist) > 1 and list(ItemRecord.objects.using(bdd).filter(sid = e.sid, lid = xlid).exclude(rank =0)):
            resslist.append(e)
    l = len(resslist)

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name
    xlibname = Library.objects.using(bdd).get(lid =xlid).name

    global lastrked
    if lastrked !=None and not lastrked.lid ==lid:
        lastrked =None

    return render(request, 'epl/xto_rank_list.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'l' : l, 'k' : k, 'xlibname' : xlibname, \
    'lastrked' : lastrked, 'version' : version, 'sort' : sort, 'xlid' : xlid, 'webmaster' : webmaster, 'bdd' : bdd, })


def excllist(request, bdd):

    k =logstatus(request)
    version =epl_version

    EXCLUSION_CHOICES = ('', ''),
    for e in Exclusion.objects.using(bdd).all().order_by('label'):
        EXCLUSION_CHOICES += (e.label, e.label),
    EXCLUSION_CHOICES += ("Autre (Commenter)", _("Autre (Commenter)")),

    l =0

    libch = ('',''),
    for l in Library.objects.using(bdd).all().exclude(name ='checker').order_by('name'):
        libch += (l.name, l.name),

    sortch = ('title',_('titre')), ('excl',_("motif d'exclusion")), ('cn',_('cote et titre')), ('sid',_('ppn')),

    stillmodch = ('',''), ('oui',_('oui')), ('non',_('non')),

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

        if exclreason and stillmod:
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
        elif exclreason and not stillmod:
            excl_list =ItemRecord.objects.using(bdd).filter(lid =lid, rank =0, excl =exclreason).order_by(sort)
        elif stillmod and not exclreason:
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
        elif not stillmod and not exclreason:
            excl_list =ItemRecord.objects.using(bdd).filter(lid =lid, rank =0).order_by(sort)

        length =len(excl_list)

    return render(request, 'epl/excl.html', locals())


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

    return render(request, 'epl/faulty.html', locals())


def arbitration(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="20"
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="20"
        newestfeature.save(using=bdd)

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

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name

    nlib = len(Library.objects.using(bdd).exclude(lid ="999999999"))

    global lastrked
    if lastrked !=None and not lastrked.lid ==lid:
        lastrked =None

    return render(request, 'epl/arbitration.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'size' : size, 'k' : k, \
    'lastrked' : lastrked, 'version' : version, 'nlib' : nlib, 'sort' : sort, 'webmaster' : webmaster, 'bdd' : bdd, })


def arbrk1(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="24"
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="24"
        newestfeature.save(using=bdd)

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

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name

    global lastrked
    if lastrked !=None and not lastrked.lid ==lid:
        lastrked =None

    return render(request, 'epl/arbrk1.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'size' : size, 'k' : k, \
    'lastrked' : lastrked, 'version' : version, 'sort' : sort, 'webmaster' : webmaster, 'bdd' : bdd, })


def arbnork1(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="25"
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="25"
        newestfeature.save(using=bdd)

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

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name

    global lastrked
    if lastrked !=None and not lastrked.lid ==lid:
        lastrked =None

    return render(request, 'epl/arbnork1.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'size' : size, 'k' : k, \
    'lastrked' : lastrked, 'version' : version, 'sort' : sort, 'webmaster' : webmaster, 'bdd' : bdd, })


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


def xarbitration(request, bdd, lid, xlid, sort):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="21$" + str(xlid)
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="21$" + str(xlid)
        newestfeature.save(using=bdd)

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
        if len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) ==0 and \
        len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =99)) ==0 and \
        len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) >1:
            if ItemRecord.objects.using(bdd).filter(sid =sid, lid = xlid, status =0).exclude(rank =1).exclude(rank =0).exclude(rank =99):
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
    libname = Library.objects.using(bdd).get(lid =lid).name
    xlibname = Library.objects.using(bdd).get(lid =xlid).name

    global lastrked
    if lastrked !=None and not lastrked.lid ==lid:
        lastrked =None

    return render(request, 'epl/xarbitration.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'size' : size, 'k' : k, 'xlibname' : xlibname, \
    'xlid' : xlid, 'lastrked' : lastrked, 'version' : version, 'sort' : sort, 'webmaster' : webmaster, 'bdd' : bdd, })


def x1arb(request, bdd, lid, xlid, sort):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="22$" + str(xlid)
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="22$" + str(xlid)
        newestfeature.save(using=bdd)

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

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name
    xlibname = Library.objects.using(bdd).get(lid =xlid).name

    global lastrked
    if lastrked !=None and not lastrked.lid ==lid:
        lastrked =None

    return render(request, 'epl/x1arbitration.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'size' : size, 'k' : k, 'xlibname' : xlibname, \
    'lastrked' : lastrked, 'version' : version, 'sort' : sort, 'xlid' : xlid, 'webmaster' : webmaster, 'bdd' : bdd, })


def x0arb(request, bdd, lid, xlid, sort):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="23$" + str(xlid)
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="23$" + str(xlid)
        newestfeature.save(using=bdd)

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

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name
    xlibname = Library.objects.using(bdd).get(lid =xlid).name

    global lastrked
    if lastrked !=None and not lastrked.lid ==lid:
        lastrked =None

    return render(request, 'epl/x0arbitration.html', { 'resslist' : resslist, \
    'lid' : lid, 'libname' : libname, 'size' : size, 'k' : k, 'xlibname' : xlibname, \
    'lastrked' : lastrked, 'version' : version, 'sort' : sort, 'xlid' : xlid, 'webmaster' : webmaster, 'bdd' : bdd, })


def instrtodo(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="30"
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="30"
        newestfeature.save(using=bdd)

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

    #Getting library name :
    libname = Library.objects.using(bdd).get(lid =lid).name

    nlib = len(Library.objects.using(bdd).exclude(lid ="999999999"))

    lidchecker = "999999999"

    return render(request, 'epl/instrtodo.html', locals())


def instroneb(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="35"
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="35"
        newestfeature.save(using=bdd)

    if lid !="999999999":
        l = list(ItemRecord.objects.using(bdd).filter(lid =lid, rank =1).exclude(status =0).exclude(status =2).exclude(status =3)\
        .exclude(status =4).exclude(status =5).exclude(status =6).order_by(sort))
        # Ressources whose the lid identified library has rank =1 and has to deal with bound elements (status =1)

    elif lid =="999999999":
        do = home(request, bdd)
        return do

    size = len(l)

    #Getting library name :
    libname = Library.objects.using(bdd).get(lid =lid).name

    return render(request, 'epl/instrtodobd1.html', locals())


def instrotherb(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="36"
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="36"
        newestfeature.save(using=bdd)

    if lid !="999999999":
        l = list(ItemRecord.objects.using(bdd).filter(lid =lid).exclude(rank =1).\
        exclude(status =0).exclude(status =2).exclude(status =3).exclude(status =4)\
        .exclude(status =5).exclude(status =6).order_by(sort))
        # Ressources whose the lid identified library has rank !=1 and has to deal with bound elements (status =1)

    elif lid =="999999999":
        do = home(request, bdd)
        return do

    size = len(l)

    #Getting library name :
    libname = Library.objects.using(bdd).get(lid =lid).name

    return render(request, 'epl/instrtodobdnot1.html', locals())


def instronenotb(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="37"
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="37"
        newestfeature.save(using=bdd)

    if lid !="999999999":
        l = list(ItemRecord.objects.using(bdd).filter(lid =lid, rank =1).exclude(status =0).\
        exclude(status =1).exclude(status =2).exclude(status =4).exclude(status =5).exclude(status =6).order_by(sort))
        # Ressources whose the lid identified library has rank =1 and has to deal with not bound elements (status =3)

    elif lid =="999999999":
        do = home(request, bdd)
        return do

    size = len(l)

    #Getting library name :
    libname = Library.objects.using(bdd).get(lid =lid).name

    return render(request, 'epl/instrtodonotbd1.html', locals())


def instrothernotb(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="38"
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="38"
        newestfeature.save(using=bdd)

    if lid !="999999999":
        l = list(ItemRecord.objects.using(bdd).filter(lid =lid).exclude(rank =1).exclude(status =0).\
        exclude(status =1).exclude(status =2).exclude(status =4).exclude(status =5).exclude(status =6).order_by(sort))
        # Ressources whose the lid identified library has rank !=1 and has to deal with not bound elements (status =3)

    elif lid =="999999999":
        do = home(request, bdd)
        return do

    size = len(l)

    #Getting library name :
    libname = Library.objects.using(bdd).get(lid =lid).name

    return render(request, 'epl/instrtodonotbdnot1.html', locals())


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


def xinstrlist(request, bdd, lid, xlid, sort):

    k =logstatus(request)
    version =epl_version

    if lid =="999999999":
        return notintime(request, bdd, "-?-", lid)

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="31$" + str(xlid)
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="31$" + str(xlid)
        newestfeature.save(using=bdd)

    name = Library.objects.using(bdd).get(lid =lid).name
    xname = Library.objects.using(bdd).get(lid =xlid).name

    lprov = list(ItemRecord.objects.using(bdd).filter(lid =lid).exclude(status =0).exclude(status =2).\
    exclude(status =4).exclude(status =5).exclude(status =6).order_by(sort))

    l =[]
    for e in lprov:
        if ItemRecord.objects.using(bdd).filter(lid =xlid, sid =e.sid).exclude(rank =0):
            l.append(e)

    size = len(l)

    return render(request, 'epl/xto_instr_list.html', locals())


def tobeedited(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="40"
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="40"
        newestfeature.save(using=bdd)

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

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name

    return render(request, 'epl/to_edit_list.html', locals())


def mothered(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="41"
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="41"
        newestfeature.save(using=bdd)

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

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name

    return render(request, 'epl/to_edit_list_mother.html', locals())


def notmothered(request, bdd, lid, sort):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="42"
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="42"
        newestfeature.save(using=bdd)

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

    #Library name :
    libname = Library.objects.using(bdd).get(lid =lid).name

    return render(request, 'epl/to_edit_list_notmother.html', locals())


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


def xmothered(request, bdd, lid, xlid, sort):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="43$" + str(xlid)
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="43$" + str(xlid)
        newestfeature.save(using=bdd)

    l = list(ItemRecord.objects.using(bdd).filter(lid =lid, rank =1).order_by(sort))

    #Initializing a list of ressources to edit :
    resslist = []

    for e in l:
        nl = Instruction.objects.using(bdd).filter(sid =e.sid)
        kd = nl.filter(name = "checker")
        if len(kd) ==2 and Instruction.objects.using(bdd).filter(sid =e.sid, name =Library.objects.using(bdd).get(lid =xlid)):
            resslist.append(e)

    size = len(resslist)

    name = Library.objects.using(bdd).get(lid =lid).name
    xname = Library.objects.using(bdd).get(lid =xlid).name

    return render(request, 'epl/xto_edit_list_mother.html', locals())


def xnotmothered(request, bdd, lid, xlid, sort):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="44$" + str(xlid)
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(lid =lid).name).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="44$" + str(xlid)
        newestfeature.save(using=bdd)

    l = list(ItemRecord.objects.using(bdd).filter(lid =lid).exclude(rank =1).exclude(rank =0).exclude(rank =99).order_by(sort))

    #Initializing a list of ressources to edit :
    resslist = []

    for e in l:
        nl = Instruction.objects.using(bdd).filter(sid =e.sid)
        kd = nl.filter(name = "checker")
        if len(kd) ==2 and Instruction.objects.using(bdd).filter(sid =e.sid, name =Library.objects.using(bdd).get(lid =xlid)):
            resslist.append(e)

    size = len(resslist)

    name = Library.objects.using(bdd).get(lid =lid).name
    xname = Library.objects.using(bdd).get(lid =xlid).name

    return render(request, 'epl/xto_edit_list_notmother.html', locals())


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
        coitemlist =ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0).order_by("rank")
        for co in coitemlist:
            coliblist.append(Library.objects.using(bdd).get(lid = co.lid))

        # Not Contributing collections (lib) ordered by 'rank'
        exlist = []
        for elmt in ItemRecord.objects.using(bdd).filter(sid =sid, rank =0):
            exlist.append(((Library.objects.using(bdd).get(lid = elmt.lid)).name, elmt.excl, elmt.comm))

        return render(request, 'epl/edition.html', locals())

    else:
        return notintime(request, bdd, sid, lid)


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
            action, laction =_("Edition de la fiche de résultante"), "/ed/" + str(sid) + "/" + str(lid)
    elif higher_status ==4:
        if len(ItemRecord.objects.using(bdd).filter(sid =sid, status =4)) ==len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)):
            progress =_("En attente de validation finale par le contrôleur")
            if lid =="999999999":
                action, laction =_("Validation finale"), "/end/" + str(sid) + "/" + str(lid)
        else:
            if lid !="999999999":
                if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid, status =3):
                    if Instruction.objects.using(bdd).filter(sid =sid, bound =" ", name =Library.objects.using(bdd).get(lid =lid).name):
                        progress =_("Instruction des non reliés en cours pour votre collection")
                    else:
                        progress =_("Instruction des non reliés à débuter pour votre collection")
                    action, laction =_("Instruction"), "/add/" + str(sid) + "/" + str(lid)
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
                action, laction =_("Instruction"), "/add/" + str(sid) + "/" + str(lid)
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
                action, laction =_("Validation intermédiaire"), "/end/" + str(sid) + "/" + str(lid)
        else:
            if lid !="999999999":
                if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid, status =1):
                    if Instruction.objects.using(bdd).filter(sid =sid, bound ="x", name =Library.objects.using(bdd).get(lid =lid).name):
                        progress =_("Instruction des reliés en cours pour votre collection")
                    else:
                        progress =_("Instruction des reliés à débuter pour votre collection")
                    action, laction =_("Instruction"), "/add/" + str(sid) + "/" + str(lid)
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
                action, laction =_("Instruction"), "/add/" + str(sid) + "/" + str(lid)
            else:
                xname =Library.objects.using(bdd).get(lid =ItemRecord.objects.using(bdd).get(sid =sid, status =1).lid).name
                if Instruction.objects.using(bdd).filter(sid =sid, bound ="x", name =xname):
                    progress =_("Instruction des reliés en cours pour : ")
                else:
                    progress =_("Instruction des reliés en cours ; à débuter pour : ")
            if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid) and len(Instruction.objects.using(bdd).filter(sid =sid)) ==0:
                alteraction, lalteraction =_("Modification éventuelle du rang de votre collection"), "/rk/" + str(sid) + "/" + str(lid)
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
                     action, laction =_("Repositionnement éventuel de votre collection"), "/rk/" + str(sid) + "/" + str(lid)
            elif ItemRecord.objects.using(bdd).filter(sid =sid, rank =99) and len(ItemRecord.objects.using(bdd).filter(sid =sid).exclude(rank =0)) >1:
                if ItemRecord.objects.using(bdd).filter(sid =sid, rank =99, lid =lid):
                    progress =_("Positionnement à compléter pour votre collection")
                    action, laction =_("Positionnement de votre collection"), "/rk/" + str(sid) + "/" + str(lid)
                else:
                    progress =_("Positionnement à compléter pour une ou plusieurs collections")
                    if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid):
                        alteraction, lalteraction =_("Modification éventuelle du rang de votre collection"), "/rk/" + str(sid) + "/" + str(lid)
            elif len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) >1:
                if ItemRecord.objects.using(bdd).filter(sid =sid, rank =1, lid =lid):
                    progress =_("Rang 1 revendiqué pour plusieurs collections dont la vôtre")
                    action, laction =_("Repositionnement éventuel de votre collection"), "/rk/" + str(sid) + "/" + str(lid)
                else:
                    progress =_("Rang 1 revendiqué pour plusieurs collections mais pas la vôtre")
                    if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid):
                        alteraction, lalteraction =_("Modification éventuelle du rang de votre collection"), "/rk/" + str(sid) + "/" + str(lid)
            else:# len(ItemRecord.objects.using(bdd).filter(sid =sid, rank =1)) ==0:
                progress =_("Le rang 1 n'a été revendiqué pour aucune collection")
                if ItemRecord.objects.using(bdd).filter(sid =sid, lid =lid):
                    action, laction =_("Repositionnement éventuel de votre collection"), "/rk/" + str(sid) + "/" + str(lid)
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
        pklastone = Instruction.objects.using(bdd).filter(sid = sid).latest('pk').pk
    except:
        pklastone =0

    #Attachements :
    attchmt =ItemRecord.objects.using(bdd).filter(sid =sid).order_by('-status')
    attlist = [(Library.objects.using(bdd).get(lid =element.lid).name, element) for element in attchmt]

    rklist = ItemRecord.objects.using(bdd).filter(sid =sid).order_by('rank', 'lid')
    ranklist = [(element, Library.objects.using(bdd).get(lid =element.lid).name) for element in rklist]

    return render(request, 'epl/current.html', locals())


def checkinstr(request, bdd):

    k =logstatus(request)
    version =epl_version

    project = Project.objects.using(bdd).all().order_by('pk')[0].name

    return render(request, 'epl/checker.html', locals())


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


def xckbd(request, bdd, coll_set):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(name ="checker")).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="32$" + str(coll_set)
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(name ="checker")).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="32$" + str(coll_set)
        newestfeature.save(using=bdd)

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


def xcknbd(request, bdd, coll_set):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(name ="checker")).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="33$" + str(coll_set)
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(name ="checker")).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="33$" + str(coll_set)
        newestfeature.save(using=bdd)

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


def xckall(request, bdd, coll_set):

    k =logstatus(request)
    version =epl_version

    newestfeature =Feature()
    if not Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(name ="checker")).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition"):
        newestfeature.libname =Library.objects.using(bdd).get(lid =lid).name
        newestfeature.feaname ="34$" + str(coll_set)
        newestfeature.save(using=bdd)
    else:
        newestfeature =Feature.objects.using(bdd).filter(libname =Library.objects.using(bdd).get(name ="checker")).exclude(feaname = "ranking").exclude(feaname ="arbitration").exclude(feaname ="instrtodo").exclude(feaname ="edition")[0]
        newestfeature.feaname ="34$" + str(coll_set)
        newestfeature.save(using=bdd)

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
