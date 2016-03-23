from django.db import transaction

from django.shortcuts import render, redirect

# Create your views here.
import logging
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from donate.models import *


def signin(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            return redirect('dashboard')
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse("Username and password doesnt match")


def register(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.POST['username'])
        if user:
            return HttpResponse("Username Already taken")

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password']
                )
                user.save()
        except:
            return HttpResponse("Error creating an account. Please register again")

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
            return render(request, 'volunteer/volunteer', context) ### Add volunteer page
        else:
            ngo = NGO(user=user)
            ngo.save()
            return render(request, 'ngo/contact.html', context)
    return redirect('signup')


def contact(request):
    if request.method == 'POST':
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
        return redirect('login')


def dashboard(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            return render(request, 'donor/donor.html')
        elif hasattr(user, 'volunteer'):
            # for deleting multiple elements, iterate through POST.keys(), and check if name attribute matches
            # Read Querydict docs
            pass
        elif hasattr(user, 'ngo'):
            context = {'ngo': user.ngo}
            return render(request, 'ngo/ngo.html', context)
    else:
        return redirect('login')


def create_ad(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated() and hasattr(user, 'donor'):
            item = Item.objects.get(name=request.POST['item_name'])
            donation = Donation(
                donor=user.donor,
                item=item,
                quantity=request.POST['quantity'],
                location=request.POST['address']
            )
            donation.save()
            return redirect('dashboard')


def create_event(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated() and hasattr(user, 'ngo'):
            event = Event(
                ngo=user.ngo,
                type=request.POST['type'],
                name=request.POST['name'],
                location=request.POST['location'],
                time=request.POST['time'],
                description=request.POST['description']
            )
            event.save()

            return redirect('dashboard')


def settings(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            if hasattr(user, 'donor'):
                user.donor.pincode = request.POST['pincode']
                user.donor.phone = request.POST['phone']
                user.donor.address = request.POST['address']
                user.donor.save()
                if request.POST['new_password']:
                    user.set_password(request.POST['new_password'])
                    user.save()
            elif hasattr(user, 'volunteer'):
                user.volunteer.address = request.POST['address']
                user.volunteer.phone = request.POST['phone']
            elif hasattr(user, 'ngo'):
                pass
    return redirect('dashboard')


def view_events(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            context = {'events': Event.objects.all()}
            return render(request, 'donor/viewEvents.html', context)
        return HttpResponse("Invalid page")
    return redirect('home')


def ngo_list(request):      # Donor
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            context = {'ngos': NGO.objects.all()}
            return render(request, 'donor/ngoList.html', context)
        return HttpResponse("Invalid page")
    return redirect('home')


def view_items(request):    # For donors
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            context = {'items': Item.objects.all()}
            return render(request, 'donor/items_required.html', context)
        return HttpResponse("Invalid page")
    return redirect('home')


def edit_req(request):
    pass


def req_vol(request):
    pass


def log_out(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('home')


def about(request):
    return render(request, 'about.html')


def signup(request):
    context = {"error_message": ''}
    context.update(csrf(request))
    return render(request, 'register.html', context)


def home(request):
    print(request.user.username)
    if request.user.is_authenticated():
        return redirect('dashboard')
    else:
        return render(request, 'home.html')


def log_in(request):
    context = {"error_message": ''}
    context.update(csrf(request))
    return render(request, 'login.html', context)


def create_ad_view(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            context = {'donor': user.donor}
            context.update(csrf(request))
            return render(request, 'donor/create_ad.html', context)
        return HttpResponse("Invalid page")
    return redirect('login')


def create_event_view(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'ngo'):
            context = {}
            context.update(csrf(request))
            return render(request, 'ngo/create_event.html', context)
        return HttpResponse("Invalid page")
    return redirect('login')


def edit_req_view(request):
    pass


def req_vol_view(request):
    pass


def settings_view(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            context = {'donor': user.donor}
            context.update(csrf(request))
            return render(request, 'donor/settings.html', context)
        elif hasattr(user, 'volunteer'):
            context = {'volunteer': user.volunteer}
            context.update(csrf(request))
            return render(request, 'ngo/settings.html', context)
        elif hasattr(user, 'ngo'):
            context = {'ngo': user.ngo}
            context.update(csrf(request))
            return render(request, 'donor/settings.html', context)
    return redirect('login')


def guidelines(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            return render(request, 'donor/guidelines.html')
        elif hasattr(user, 'volunteer'):
            pass
        elif hasattr(user, 'ngo'):
            pass
    return redirect('login')


def join_as_vol(request):
    user = request.user
    if user.is_authenticated() and hasattr(user, 'donor'):
        logout(request)
        return redirect('signup')
    return redirect('login')
