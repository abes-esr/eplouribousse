from django.urls import path

from . import views

urlpatterns = [
    path('ranking/<str:sid>/<str:lid>', views.takerank, name='ranking'),
    path('addinstruction/<str:sid>/<str:lid>', views.addinstr, name='add instruction'),
    path('delinstruction/<str:sid>/<str:lid>', views.delinstr, name='delete instruction'),
    path('endinstruction/<str:sid>/<str:lid>', views.endinstr, name='end of instruction'),
    path('to_rank_list/<str:lid>', views.ranktotake, name='to be ranked list'),
    path('instrtodo/<str:lid>', views.instrtodo, name='instruction to do list, all'),
    path('instrtodobd1/<str:lid>', views.instroneb, name='instruction to do list, bound, rank 1'),
    path('instrtodobdnot1/<str:lid>', views.instrotherb, name='instruction to do list, bound, other ranks'),
    path('instrtodonotbd1/<str:lid>', views.instronenotb, name='instruction to do list, not bound, rank 1'),
    path('instrtodonotbdnot1/<str:lid>', views.instrothernotb, name='instruction to do list, not bound, other ranks'),
    path('arbitration/<str:lid>', views.arbitration, name='arbitration'),
    path('to_edit_list/<str:lid>', views.tobeedited, name='to be edited list'),
    path('edition/<str:sid>/<str:lid>', views.edition, name='edition'),
    path('pdfgen/<str:sid>/<str:lid>', views.pdfedition, name='pdfedition'),
    path('home', views.home, name='home'),
    path('indicators', views.indicators, name='indicators'),
]
