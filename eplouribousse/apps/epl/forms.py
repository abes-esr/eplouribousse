from django import forms

from .models import ItemRecord, Instruction, Library, EXCLUSION_CHOICES, Feature, LIBRARY_CHOICES, FEATURE_CHOICES, CHECKING_CHOICES, Check, Flag, PHASE_CHOICES

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


class InstructionCheckerFilter(forms.Form):
    name = forms.MultipleChoiceField(required = True, widget=forms.CheckboxSelectMultiple, choices=LIBRARY_CHOICES[1:], label =_("Bibliothèques impliquées (opérateur 'ou')"))
    phase = forms.MultipleChoiceField(required = True, widget=forms.CheckboxSelectMultiple, choices=PHASE_CHOICES, label =_("Phase d'instruction"))
