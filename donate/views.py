from django.shortcuts import render

# Create your views here.
import logging
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from donate.models import Donor, Volunteer, Admin, NGO, User, Donation, Item


def signin(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            login(request, user)
            return render(request, reverse('dashboard'))
        else:
            return HttpResponse("Username and password doesnt match")


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
                return render(request, 'donor/contact.html')
            elif type == 'vol':
                volunteer = Volunteer(user=user)
                volunteer.save()
                return render(request, '') ### Add volunteer page
            else:
                ngo = NGO(user=user)
                ngo.save()
                return render(request, 'ngo/ngoregister.html')
        else:
            return render(request, reverse(signup), {"error_message": 'Username already taken'})


def contact(request):
    if request.user.is_authenticated():
        if request.user.donor:
            donor = request.user.donor
            donor.address = request.POST['address']
            donor.pincode = request.POST['pin']
            donor.phone = request.POST['phone']
        elif request.user.volunteer:
            pass
        elif request.user.ngo:
            ngo = request.user.ngo
            request.user.first_name = request.POST['name']
            ngo.description = request.POST['description']
            ngo.phone = request.POST['phone']
            ngo.pincode = request.POST['pin']
            ngo.image = request.FILES['file']

        return render(request, reverse(dashboard))
    else:
        return HttpResponseRedirect(reverse(home))


def dashboard(request):
    # If donor render donor/donor.html
    # else render volunteer/<>.html
    # else ngo/<>.html
    pass

def create_ad(request):
    user = request.user
    if user.is_authenticated() and user.donor:
        ###item = Item
        ###donation = Donation(donor=user.donor, )
        return render(request, reverse('dashboard'))

def create_event(request):
    # Check if volunteer
    # Add to db
    pass

def settings(request):
    # Update db based on user type
    pass

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
    return render(request, 'login.html', {"error_message": ''})

