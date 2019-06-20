# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserRegistrationSerializer
from .models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
import urllib2
from rest_framework.decorators import (
    api_view,
    detail_route,
    list_route,
    renderer_classes,
    authentication_classes,
    permission_classes)

from rest_framework.response import Response


from django.contrib.auth import authenticate, login
import requests, json

class UserRegistrationViewset(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

class LoginAPI(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    def create(self, request):
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            data = {"email" : email, "password" : password}
            url = "http://127.0.0.1:8000/auth-jwt/"
            req = requests.post(url,data=data)
            return Response(json.loads(req.content))
        else:
            return Response("Unauthorized",status = HTTP_401_UNAUTHORIZED)
        

class UserProfile(viewsets.ViewSet):
    def list(self, request):
        print "request.user", request.user
        queryset = User.objects.all()
        serializer = UserRegistrationSerializer(queryset, many=True)
        return Response(serializer.data)
        