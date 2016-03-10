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

        if user is not None:
            login(request, user)
            return render(request, reverse('dashboard'))
        else:
            return HttpResponse("Username and password doesnt match")


def register(request):
    if request.method == 'POST':
        context = {}
        context.update(csrf(request))
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
            context['user_name'] = request.POST['username']
            context.update(csrf(request))
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
    if user.donor:
        donor = user.donor
        donor.address = request.POST['address']
        donor.pincode = request.POST['pin']
        donor.phone = request.POST['phone']
    elif request.user.volunteer:
        pass
    elif user.ngo:
        ngo = user.ngo
        request.user.first_name = request.POST['name']
        ngo.description = request.POST['description']
        ngo.phone = request.POST['phone']
        ngo.pincode = request.POST['pin']

    login(request, user)
    return render(request, reverse(dashboard))


def dashboard(request):
    user = request.user
    if user.is_authenticated():
        if user.donor:
            return render(request, 'donor/donor.html')
        elif user.volunteer:
            pass
        elif user.ngo:
            pass


def create_ad(request):
    user = request.user
    if user.is_authenticated() and user.donor:
        ###item = Item
        ###donation = Donation(donor=user.donor, )
        return HttpResponseRedirect(reverse('dashboard'))

def create_event(request):
    # Check if volunteer
    # Add to db
    pass

def settings(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            if user.donor:
                user.donor.pincode = request.POST['pincode']
                user.donor.phone = request.POST['phone']
                user.donor.address = request.POST['address']
                user.set_password(request.POST['new_password'])
                user.save()
            elif user.volunteer:
                pass
            elif user.ngo:
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
    if request.user.is_authenticated():
        return render(request, reverse('dashboard'))
    return render(request, 'home.html')

def log_in(request):
    return render(request, 'login.html', {"error_message": ''})

