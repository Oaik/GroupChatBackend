from django.urls import path
from . import views
from .views import MyTokenObtainPairView,register,logout

from rest_framework_simplejwt.views import (
    TokenRefreshView
)


urlpatterns = [
    path('',views.getRoutes),

    path('register/',register),
    # this from the documentation of simple jwt
    path('login/', MyTokenObtainPairView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('logout/',logout)
]