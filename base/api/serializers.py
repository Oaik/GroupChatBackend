from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import RefreshToken,TokenError

# Register serializer



class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(min_length=6,write_only=True)

    class Meta:
        model = User
        # the fields yhat I want to send to front-end
        fields = ('username','password','first_name','last_name','id')
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # **validated_data --> to take all data from the fields
        return user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }
    # when I called serializer.is_valid()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs


    # when I called serializer.save()
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')



# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']