from django.db import models

from django.contrib.auth.models import User


# Create your models here.

class RoomMember (models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=200)
    room_name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



# 1 - create Database Model (RoomMember) | Store username, uid and room name
# 2 - on join, create RoomMember in database
# 3 - on handleUserJoin event, query database for room member name by uid
# 4 - on leave, delete room member

