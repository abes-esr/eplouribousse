from .models import Exclusion
from django.utils.translation import ugettext_lazy as _

EXCLUSION_CHOICES = ("Autre (Commenter)", _("Autre (Commenter)")),
for e in Exclusion.objects.all().order_by('label'):
    EXCLUSION_CHOICES += (e.label, e.label),
