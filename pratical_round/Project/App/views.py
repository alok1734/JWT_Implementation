# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserRegistrationSerializer
from .models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
import urllib2
from rest_framework import status


from rest_framework.decorators import (
    api_view,
    detail_route,
    list_route,
    renderer_classes,
    authentication_classes,
    permission_classes)

from rest_framework.response import Response

from rest_framework_jwt.settings import api_settings


from django.contrib.auth import authenticate, login
import requests, json
 
import jwt,json
from rest_framework import views
from rest_framework.response import Response
from models import User
from django.contrib.auth import get_user_model
######################################################################
# Please read out this link about refresh token it is claiming,
#that refreshing token is there not refresh token
#https://github.com/tymondesigns/jwt-auth/issues/1105
######################################################################
## Main Point of this link 

# Man this is so confusing. 
#The JWT specification doesn't even include the concept of a refresh token,
# yet many resources talk about it as if its part of JWT. 
#Apparently refreshing tokens is a custom job, 
#and can be done in many ways.
# I came to this package assuming there exist "refresh tokens", 
#but couldn't find it after digging and digging through the source code, and documentation (although small).
# My suggestion is to add a "refresh tokens" page to the wiki explaining that there are no refresh tokens, and that the refreshing is done using the original access token.

###########################################################################
# TASK 1 - For Registration
# Api is used for the registration of the User's.
# Since the api's is used for the registration , 
# I don't think we need to provide any permission for this particular api
# So, I gave AllowAny permission for this or we can not mention permission class. 
###############################################################
class UserRegistrationViewset(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    def create(self, request):

        email = request.data.get('email', "")
        password = request.data.get('password', "")

        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
        my_user = get_user_model()
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        try : 
            my_user = authenticate(email = email, password = password , request = request)

            if my_user is not None:            
                payload = jwt_payload_handler(my_user)
                token = jwt_encode_handler(payload)
                data = {'token':token}
                return Response(data)
        except Exception as e:
            return Response({"Something went wrong": e},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message":"First go for the registration"},status = status.HTTP_401_UNAUTHORIZED)

    def list(self, request):
        queryset = User.objects.all(    )
        serializer = UserRegistrationSerializer(queryset, many=True)
        return Response(serializer.data)
#############################################################
# Task -2
# This Api is used for the login , Again I don't think so it required Authentication. 
# but if we want to make this JWT authentication to this API , 
# we make an another API which will provide me the token for this API.
# it will return access token in response.
# You can make changes in settings file for JWT expiration for the variable
# JWT_EXPIRATION_DELTA 
####################################################################3 

class LoginAPI(viewsets.ViewSet):
    permission_classes=(AllowAny,)

    def list(self, request):

        my_user = get_user_model()
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        email = request.data.get("email", "")
        password = request.data.get("password", "")
        try : 
            my_user = authenticate(email = email, password = password , request = request)

            if my_user is not None:            
                payload = jwt_payload_handler(my_user)
                token = jwt_encode_handler(payload)
                data = {'token':token}
                return Response(data)
        except Exception as e:
            return Response({"Something went wrong": e},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message":"First go for the registration"},status = status.HTTP_401_UNAUTHORIZED)
########################################################################
#Task -3
#This api is used to display User profile
#JWT Authentication is there for this.
        
#####################################################################
class UserProfile(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, )
    def list(self, request):
        queryset = User.objects.filter(email = request.user.email)
        serializer = UserRegistrationSerializer(queryset, many=True)
        return Response(serializer.data)
        