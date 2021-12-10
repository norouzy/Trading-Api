from django.shortcuts import render
from .serializers import UserSerializer, PositionSerializer, PositionAddSerializer, Paper_tradingSerializer_test
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, ListAPIView, CreateAPIView
from django.contrib.auth.models import User
from .permissions import IsSuperUser, IsUser, UserPosition
from .models import Position, Paper_trading
# Create your views here.

class UserList(ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (IsSuperUser,)

class UserDetail(RetrieveUpdateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (IsUser,)
	
