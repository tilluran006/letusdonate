from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
import logging
from donate.models import Donor, Volunteer, Admin, NGO


def signin(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            login(request, user)
            if request.POST['account_type' == 'donor']:
                return HttpResponseRedirect('')
        # if isinstance(user.role, Donor):
        #     pass
        # elif isinstance(user, Volunteer):
        #     pass
        # elif isinstance(user, Admin):
        #     pass
        # elif isinstance(user, NGO):
        #     pass

def signup(request):
    pass

def home(request, dummy):
    return render(request, 'main.html')

def login(request):
    return render(request, 'login.html')