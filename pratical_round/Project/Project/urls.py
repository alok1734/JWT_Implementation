"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url , include
from django.contrib import admin
from rest_framework import routers
from App.views import UserRegistrationViewset , LoginAPI, UserProfile
from rest_framework_simplejwt import views as jwt_views

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

router = routers.SimpleRouter()
router.register(r'users', UserRegistrationViewset)
router.register(r'login', LoginAPI, basename='login')
router.register(r'userprofile', UserProfile, basename='userprofile')
urlpatterns = router.urls
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^registration/', include(router.urls)),
   	url(r'^auth-jwt/', obtain_jwt_token),
    url(r'^auth-jwt-refresh/', refresh_jwt_token),
    url(r'^auth-jwt-verify/', verify_jwt_token),
]


