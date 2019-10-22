from django import forms

from .models import ItemRecord, Instruction, Library, EXCLUSION_CHOICES, Feature, LIBRARY_CHOICES, FEATURE_CHOICES, CHECKING_CHOICES, Check, Flag


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
