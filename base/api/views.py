from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status,filters
from rest_framework.permissions import IsAuthenticated

# we will overwrite on these build in functions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

from .serializers import UserSerializer,RegisterSerializer,LogoutSerializer




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add username in token payload
        token['username'] = user.username

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer





@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer=RegisterSerializer(data=request.data)
        # check if data is valid
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        refresh = RefreshToken.for_user(user)
        data=serializer.data
        print(refresh)
        return Response( {
            "data":str(data),
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })
        #return Response(serializer.data,refresh,status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    if request.method == 'POST':
        serializer=LogoutSerializer(data=request.data)
        # check if data is valid
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]

    return Response(routes)