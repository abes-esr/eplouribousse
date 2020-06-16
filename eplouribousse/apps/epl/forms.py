from django import forms

from .models import ItemRecord, Instruction, Library, EXCLUSION_CHOICES, Feature, LIBRARY_CHOICES, FEATURE_CHOICES, CHECKING_CHOICES, Check, Flag, PHASE_CHOICES

from django.utils.translation import ugettext_lazy as _

class PositionForm(forms.ModelForm):
    class Meta:
        model = ItemRecord
        fields = ('rank', 'excl', 'comm',)
        widgets = {
            'rank' : forms.Select(attrs={'title': _("Choisissez 1 pour la collection mère ; 2, 3 ou 4 selon l'importance de votre collection ou d'autres raisons ...")}),
            'excl' : forms.Select(choices=EXCLUSION_CHOICES),
            'comm' : forms.Textarea(attrs={'placeholder': _("Commentaire éventuel pour expliquer votre choix (max. 250 caractères)")}),
        }


class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        exclude = ('sid', 'name', 'bound',)
        widgets = {
            'oname' : forms.TextInput(attrs={'title': _("Intitulé de la bibliothèque ayant précédemment déclaré une 'exception' ou un 'améliorable'")}),
            'descr' : forms.TextInput(attrs={'placeholder': _("1990(2)-1998(12) par ex."), 'title': _("Suite ininterrompue chronologiquement ; le n° de ligne est à déterminer selon l'ordre chronologique de ce champ")}),
            'exc' : forms.TextInput(attrs={'placeholder': _("1991(5) par ex."), 'title': \
            _("éléments manquants dans le segment pour la forme considérée (pas forcément des lacunes si l'on considère la forme reliée)")}),
            'degr' : forms.TextInput(attrs={'placeholder': _("1995(4) par ex."), 'title': \
            _("éléments dégradés (un volume relié dégradé peut être remplacé par les fascicules correspondants en bon état)")}),
        }


class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ('libname', 'feaname',)
        widgets = {
            'libname' : forms.Select(choices=LIBRARY_CHOICES),
            'feaname' : forms.RadioSelect(choices=FEATURE_CHOICES),
        }


class CheckForm(forms.ModelForm):
    class Meta:
        model = Flag
        fields = ('flag',)


class AdminCheckForm(forms.ModelForm):
    class Meta:
        model = Check
        fields = ('checkin',)
        widgets = {
            'checkin' : forms.RadioSelect(choices=CHECKING_CHOICES,),
        }


class InstructionCheckerFilter(forms.Form):
    name = forms.MultipleChoiceField(required = True, widget=forms.CheckboxSelectMultiple, choices=LIBRARY_CHOICES[1:], label =_("Bibliothèques impliquées (opérateur 'ou')"))
    phase = forms.MultipleChoiceField(required = True, widget=forms.CheckboxSelectMultiple, choices=PHASE_CHOICES, label =_("Phase d'instruction"))
