from django.urls import path

from . import views

urlpatterns = [
    path('rk/<str:sid>/<str:lid>', views.takerank, name='ranking'),
    path('timeout/<str:sid>/<str:lid>', views.notintime, name='not in time'),
    path('add/<str:sid>/<str:lid>', views.addinstr, name='add instruction'),
    path('del/<str:sid>/<str:lid>', views.delinstr, name='delete instruction'),
    path('end/<str:sid>/<str:lid>', views.endinstr, name='end of instruction'),
    path('rklist/<str:lid>', views.ranktotake, name='to be ranked list'),
    path('allinstr/<str:lid>', views.instrtodo, name='instruction to do list, all'),
    path('bd1/<str:lid>', views.instroneb, name='instruction to do list, bound, rank 1'),
    path('bdnot1/<str:lid>', views.instrotherb, name='instruction to do list, bound, other ranks'),
    path('notbd1/<str:lid>', views.instronenotb, name='instruction to do list, not bound, rank 1'),
    path('notbdnot1/<str:lid>', views.instrothernotb, name='instruction to do list, not bound, other ranks'),
    path('arb/<str:lid>', views.arbitration, name='arbitration'),
    path('edlist/<str:lid>', views.tobeedited, name='to be edited list'),
    path('ed/<str:sid>/<str:lid>', views.edition, name='edition'),
    path('pdf/<str:sid>/<str:lid>', views.pdfedition, name='pdfedition'),
    path('', views.home, name='home'),
    path('dashboard', views.indicators, name='indicators'),
]
