from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'city', 'email')

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get('password', None))
        return User.objects.create(**validated_data)
    

        
 