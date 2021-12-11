from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView

from .serializers import *
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework import viewsets

from django.contrib.auth import get_user_model
from .permissions import IsSuperUser, IsUser, UserPosition, UserPapertrading
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


class PositionStatusUpdate(RetrieveUpdateDestroyAPIView):
	serializer_class = PositionUpdateSerializer
	permission_classes = (UserPosition,)
	def get_queryset(self):
		user = self.request.user
		query = Position.objects.filter(paper_trading__user=user)
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


class PapertradingViewSet(viewsets.ModelViewSet):
	# queryset = Paper_trading.objects.all()
	serializer_class = PaperTradingSerializer
	permission_classes = (UserPapertrading,)
	def get_queryset(self):
		user = self.request.user
		query = Paper_trading.objects.filter(user=user)
		return query
	def perform_create(self, serializer):
		user = self.request.user
		serializer.save(user=user)

class PapertradingListView(ListCreateAPIView):
	serializer_class = PaperTradingSerializer
	permission_classes = (IsUser,)
	def get_queryset(self):
		user = self.request.user
		query = Paper_trading.objects.filter(user=user)
		return query
	def perform_create(self, serializer):
		user = self.request.user
		serializer.save(user=user)

class PapertradingDetail(RetrieveUpdateDestroyAPIView):
	serializer_class = PaperTradingSerializer
	permission_classes = (UserPapertrading,)
	def get_queryset(self):
		user = self.request.user
		query = Paper_trading.objects.filter(user=user)
		return query