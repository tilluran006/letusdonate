from django.shortcuts import render

# Create your views here.
import logging
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from donate.models import Donor, Volunteer, Admin, NGO, User


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

def register(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.POST['username'])
        if not user:
            user = User.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password']
            )
            user.save()
            type = request.POST['type']
            if type == 'donor':
                donor = Donor(user=user)
                donor.save()
                return render(request, reverse('contact'))
            elif type == 'vol':
                volunteer = Volunteer(user=user)
                volunteer.save()
                return render(request, reverse('contact'))
            else:
                ngo = NGO(user=user)
                ngo.save()
                #Return render(Next page)
        else:
            return render(request, reverse(register), {"error_message": 'Username already taken'})


def contact(request):
    if request.user.is_authenticated():
        if request.user.donor:
            donor = request.user.donor
            donor.address = request.POST
        elif request.user.volunteer:
            pass


def dashboard(request, user_type):
    # If donor render donor/donor.html
    # else render volunteer/<>.html
    # else ngo/<>.html
    pass

def settings(request):
    #if donor then display
    return render(request, 'donor/settings.html')

def log_out(request):
    #Code for logout
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def signup(request):
    return render(request, 'register.html', {"error_message": ''})

def home(request):
    # if logged in redirect to dashboard
    return render(request, 'home.html')

def log_in(request):
    return render(request, 'login.html')

