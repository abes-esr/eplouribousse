from django import forms

from .models import ItemRecord, Instruction, Library, EXCLUSION_CHOICES, Feature, LIBRARY_CHOICES, FEATURE_CHOICES, CHECKING_CHOICES, Check, Flag

from django.utils.translation import ugettext_lazy as _

class PositionForm(forms.ModelForm):
    class Meta:
        model = ItemRecord
        fields = ('rank', 'excl', 'comm',)
        widgets = {
            'excl': forms.Select(choices=EXCLUSION_CHOICES),
            'comm' : forms.Textarea,
        }


class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        exclude = ('sid', 'name', 'bound',)


class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ('libname', 'feaname',)
        widgets = {
            'libname': forms.Select(choices=LIBRARY_CHOICES),
            'feaname': forms.RadioSelect(choices=FEATURE_CHOICES),
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
            'checkin': forms.RadioSelect(choices=CHECKING_CHOICES,),
        }


class EditionForm(forms.Form):
    RK_CHOICES = (("a", _("Premier Rang")), ("b", _("Autre rang")),)
    LIB_CHOICES = LIBRARY_CHOICES[1:]
    rank = forms.ChoiceField(required = True, widget=forms.Select, choices=RK_CHOICES, label =_("Rang des collections de la bibliothèque mentionnée dans l'entête de cette page"))
    lib = forms.ChoiceField(required = True, widget=forms.Select, choices=LIB_CHOICES, label =_("Autre bibliothèque impliquée"))

class XlibForm(forms.Form):
    name = forms.ChoiceField(required = True, widget=forms.Select, choices=LIBRARY_CHOICES[1:], label =_("Autre bibliothèque impliquée"))
