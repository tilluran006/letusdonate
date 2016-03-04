from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout

#
# def login(request):
#     if request.method == 'POST':
#         user = authenticate(username=request.POST['username'], password=request.POST[])