"""letusdonate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from donate.views import *

urlpatterns = [
    #Same for all
    url(r'^admin/', admin.site.urls),
    url(r'^signin$', signin, name="signin"),
    url(r'^register', register, name="register"),
    url(r'^logout$', log_out, name="logout"),
    url(r'^$', home, name="home"),  # Before logging in
    url(r'^signup$', signup, name="signup"),

    #Dummy views
    url(r'^login$', log_in, name="login"),
    url(r'^create_ads', create_ad_view, name="create_ad_view"),

    #user specific
    url(r'^create_event$', create_event, name="create_event"),
    url(r'^create_ad$', create_ad, name="create_ad"),
    url(r'^join_as_vol$', join_as_vol, name="join_as_vol"),

    #different view for each user
    url(r'^contact$', contact, name="contact"),  # Donor,volunteer contact: To be shown after signup
    url(r'^dashboard/?$', dashboard, name="dashboard"),
    url(r'^settings$', settings, name="settings"),
    url(r'^guidelines$', guidelines, name="guidelines"),
]

