from .models import Exclusion
from django.utils.translation import ugettext_lazy as _

EXCLUSION_CHOICES = ('',''),
for e in Exclusion.objects.all().exclude(label ="Autre (Commenter)").order_by('label'):
        EXCLUSION_CHOICES += (e.label, e.label),
EXCLUSION_CHOICES += ("Autre (Commenter)", _("Autre (Commenter)")),
