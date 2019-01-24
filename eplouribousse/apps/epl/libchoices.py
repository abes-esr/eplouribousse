from .models import Library

LIBRARY_CHOICES = ('admin','admin'),
if Library.objects.all().exclude(name ='admin'):
    for l in Library.objects.all().exclude(name ='admin').order_by('name'):
        LIBRARY_CHOICES += (l.name, l.name),
