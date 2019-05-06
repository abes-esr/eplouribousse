from django.db import models


class Library(models.Model):
    """Model for the libraries."""
    lid = models.CharField('library ID', max_length=16, unique=True)
    name = models.CharField('library name', max_length=30, unique=True)
    contact = models.EmailField('email')
    def __str__(self):
        return self.name

from .libchoices import LIBRARY_CHOICES

#Reasons to exclude an item record (see under ; class : ItemRecord,
#field : excl) :
EXCLUSION_CHOICES = (
    ('Abonnement en cours', 'Abonnement en cours'),
    ('Dépôt légal', 'Dépôt légal'),
    ('Entièrement patrimonial', 'Entièrement patrimonial'),
    ("Fait partie d'un plan de conservation partagée", "Fait partie d'un plan de conservation partagée"),
    ("Autre (Commenter)", "Autre (Commenter)"),
)

#Ranking choices :
RANKING_CHOICES = ((4, 4), (3, 3), (2, 2), (1, 1),)

class ItemRecord(models.Model):
    """Model for the item records."""
    sid = models.CharField('serial ID', max_length=16, blank =False)
    issn = models.CharField('issn', max_length=9, blank=True)
    title = models.TextField('title', max_length=100)
    pubhist = models.CharField('publication history', max_length=25, \
            blank=True)
    lid = models.CharField('library ID', max_length=16, blank =False)
    holdstat = models.TextField('holdings statement', blank=True)
    missing = models.TextField('gap', blank=True)
    cn = models.CharField('call number', max_length=50, blank=True)
    rank = models.PositiveSmallIntegerField('ranking', default=99, choices=RANKING_CHOICES, null =False)
    #Ranking is used to order the libraries for treatment based on holdings
    #statement or other criteria ; 1 shall be used by the library claiming
    #to be the repository for the publication. 0 is used in case of exclusion :
    excl = models.CharField("exclusion ?", max_length=100, \
    choices=EXCLUSION_CHOICES, blank=True)
    #To let a library declaring that its item must not be taken into account
    #for one of the EXCLUSION_CHOICES reasons.
    comm = models.CharField('comment', max_length=250, blank=True)
    #For any comment (optional)
    status = models.PositiveSmallIntegerField('status', default=0, null =False)
    # Number of admin control(s) i.e. instruction(s) --> used for selections (lists)
    # It informs on treatment stage :
    # 0 : initial state, item can still be ranked (default value)
    # 1 : all libraries have taken rank and the publication must be instructed (bound elements) in the lid identified library
    # 2 : bound elements completed in the lid identified library
    # 3 : not-bound elements must be instructed (bound elements) in the lid identified library
    # 4 : publication has just been completely instructed by the lid identified library
    # 5 : visa is ok for the whole treatment by admin
    # 6 : error in instructing the resulting collection (doesn't affect ItemRecord with rank =0) to inform the bbd admin and to retire provisionally the ressource
    def __str__(self):
        r = str(self.rank)
        s = str(self.status)
        info = str(self.sid + ' | ' + self.issn + ' | ' + self.lid + ' | ' \
        + self.cn + ' | ' + self.excl + ' | ' + r + ' | ' + s)
        return info


class Instruction(models.Model):
    """Model for instruction lines."""
    sid = models.CharField('serial ID', max_length=16, blank=False)
    line = models.PositiveSmallIntegerField('line number', default=0, null =False)
    name = models.CharField('library name', max_length=30, blank =False)
    bound = models.CharField('bound', max_length=1, blank=True)
    oname = models.CharField('name of the other library on the instruction \
    of which an enhance is made or an exception is replaced', max_length=30, \
    blank=True)
    descr = models.CharField('segment description', max_length=250, blank=True)
    exc = models.CharField('exception', max_length=250, blank=True)
    degr = models.CharField('enhanceable elements'\
    , max_length=250, blank=True)
    time = models.CharField('time', max_length=250, blank=True)
    def __str__(self):

        if self.bound ==" ":
            b = "not bound"
        else:
            b = "bound"

        info = str(self.time) + ' | ' + str(self.pk) + ' | ' + str(self.sid) + ' | ' + str(self.line) \
        + ' | ' + str(self.name + ' | ' + self.oname + ' | ' + self.descr) \
        + ' | ' + b
        return info


#Feature choices :
FEATURE_CHOICES = (
    ('ranking', "1. Positionnement"),
    ('arbitration', "2. Arbitrages"),
    ('instrtodo', "3. Instruction"),
    ('edition', "4. Résultantes"),
)


class Feature(models.Model):
    """Model for features."""
    libname = models.CharField('library', max_length=30, blank=False, choices=LIBRARY_CHOICES)
    feaname = models.CharField('feature', max_length=120, default="ranking", blank=False, choices=FEATURE_CHOICES)
    def __str__(self):
        info = self.libname + ' | ' + self.feaname
        return info

class BddAdmin(models.Model):
    """Model for BDD administrator(s)"""
    name = models.CharField('library name', max_length=30, unique=True)
    contact = models.EmailField('email')
    def __str__(self):
        return self.name

#Checking choices :
CHECKING_CHOICES = (('Visa', "Visa OK (La fiche est conforme)"), ('Notify', "Anomalie (L'administrateur de la base sera informé)"),)

class Check(models.Model):
    """Model for admin checking"""
    checkin = models.CharField('Visa de conformité', max_length=120, default ="Visa", blank=False, choices =CHECKING_CHOICES)
    def __str__(self):
        return self.checkin

class Flag(models.Model):
    """Model for checking"""
    flag = models.BooleanField('checking', default=False)
    def __str__(self):
        return str(self.flag)
