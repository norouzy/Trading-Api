from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView

from .serializers import *
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework import viewsets
from django.contrib.auth.models import User
from .permissions import IsSuperUser, IsUser
from .models import Position, Paper_trading

from rest_framework.response import Response


class UserList(ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (IsSuperUser,)


class UserDetail(RetrieveUpdateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (IsUser,)


class PositionList(ListCreateAPIView):
	serializer_class = PositionSerializer
	def get_queryset(self):
		user = self.request.user
		query = Position.objects.filter(paper_trading__user=user)
		return query


class PositionDetail(RetrieveUpdateDestroyAPIView):
	serializer_class = PositionSerializer
	def get_queryset(self):
		user = self.request.user
		query = Position.objects.filter(paper_trading__user=user)
		return query

class PositionCreate(CreateAPIView):
	serializer_class = PositionAddSerializer
	def get_queryset(self):
		user = self.request.user
		query = Position.objects.filter(paper_trading__user=user)
		return query

	def perform_create(self, serializer):
		user = self.request.user
		paper = user.paper_trading
		serializer.save(paper_trading=paper)
