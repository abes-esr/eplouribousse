from django.urls import path

from . import views, views_pdf, views_csv

urlpatterns = [
    path('', views.selectbdd, name='bddselect'),
    path('<str:bdd>', views.home, name='project_home'),
    path('<str:bdd>/adminbase', views.adminbase, name='project administration'),
    path('<str:bdd>/excl_adm', views.excl_adm, name='exclusions administration'),
    path('<str:bdd>/projinfos_adm', views.projinfos_adm, name='project infos administration'),
    path('<str:bdd>/lib_adm', views.lib_adm, name='libraries (i.e. collections) infos administration'),
    path('<str:bdd>/alerts_adm', views.alerts_adm, name='alerts administration'),
    path('<str:bdd>/alerts_user', views.alerts_user, name='user alerts administration'),
    path('<str:bdd>/admins_adm', views.admins_adm, name='administrators administration'),
    path('<str:bdd>/uters_adm', views.uters_adm, name='users administration'),
    path('<str:bdd>/authusrs_adm', views.authusrs_adm, name='authorized users administration'),
    path('<str:bdd>/diffusion/<str:smthng>/<str:origcontent>', views.diffusion, name='mail to diffusion list'),

    path('default/password_reset/', views.password_reset_request, name='password_reset'),
    path('default/globadm', views.globadm, name='global administration'),
    path('default/about', views.about, name='about'),
    path('default/license', views.license, name='license'),
    path('default/cgu', views.cgu, name='cgu'),
    path('default/confidentialite', views.confidentialite, name='confidentialite'),
    path('default/contactdev', views.contactdev, name='contact du développeur'),
    path('default/webmaster', views.webmstr, name='webmaster'),
    path('<str:bdd>/projectmaster', views.projmstr, name='projectmaster'),
    path('<str:bdd>/router/<str:lid>', views.router, name='route to the right list'),
    path('default/lang', views.lang, name='language'),
    path('default/disconnect', views.logout_view, name='disconnection'),
    path('<str:bdd>/timeout/<str:sid>/<str:lid>', views.notintime, name='not in time'),
    path('<str:bdd>/dashboard', views.indicators, name='indicators'),
    path('<str:bdd>/dashboard/<str:lid>', views.indicators_x, name='indicators_x'),
    path('<str:bdd>/gen_search', views.general_search, name='multicriteria searching'),
    path('<str:bdd>/gen_search_results/<str:lid>/<str:xlid>/<path:recset>/<str:sort>', views.cross_list, name='results list to multicriteria search'),
    path('<str:bdd>/reinit/<str:sid>', views.reinit, name='reinitialisation'),

    path('<str:bdd>/rk/<str:sid>/<str:lid>', views.takerank, name='ranking'),

    path('<str:bdd>/add/<str:sid>/<str:lid>', views.addinstr, name='add instruction'),
    path('<str:bdd>/sel/<str:sid>/<str:lid>', views.selinstr, name='select instruction to modify'),
    path('<str:bdd>/mod/<str:sid>/<str:lid>/<int:linetomodify>', views.modinstr, name='modify instruction'),
    path('<str:bdd>/del/<str:sid>/<str:lid>', views.delinstr, name='delete instruction'),
    path('<str:bdd>/end/<str:sid>/<str:lid>', views.endinstr, name='end of instruction'),

    path('<str:bdd>/rklist/<str:lid>/<str:sort>', views.ranktotake, name='to be ranked list'),
    path('<str:bdd>/modifrklist/<str:lid>/<str:sort>', views.modifranklist, name='modify a rank list'),
    path('<str:bdd>/rkfilter/<str:lid>', views.filter_rklist, name='rkfilter'),
    path('<str:bdd>/rklist/<str:lid>/<str:xlid>/<str:sort>', views.xranktotake, name='xto be ranked list'),
    path('<str:bdd>/excl', views.excllist, name='exclusions'),
    path('<str:bdd>/faulty', views.faulty, name='faulty'),
    path('<str:bdd>/listall/<str:lid>/<str:sort>', views.listall, name='all'),
    path('<str:bdd>/listallfilter/<str:lid>/<str:sort>', views.filter_listall, name='filter for listall'),
    path('<str:bdd>/listall/<str:lid>/<str:xlid>/<str:sort>', views.xlistall, name='all crossed'),

    path('<str:bdd>/arb/<str:lid>/<str:sort>', views.arbitration, name='arbitration'),
    path('<str:bdd>/arbrk1_list/<str:lid>/<str:sort>', views.arbrk1, name='arbitration rank 1'),
    path('<str:bdd>/arbnork1_list/<str:lid>/<str:sort>', views.arbnork1, name='arbitration no rank 1'),
    path('<str:bdd>/arbfilter/<str:lid>', views.filter_arblist, name='arbfilter'),
    path('<str:bdd>/arblist/<str:lid>/<str:xlid>/<str:sort>', views.xarbitration, name='xarbitration'),
    path('<str:bdd>/arb1list/<str:lid>/<str:xlid>/<str:sort>', views.x1arb, name='x1arbitration'),
    path('<str:bdd>/arb0list/<str:lid>/<str:xlid>/<str:sort>', views.x0arb, name='x0arbitration'),

    path('<str:bdd>/allinstr/<str:lid>/<str:sort>', views.instrtodo, name='instruction to do list, all'),
    path('<str:bdd>/bd1/<str:lid>/<str:sort>', views.instroneb, name='instruction to do list, bound, rank 1'),
    path('<str:bdd>/bdnot1/<str:lid>/<str:sort>', views.instrotherb, name='instruction to do list, bound, other ranks'),
    path('<str:bdd>/notbd1/<str:lid>/<str:sort>', views.instronenotb, name='instruction to do list, not bound, rank 1'),
    path('<str:bdd>/notbdnot1/<str:lid>/<str:sort>', views.instrothernotb, name='instruction to do list, not bound, other ranks'),
    path('<str:bdd>/instrfilter/<str:lid>', views.instrfilter, name='instrfilter'),
    path('<str:bdd>/instrlist/<str:lid>/<str:xlid>/<str:sort>', views.xinstrlist, name='xinstr'),

    path('<str:bdd>/edlist/<str:lid>/<str:sort>', views.tobeedited, name='to be edited list'),
    path('<str:bdd>/edmotherlist/<str:lid>/<str:sort>', views.mothered, name='to be edited mother list'),
    path('<str:bdd>/ednotmotherlist/<str:lid>/<str:sort>', views.notmothered, name='to be edited notmother list'),
    path('<str:bdd>/edfilter/<str:lid>', views.filter_edlist, name='edfilter'),
    path('<str:bdd>/edmotherlist/<str:lid>/<str:xlid>/<str:sort>', views.xmothered, name='xto be edited mother list'),
    path('<str:bdd>/ednotmotherlist/<str:lid>/<str:xlid>/<str:sort>', views.xnotmothered, name='xto be edited notmother list'),
    path('<str:bdd>/ed/<str:sid>/<str:lid>', views.edition, name='edition'),
    path('<str:bdd>/current_status/<str:sid>/<str:lid>', views.current_status, name='current status'),
    path('<str:bdd>/statadmin/<str:sid>', views.statadmin, name='status admin'),
    path('<str:bdd>/instradmin/<str:id>', views.instradmin, name='instruction admin'),

    path('<str:bdd>/999999999', views.checkinstr, name='message to checker'),
    path('<str:bdd>/xcheck', views.checkerfilter, name='checker filter'),
    path('<str:bdd>/xckbd', views.xckbd, name='instrtodo for checker xbd'),
    path('<str:bdd>/xcknbd', views.xcknbd, name='instrtodo for checker xnbd'),
    path('<str:bdd>/xckall', views.xckall, name='instrtodo for checker xall'),

    path('<str:bdd>/pdf/<str:sid>/<str:lid>', views_pdf.pdfedition, name='pdfedition'),
    path('<str:bdd>/edallpdf/<str:lid>', views_pdf.edallpdf, name='alltopdf'),
    path('<str:bdd>/edmotherpdf/<str:lid>', views_pdf.motherpdf, name='mothertopdf'),
    path('<str:bdd>/ednotmotherpdf/<str:lid>', views_pdf.notmotherpdf, name='notmothertopdf'),
    path('<str:bdd>/edmotherpdf/<str:lid>/<str:xlid>', views_pdf.xmotherpdf, name='xmothertopdf'),
    path('<str:bdd>/ednotmotherpdf/<str:lid>/<str:xlid>', views_pdf.xnotmotherpdf, name='xnotmothertopdf'),

    path('<str:bdd>/csv/<str:lid>/<str:xlid>/<path:recset>/<str:what>/<str:length>', views_csv.simple_csv, name='csv export'),
    path('default/csv/uters', views_csv.uters_csv, name='csv uters export'),
]
