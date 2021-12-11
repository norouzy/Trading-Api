from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView

from .serializers import PaperTradingSerializer, PositionSerializer, PositionCreateSerializer, PositionAddSerializer, UserSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from django.contrib.auth import get_user_model
from .permissions import IsSuperUser, IsUser, UserPosition
from .models import Position

from rest_framework.response import Response


User = get_user_model()

class UserList(ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (IsSuperUser,)


class UserDetail(RetrieveUpdateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (IsUser,)


class PositionList(ListAPIView):
	serializer_class = PositionSerializer
	permission_classes = (IsUser,)
	def get_queryset(self):
		user = self.request.user
		query = Position.objects.filter(paper_trading__user=user)
		return query


class PositionDetail(RetrieveUpdateDestroyAPIView):
	serializer_class = PositionCreateSerializer
	permission_classes = (UserPosition,)
	def get_queryset(self):

		query = Position.objects.all()
		return query

class PositionCreate(CreateAPIView):
	serializer_class = PositionAddSerializer
	def perform_create(self, serializer):
		user = self.request.user
		paper = user.paper_trading
		serializer.save(paper_trading=paper)


class PositionTotal(ListAPIView):
	queryset = Position.objects.all()
	serializer_class = PositionSerializer
	permission_classes = (IsSuperUser,)
