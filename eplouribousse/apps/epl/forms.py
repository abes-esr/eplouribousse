from django import forms

from .models import ItemRecord, Instruction, Library, EXCLUSION_CHOICES, Feature, LIBRARY_CHOICES, FEATURE_CHOICES, CHECKING_CHOICES, Check, Flag, PHASE_CHOICES

from django.utils.translation import ugettext_lazy as _

class PositionForm(forms.ModelForm):
    class Meta:
        model = ItemRecord
        fields = ('rank', 'excl', 'comm',)
        widgets = {
            'excl' : forms.Select(choices=EXCLUSION_CHOICES),
            'comm' : forms.Textarea(attrs={'placeholder': _("Commentaire éventuel pour expliquer votre choix (max. 250 caractères)")}),
        }


class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        exclude = ('sid', 'name', 'bound',)
        widgets = {
            'line' : forms.TextInput(attrs={'title': _("Respectez l'ordre chronologique du champ 'Segment'")}),
            'oname' : forms.TextInput(attrs={'title': _("Intitulé de la bibliothèque ayant précédemment déclaré une 'exception' ou un 'améliorable'")}),
            'descr' : forms.TextInput(attrs={'placeholder': _("1990(2)-1998(12) par ex.")}),
            'exc' : forms.TextInput(attrs={'placeholder': _("1991(5) par ex.")}),
            'degr' : forms.TextInput(attrs={'placeholder': _("1995(4) par ex.")}),
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
