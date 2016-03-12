from django.shortcuts import render

# Create your views here.
import logging
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from donate.models import Donor, Volunteer, Admin, NGO, User, Donation, Item


def signin(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard'))
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        print "######", request.user.username
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return HttpResponse("Username and password doesnt match")


def register(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password']
        )
        user.save()
        type = request.POST['type']
        context = {'user_name': request.POST['username']}
        context.update(csrf(request))
        if type == 'donor':
            donor = Donor(user=user)
            donor.save()
            return render(request, 'donor/contact.html', context)
        elif type == 'vol':
            volunteer = Volunteer(user=user)
            volunteer.save()
            return render(request, '', context) ### Add volunteer page
        else:
            ngo = NGO(user=user)
            ngo.save()
            return render(request, 'ngo/ngoregister.html', context)
        # else:
        #     return render(request, reverse(signup), {"error_message": 'Username already taken'})


def contact(request):
    user = User.objects.get(username=request.POST['user_name'])
    if hasattr(user, 'donor'):
        donor = user.donor
        donor.address = request.POST['address']
        donor.pincode = request.POST['pin']
        donor.phone = request.POST['phone']
        donor.save()
    elif hasattr(user, 'volunteer'):
        pass
    elif hasattr(user, 'ngo'):
        ngo = user.ngo
        ngo.description = request.POST['description']
        ngo.phone = request.POST['phone']
        # ngo.pincode = request.POST['pin']
        ngo.save()
        user.first_name = request.POST['name']
        user.save()
    return HttpResponseRedirect(reverse('login'))


def dashboard(request):
    logging.info(request.user.username)
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            return render(request, 'donor/donor.html')
        elif hasattr(user, 'volunteer'):
            pass
        elif hasattr(user, 'ngo'):
            return render(request, 'ngo/ngo.html')


def create_ad(request):
    user = request.user
    if user.is_authenticated() and hasattr(user, 'donor'):
        ###item = Item
        ###donation = Donation(donor=user.donor, )
        return HttpResponseRedirect(reverse('dashboard'))

def create_event(request):
    user = request.user
    if user.is_authenticated() and hasattr(user, 'donor'):
        pass

def settings(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            if hasattr(user, 'donor'):
                user.donor.pincode = request.POST['pincode']
                user.donor.phone = request.POST['phone']
                user.donor.address = request.POST['address']
                user.donor.save()
                user.set_password(request.POST['new_password'])
                user.save()
            elif hasattr(user, 'volunteer'):
                pass
            elif hasattr(user, 'ngo'):
                pass

def log_out(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect(reverse('home'))

def about(request):
    return render(request, 'about.html')

def signup(request):
    return render(request, 'register.html', {"error_message": ''})

def home(request):
    print(request.user.username)
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard')
    else:
        return render(request, 'home.html')

def log_in(request):
    context = {"error_message": ''}
    context.update(csrf(request))
    return render(request, 'login.html', context)

def create_ad_view(request):
    user = request.user
    if user.is_authenticated() and hasattr(user, 'donor'):
        context = {}
        context.update(csrf(request))
        return render(request, 'donor/create_ad.html', context)

def guidelines(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            return render(request, 'donor/guidelines.html')
        elif hasattr(user, 'volunteer'):
            pass
        elif hasattr(user, 'ngo'):
            pass

def events(request):    #For donor
    user = request.user
    if user.is_authenticated() and hasattr(user, 'donor'):
        pass

def join_as_vol(request):
    user = request.user
    if user.is_authenticated() and hasattr(user, 'donor'):
        logout(request)
        return HttpResponseRedirect(reverse('signup'))
