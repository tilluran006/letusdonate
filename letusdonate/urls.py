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
    url(r'^admin/', admin.site.urls),
    url(r'^signin', signin, name="signin"),
    url(r'^register$', register, name="register"),
    url(r'^logout', log_out, name="logout"),
    url(r'^contact', contact, name="contact"),  # Donor,volunteer contact: To be shown after signup
    # url(r'^((donor)|(volunteer)|(ngo))/?$', dashboard, name="dashboard"),
    url(r'^<user_type>/?$', dashboard, name="dashboard"),

    url(r'^$', home, name="home"),  # Before logging in
    url(r'^login', log_in, name="login"),
    url(r'^signup$', signup, name="signup"),
    url(r'^<user_type>/settings$', settings, name="settings"),
]

