from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, AutheTokenSerializer

from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from matir_bank.core import response_maker
from datetime import datetime, timedelta

# from django.contrib.auth.models import User


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return response_maker.Ok({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
            })
        return response_maker.Error(serializer.errors) 



class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AutheTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            temp_list=super(LoginAPI, self).post(request, format=None)


            expirate_datetime = datetime.strptime(temp_list.data['expiry'], "%Y-%m-%dT%H:%M:%S.%fZ")
            cur_datetime = datetime.now()

            timedelta = expirate_datetime - cur_datetime
            temp_list.data['expires_in'] = timedelta.seconds

            return response_maker.Ok(temp_list.data)
        
        return response_maker.Error(serializer.errors) 