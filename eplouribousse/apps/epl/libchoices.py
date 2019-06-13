from .models import Library

LIBRARY_CHOICES = ('checker','checker'),
if Library.objects.all().exclude(name ='checker'):
    for l in Library.objects.all().exclude(name ='checker').order_by('name'):
        LIBRARY_CHOICES += (l.name, l.name),
