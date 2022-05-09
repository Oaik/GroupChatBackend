"""
Doc string for module

"""

from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Friend_list,FriendRequest



class FriendlistSerializer(serializers.ModelSerializer):
    class Meta:
        model=Friend_list
        fields=['users1']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','first_name','last_name','username')



class FriendrequestSerializer(serializers.ModelSerializer):
    sender=UserSerializer()
    class Meta:
        model=FriendRequest
        fields=('id','sender','receiver')

