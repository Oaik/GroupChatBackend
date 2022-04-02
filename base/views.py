from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import random
import time
import json
from .models import RoomMember
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

from base.models import Contact

# Create your views here.

# contact


def index (request) :
    contacts = Contact.objects.all()
    search_input = request.GET.get('search-area')
    if search_input :
        contacts = Contact.objects.filter(full_name__startswith=search_input)
    else :
        contacts = Contact.objects.all()
        search_input = ''
    context = {'contacts' : contacts}
    return render(request, 'base/index.html', context)

def addContact (request) :
    if request.method == 'POST' :
        new_contact = Contact(
            full_name =  request.POST['fullname'],
            relationship = request.POST['relationship'],
            email = request.POST['email'],
            phone_number = request.POST['phone-number'],
            address = request.POST['address']
        )
        new_contact.save()
        return redirect('/contact-list/')
    return render(request, 'base/new.html')

def contactProfile (request, pk) :
    contact = Contact.objects.get(id = pk)
    context = {'contact' : contact}
    return render(request, 'base/contact-profile.html', context)


def editContact(request, pk):
    contact = Contact.objects.get(id=pk)

    if request.method == 'POST' :
        contact.full_name = request.POST['fullname']
        contact.relationship = request.POST['relationship']
        contact.phone_number = request.POST['phone-number']
        contact.email = request.POST['e-mail']
        contact.address = request.POST['address']
        contact.save()

        return redirect('/profile/'+str(contact.id))
    context = {'contact' : contact}
    return render(request, 'base/edit.html', context)

def deleteContact (request, pk) :
    contact = Contact.objects.get(id=pk)
    if request.method == 'POST' :
        contact.delete()
        return redirect('/contact-list/')
    context = {'contact' : contact}
    return render(request, 'base/delete.html', context)



# user
class CustomLoginView (LoginView) :
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('lobby')


class RegisterPage (FormView) :
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('lobby')

    def form_valid(self, form):
        user = form.save()
        if user is not None :
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)


    def get (self, *args, **kwargs) :
        if self.request.user.is_authenticated :
            return redirect('lobby')
        return super(RegisterPage, self).get(*args, **kwargs)

def getToken (request) :
    appId = '38e3a9c1018e4d6ca9b60f351d15c7c5'
    appCertificate = '630d80cc553845b3b9c5f5b4f882466c'
    # http: // 127.0.0.1: 8000 / get_token /?channel = room1
    # channelName = room1
    channelName = request.GET.get('channel')
    # i need to generate random number for the user
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    # if role = 1 so it's a host
    # if role = 2 so it's a guest
    # anyway it's not a matter with authentication
    # so i will leave it 1 for everybody
    role = 1
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    # JsonResponse is an HttpResponse subclass that helps to create a JSON-encoded response.
    return JsonResponse({'token' : token, 'uid' : uid}, safe=False)

def lobby (request) :
    if not request.user.is_authenticated:
        return render(request, 'base/login.html')
    return render(request, 'base/lobby.html')


def room (request) :
    if not request.user.is_authenticated:
        return render(request, 'base/login.html')
    return render(request, 'base/room.html')

@csrf_exempt
def createMember (request) :
    # get data from front-end then parse it by json
    data = json.loads(request.body)
    # i need to check if the member is exist before create it
    # created will be boolean

    member, created = RoomMember.objects.get_or_create(
        name = data['name'],
        uid = data['UID'],
        room_name = data['room_name']
    )
    return JsonResponse({'name' : data['name']}, safe=False)

def getMember (request) :
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )

    name = member.name
    return JsonResponse({'name':member.name}, safe=False)


@csrf_exempt
def deleteMember (request) :
    # get data from front-end then parse it by json
    data = json.loads(request.body)

    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name'],
    )

    member.delete()

    return JsonResponse('member was deleted', safe=False)

