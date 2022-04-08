from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from agora_token_builder import RtcTokenBuilder
import random
import time
import json
from .models import RoomMember
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User


from base.models import Contact



from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required

#
# Create your views here.

# user form
def registerPage (request) :
    if request.user.is_authenticated :
        return redirect('lobby')
    else :
        form = CreateUserForm()
        if request.method == 'POST' :
            form = CreateUserForm(request.POST)
            if form.is_valid() :
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

        context = {'form' : form}
        return render(request, 'base/registerPage.html', context)

def loginPage (request) :
    if request.user.is_authenticated :
        return redirect('lobby')
    else :
        if request.method == 'POST' :
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None :
                login(request, user)
                return redirect('lobby')
            else :
                messages.info(request, 'Username or password is incorrect')
        return render(request, 'base/loginPage.html')

def logoutPage (request) :
    logout(request)
    return render(request, 'base/loginPage.html')

# contact

@login_required(login_url='login')
def index (request) :
    contacts = Contact.objects.all()
    search_input = request.GET.get('search-area')
    if search_input :
        contacts = Contact.objects.filter(pk=search_input)
    else :
        contacts = Contact.objects.all()
        search_input = ''
    context = {'contacts' : contacts}
    return render(request, 'base/index.html', context)

@login_required(login_url='login')
def addContact (request) :
    if request.method == 'POST' :
        contactUser = User.objects.get(pk=request.POST['userID'])
        new_contact = Contact(
            currentUser = request.user,
            userID = contactUser
        )
        new_contact.save()
        return redirect('/contact-list/')
    return render(request, 'base/new.html')

@login_required(login_url='login')
def contactProfile (request, pk) :
    contact = Contact.objects.get(id = pk)

    smallID = contact.userID.id
    bigID = contact.currentUser.id

    if smallID > bigID :
        tmp = smallID
        smallID = bigID
        bigID = tmp


    roomName = str(smallID) + ' - ' + str(bigID)
    context = {'contact' : contact, "roomName": roomName}
    return render(request, 'base/lobby.html', context)
#

@login_required(login_url='login')
def editContact(request, pk):
    contact = Contact.objects.get(id=pk)
    if request.method == 'POST' :
        contactUser = User.objects.get(pk=request.POST['userID'])
        contact.userID = contactUser
        contact.save()

        return redirect('/profile/'+str(contact.id))
    context = {'contact' : contact}
    return render(request, 'base/edit.html', context)

@login_required(login_url='login')
def deleteContact (request, pk) :
    contact = Contact.objects.get(id=pk)
    if request.method == 'POST' :
        contact.delete()
        return redirect('/contact-list/')
    context = {'contact' : contact}
    return render(request, 'base/delete.html', context)


def getToken (request) :
    appId = '38e3a9c1018e4d6ca9b60f351d15c7c5'
    appCertificate = '630d80cc553845b3b9c5f5b4f882466c'
    # http: // 127.0.0.1: 8000 / get_token /?channel = room1
    # channelName = room1
    channelName = request.GET.get('channel')

    # i need to generate random number for the user
    uid = request.user.id
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

@login_required(login_url='login')
def lobby (request) :
    if not request.user.is_authenticated:
        return render(request, 'base/loginPage.html')
    return render(request, 'base/lobby.html')


@login_required(login_url='login')
def room (request) :
    if not request.user.is_authenticated:
        return render(request, 'base/loginPage.html')
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

