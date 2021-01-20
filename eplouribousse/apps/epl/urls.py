from django.urls import path

from . import views, views_pdf, views_csv

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('webmaster', views.webmstr, name='webmaster'),
    path('confirmation', views.confirm, name='confirmation'),
    path('router/<str:lid>', views.router, name='route to the right list'),
    path('lang', views.lang, name='language'),
    path('disconnect', views.logout_view, name='disconnection'),
    path('timeout/<str:sid>/<str:lid>', views.notintime, name='not in time'),
    path('dashboard', views.indicators, name='indicators'),
    path('search', views.search, name='searching a serial'),

    path('rk/<str:sid>/<str:lid>', views.takerank, name='ranking'),

    path('add/<str:sid>/<str:lid>', views.addinstr, name='add instruction'),
    path('sel/<str:sid>/<str:lid>', views.selinstr, name='select instruction to modify'),
    path('mod/<str:sid>/<str:lid>/<int:linetomodify>', views.modinstr, name='modify instruction'),
    path('del/<str:sid>/<str:lid>', views.delinstr, name='delete instruction'),
    path('end/<str:sid>/<str:lid>', views.endinstr, name='end of instruction'),

    path('rklist/<str:lid>/<str:sort>', views.ranktotake, name='to be ranked list'),
    path('modifrklist/<str:lid>/<str:sort>', views.modifranklist, name='modify a rank list'),
    path('rkfilter/<str:lid>', views.filter_rklist, name='rkfilter'),
    path('rklist/<str:lid>/<str:xlid>/<str:sort>', views.xranktotake, name='xto be ranked list'),
    path('excl', views.excllist, name='exclusions'),
    path('faulty', views.faulty, name='faulty'),

    path('arb/<str:lid>/<str:sort>', views.arbitration, name='arbitration'),
    path('arbrk1_list/<str:lid>/<str:sort>', views.arbrk1, name='arbitration rank 1'),
    path('arbnork1_list/<str:lid>/<str:sort>', views.arbnork1, name='arbitration no rank 1'),
    path('arbfilter/<str:lid>', views.filter_arblist, name='arbfilter'),
    path('arblist/<str:lid>/<str:xlid>/<str:sort>', views.xarbitration, name='xarbitration'),
    path('arb1list/<str:lid>/<str:xlid>/<str:sort>', views.x1arb, name='x1arbitration'),
    path('arb0list/<str:lid>/<str:xlid>/<str:sort>', views.x0arb, name='x0arbitration'),

    path('allinstr/<str:lid>/<str:sort>', views.instrtodo, name='instruction to do list, all'),
    path('bd1/<str:lid>/<str:sort>', views.instroneb, name='instruction to do list, bound, rank 1'),
    path('bdnot1/<str:lid>/<str:sort>', views.instrotherb, name='instruction to do list, bound, other ranks'),
    path('notbd1/<str:lid>/<str:sort>', views.instronenotb, name='instruction to do list, not bound, rank 1'),
    path('notbdnot1/<str:lid>/<str:sort>', views.instrothernotb, name='instruction to do list, not bound, other ranks'),
    path('instrfilter/<str:lid>', views.instrfilter, name='instrfilter'),
    path('instrlist/<str:lid>/<str:xlid>/<str:sort>', views.xinstrlist, name='xinstr'),

    path('edlist/<str:lid>/<str:sort>', views.tobeedited, name='to be edited list'),
    path('edmotherlist/<str:lid>/<str:sort>', views.mothered, name='to be edited mother list'),
    path('ednotmotherlist/<str:lid>/<str:sort>', views.notmothered, name='to be edited notmother list'),
    path('edfilter/<str:lid>', views.filter_edlist, name='edfilter'),
    path('edmotherlist/<str:lid>/<str:xlid>/<str:sort>', views.xmothered, name='xto be edited mother list'),
    path('ednotmotherlist/<str:lid>/<str:xlid>/<str:sort>', views.xnotmothered, name='xto be edited notmother list'),
    path('ed/<str:sid>/<str:lid>', views.edition, name='edition'),
    path('current_status/<str:sid>/<str:lid>', views.current_status, name='current status'),

    path('999999999', views.checkinstr, name='message to checker'),
    path('xcheck', views.checkerfilter, name='checker filter'),
    path('xckbd/', views.xckbd, name='instrtodo for checker xbd'),
    path('xcknbd/', views.xcknbd, name='instrtodo for checker xnbd'),
    path('xckall/', views.xckall, name='instrtodo for checker xall'),

    path('pdf/<str:sid>/<str:lid>', views_pdf.pdfedition, name='pdfedition'),
    path('edallpdf/<str:lid>', views_pdf.edallpdf, name='alltopdf'),
    path('edmotherpdf/<str:lid>', views_pdf.motherpdf, name='mothertopdf'),
    path('ednotmotherpdf/<str:lid>', views_pdf.notmotherpdf, name='notmothertopdf'),
    path('edmotherpdf/<str:lid>/<str:xlid>', views_pdf.xmotherpdf, name='xmothertopdf'),
    path('ednotmotherpdf/<str:lid>/<str:xlid>', views_pdf.xnotmotherpdf, name='xnotmothertopdf'),

    path('csv/<str:sid>/<str:lid>', views_csv.some_view, name='kfùùz'),
    # path('edallpdf/<str:lid>', views_pdf.edallpdf, name='alltopdf'),
    # path('edmotherpdf/<str:lid>', views_pdf.motherpdf, name='mothertopdf'),
    # path('ednotmotherpdf/<str:lid>', views_pdf.notmotherpdf, name='notmothertopdf'),
    # path('edmotherpdf/<str:lid>/<str:xlid>', views_pdf.xmotherpdf, name='xmothertopdf'),
    # path('ednotmotherpdf/<str:lid>/<str:xlid>', views_pdf.xnotmotherpdf, name='xnotmothertopdf'),
]
