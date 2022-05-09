from django.shortcuts import render

from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status,filters
from .serializers import FriendlistSerializer,UserSerializer,FriendrequestSerializer
from .models import FriendRequest,Friend_list
from django.contrib.auth.models import User

# Create your views here.


# route to make friend request
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request, pk):
    sender = request.user
    recipient = User.objects.get(id=pk)
    model = FriendRequest.objects.get_or_create(sender=request.user, receiver=recipient)
    msg={"message":"you send a friend request successfully"}
    return Response(msg)



# cancel friend request
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancel_friend_request(request, pk):
    other_user = User.objects.get(id=pk)
    print(other_user)
    msg=""
    model1 = FriendRequest.objects.get(sender=request.user, receiver=other_user)
    model1.delete()
    msg="you cancel the friend request successfully"
    return Response(msg)


# accept friend request
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, pk):
    new_friend = User.objects.get(id=pk)
    msg="message"
    fq = FriendRequest.objects.get(sender=new_friend, receiver=request.user)
    Friend_list.make_friend(request.user, new_friend)
    Friend_list.make_friend(new_friend, request.user)
    fq.delete()
    msg ="you have a new friend in your friend list"
    return Response(msg)


# decline the friend request
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decline_friend_request(request, pk):
    new_friend = User.objects.get(id=pk)
    msg="message"
    fq = FriendRequest.objects.get(sender=new_friend, receiver=request.user)
    msg ="you decline a friend request successfully"
    fq.delete()
    return Response(msg)


# unfriend user
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_friend(request, pk):
    msg=""
    try:
        removee = User.objects.get(id=pk)
        friend_list = Friend_list.objects.get(current_user=request.user)
        friend_list.lose_friend(request.user,removee)
        msg="you remove a friend from your list successfully"
    except Exception as e:
        msg = f"Something went wrong: {str(e)}"
    return Response(msg)



# list all my friend
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_myfriends(request):
    f=Friend_list.objects.get(current_user=request.user).users1.all()
    serializer=UserSerializer(f,many=True)
    return Response(serializer.data)



# route to get the friend request that I recieved
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_friend_requests(request):
    r=FriendRequest.objects.filter(receiver=request.user)
    serializer=FriendrequestSerializer(r,many=True)
    return Response(serializer.data)