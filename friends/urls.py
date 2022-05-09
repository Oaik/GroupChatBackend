from django.urls import path
from .views import send_friend_request,accept_friend_request,get_myfriends,get_my_friend_requests,cancel_friend_request,remove_friend,decline_friend_request


urlpatterns = [
    # for make friend request --> taking the id of the other user
    path('add/<int:pk>/',send_friend_request),
    # for cancel friend request as sender --> taking the id of the user you want to cancel your request
    path('cancel_request/<int:pk>/',cancel_friend_request),
    # accept the friend request as receiver --> by taking the (id) of the other user
    path('accept/<int:pk>/',accept_friend_request),
    # decline the friend request as receiver --> by taking the (id) of the other user
    path('decline/<int:pk>/',decline_friend_request),
    # list all user friends
    path('list/',get_myfriends),
    # get all user friends requests that he received
    path('get_my_requests/',get_my_friend_requests),
    # to unfriend user
    path('unfriend/<int:pk>/',remove_friend),



]