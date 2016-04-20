import os

from django.db import transaction
from django.shortcuts import render, redirect

# Create your views here.
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from donate.models import *
from django.core.mail import send_mail

IMG_PATH="donate/static/user_uploads/"


def signin(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse("Username and password doesnt match")
    return redirect('login')


def register(request):
    if request.method == 'POST':
        user = User.objects.filter(username=request.POST['username'])
        if user:
            return HttpResponse("Username Already taken")

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password'],
                    first_name=request.POST['name']
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
            return render(request, 'volunteer/contact.html', context)
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
            donor.city = request.POST['city']
            donor.pincode = request.POST['pin']
            donor.phone = request.POST['phone']
            donor.save()
        elif hasattr(user, 'volunteer'):
            vol = user.volunteer
            vol.address = request.POST['address']
            vol.city = request.POST['city']
            vol.pincode = request.POST['pin']
            vol.phone = request.POST['phone']
            vol.save()
        elif hasattr(user, 'ngo'):
            ngo = user.ngo
            ngo.description = request.POST['description']
            ngo.phone = request.POST['phone']
            ngo.pincode = request.POST['pin']
            ngo.address = request.POST['address']
            ngo.city = request.POST['city']
            image_upload = request.FILES['file']
            if image_upload:
                try:
                    with transaction.atomic():
                        with open(IMG_PATH + str(user.id) + '.jpg', 'wb+') as f:
                            for chunk in image_upload.chunks():
                                f.write(chunk)
                        ngo.image = 'static/user_uploads/' + str(user.id) + '.jpg'
                except:
                    ngo.image = 'static/user_uploads/default.jpg'
                    ngo.save()
                    return HttpResponse("User Details Saved. Error uploading image. Go to settings and retry")
            ngo.save()
        return redirect('login')
    return redirect('home')


def dashboard(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            context = {'donations': Donation.objects.filter(donor=user.donor)}
            return render(request, 'donor/donor.html', context)
        elif hasattr(user, 'volunteer'):
            context = {
                'donor_items': Donation.objects.filter(status="donor"),
                'vol_items': Donation.objects.filter(status="vol"),
                'ngo_items': Donation.objects.filter(status="ngo"),
            }
            context.update(csrf(request))
            return render(request, 'volunteer/volunteer.html', context)
        elif hasattr(user, 'ngo'):
            context = {'ngo': user.ngo}
            return render(request, 'ngo/ngo.html', context)
        logout(request)
    return redirect('login')


def create_ad(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            if hasattr(user, 'donor'):
                item = Item.objects.get(name=request.POST['itemname'])
                donation = Donation(
                    donor=user.donor,
                    item=item,
                    quantity=request.POST['quantity'],
                    description=request.POST['description'],
                    location=request.POST['address'],
                    city=request.POST['city'],
                    contact=request.POST['phone'],
                    status="donor"
                )
                donation.save()
                return redirect('dashboard')
            return redirect('login')
    return redirect('home')


def create_event(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            if hasattr(user, 'ngo'):
                event = Event(
                    ngo=user.ngo,
                    type=request.POST['type'],
                    name=request.POST['name'],
                    location=request.POST['location'],
                    city=request.POST['city'],
                    time=request.POST['time'],
                    description=request.POST['description']
                )
                event.save()
                return redirect('dashboard')
            return redirect('login')
    return redirect('home')


def settings(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            if hasattr(user, 'donor'):
                donor = user.donor
                donor.pincode = request.POST['pincode']
                donor.phone = request.POST['phone']
                donor.address = request.POST['address']
                donor.city = request.POST['city']
                donor.save()
                user.first_name = request.POST['name']
                if request.POST['new_password']:
                    user.set_password(request.POST['new_password'])
                user.save()
            elif hasattr(user, 'volunteer'):
                vol = user.volunteer
                vol.address = request.POST['address']
                vol.city = request.POST['city']
                vol.phone = request.POST['phone']
                vol.pincode = request.POST['pincode']
                vol.save()
                user.first_name = request.POST['name']
                if request.POST['new_password']:
                    user.set_password(request.POST['new_password'])
                user.save()
            elif hasattr(user, 'ngo'):
                ngo = user.ngo
                user.first_name = request.POST['name']
                if request.POST['new_password']:
                    user.set_password(request.POST['new_password'])
                user.save()
                ngo.description = request.POST['description']
                ngo.phone = request.POST['phone']
                ngo.pincode = request.POST['pincode']
                ngo.address = request.POST['address']
                ngo.city = request.POST['city']
                image_upload = request.FILES['file']

                if image_upload:
                    try:
                        with transaction.atomic():
                            with open(IMG_PATH + str(user.id) + '.jpg', 'wb+') as f:
                                for chunk in image_upload.chunks():
                                    f.write(chunk)
                            ngo.image = 'static/user_uploads/' + str(user.id) + '.jpg'
                    except:
                        ngo.image = 'static/user_uploads/default.jpg'
                        ngo.save()
                        return HttpResponse("User Settings Saved. Error uploading image. Go back to settings and retry")
                ngo.save()
    return redirect('dashboard')


def view_events(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            context = {'events': Event.objects.all()}
            return render(request, 'donor/viewEvents.html', context)
        elif hasattr(user, 'volunteer'):
            context = {
                'events': Event.objects.filter(volunteers=None),
                'events_vol': Event.objects.exclude(volunteers=None)
            }
            context.update(csrf(request))
            return render(request, 'volunteer/viewEvents.html', context)
        elif hasattr(user, 'ngo'):
            context = {'events': Event.objects.all(), 'my_events': Event.objects.filter(ngo=user.ngo)}
            return render(request, 'ngo/viewEvents.html', context)
        return HttpResponse("User is not authorized to view the requested page")
    return redirect('home')


def ngo_list(request):      # Donor
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            context = {'ngos': NGO.objects.all()}
            return render(request, 'donor/ngoList.html', context)
        return HttpResponse("User is not authorized to view the requested page")
    return redirect('home')


def view_items(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            context = {'items': Item.objects.all()}
            return render(request, 'donor/items_required.html', context)
        elif hasattr(user, 'ngo'):
            context = {'donations': Donation.objects.filter(status="vol")}
            return render(request, 'ngo/view-items.html', context)
        elif hasattr(user, 'volunteer'):
            return render(request, 'volunteer/items_required.html')
        return HttpResponse("User is not authorized to view the requested page")
    return redirect('home')


def edit_req(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            if hasattr(user, 'ngo'):
                item = Item.objects.get(name=request.POST['item_name'])
                item_quantity = ItemQuantity(item=item, ngo=user.ngo, quantity=request.POST['item_quantity'])
                item_quantity.save()
                return redirect('edit_req_view')
            return HttpResponse("User is not authorized to view the requested page")
    return redirect('dashboard')


def collect_items(request):     # Volunteer - collect from donors
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            if hasattr(user, 'volunteer'):
                for id in request.POST['donation']:
                    donation = Donation.objects.get(id=id)
                    donation.status = "vol"
                    donation.save()
            return HttpResponse("User is not authorized to view the requested page")
    return redirect('dashboard')


def deliver_items(request):     # Volunteer - deliver to ngo
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            if hasattr(user, 'volunteer'):
                for id in request.POST['donation']:
                    donation = Donation.objects.get(id=id)
                    donation.status = "ngo"
                    donation.save()
            return HttpResponse("User is not authorized to view the requested page")
    return redirect('dashboard')


def volunteer_event(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            if hasattr(user, 'volunteer'):
                event = Event.objects.get(id=request.POST['event_id'])
                user.volunteer.events_volunteered.add(event)
                user.volunteer.save()
                return redirect('view_events')
            return HttpResponse("User is not authorized to view the requested page")
    return redirect('home')


def log_out(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('home')


def about(request):
    if request.user.is_authenticated():
        context = {'logged_in': True}
    else:
        context = {'logged_in': False}
    return render(request, 'about.html', context)


def signup(request):
    context = {}
    context.update(csrf(request))
    return render(request, 'register.html', context)


def home(request):
    print(request.user.username)
    if request.user.is_authenticated():
        return redirect('dashboard')
    else:
        return render(request, 'home.html')


def log_in(request):
    context = {}
    context.update(csrf(request))
    return render(request, 'login.html', context)


def create_ad_view(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            items = Item.objects.all()
            context = {'donor': user.donor, 'items': items}
            context.update(csrf(request))
            return render(request, 'donor/create_ad.html', context)
        return HttpResponse("User is not authorized to view the requested page")
    return redirect('login')


def create_event_view(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'ngo'):
            context = {}
            context.update(csrf(request))
            return render(request, 'ngo/create_event.html', context)
        return HttpResponse("User is not authorized to view the requested page")
    return redirect('login')


def edit_req_view(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'ngo'):
            context = {'item_quantities': ItemQuantity.objects.filter(ngo=user.ngo)}
            context.update(csrf(request))
            return render(request, 'ngo/editReq.html', context)
        return HttpResponse("User is not authorized to view the requested page")
    return redirect('login')


def settings_view(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            context = {'donor': user.donor}
            context.update(csrf(request))
            return render(request, 'donor/settings.html', context)
        elif hasattr(user, 'volunteer'):
            context = {'vol': user.volunteer}
            context.update(csrf(request))
            return render(request, 'volunteer/settings.html', context)
        elif hasattr(user, 'ngo'):
            context = {'ngo': user.ngo}
            context.update(csrf(request))
            return render(request, 'ngo/settings.html', context)
    return redirect('login')


def guidelines(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            return render(request, 'donor/guidelines.html')
        elif hasattr(user, 'volunteer'):
            return render(request, 'volunteer/guidelines.html')
        elif hasattr(user, 'ngo'):
            return render(request, 'ngo/guidelines.html')
    return redirect('login')


def join_as_vol(request):
    user = request.user
    if user.is_authenticated() and hasattr(user, 'donor'):
        logout(request)
        return redirect('signup')
    return redirect('login')


def faq(request):
    if request.user.is_authenticated():
        context = {'logged_in': True}
    else:
        context = {'logged_in': False}
    return render(request, 'faq.html', context)


def contact_us_view(request):
    user = request.user
    if user.is_authenticated():
        context = {
            'logged_in': True,
            'name': user.first_name,
            'email': user.email
        }
    else:
        context = {
            'logged_in': False,
            'name': "",
            'email': ""
        }
    context.update(csrf(request))
    return render(request, 'contact-form.html', context)


def contact_us(request):
    if request.method == 'POST':
        mail_from = request.POST['name']
        email_id = request.POST['email']
        subject = "LetUsDonate: " + request.POST['subject']
        content = "Name: %s\nEmail ID: %s\n\n\n%s" % (mail_from, email_id, request.POST['message'])
        status = send_mail(subject, content, email_id, ['manithcooldude@gmail.com'], fail_silently=True)
        if status == 0:
            return HttpResponse("Email failed to send")
    return redirect('home')
