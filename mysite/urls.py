"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.conf import settings


urlpatterns = [
    path('', include('epl.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
#    path('accounts/login/', auth_views.LoginView.as_view()),
#    path('accounts/password_change/', auth_views.LoginView.as_view(template_name='epl/password_change.html')),
#    path('accounts/password_change/done/', auth_views.LoginView.as_view(template_name='epl/password_change_done.html')),
#    path('accounts/password_reset/', auth_views.LoginView.as_view(template_name='epl/password_reset.html')),
#    path('accounts/password_reset/done/', auth_views.LoginView.as_view(template_name='epl/password_reset_done.html')),
#    path('accounts/reset/<uidb64>/<token>/', auth_views.LoginView.as_view(template_name='epl/password_reset_confirm.html')),
#    path('accounts/reset/done/', auth_views.LoginView.as_view(template_name='epl/password_reset_complete.html')), 
    path('i18n/', include('django.conf.urls.i18n')),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")), ),
]
