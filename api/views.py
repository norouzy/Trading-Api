from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .serializers import *

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response

from .permissions import *

from .models import Position


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


class PositionOption(ListCreateAPIView):
  # queryset = Position_option.objects.all()
	serializer_class = PositionOptionSerializer
	permission_classes = (UserPositionOption,)

	def get_queryset(self):
		user = self.request.user
		id = self.kwargs['pk']
		query = Position_option.objects.filter(in_position=id, in_position__paper_trading__user=user)
		return query

	def perform_create(self, serializer):
		user = self.request.user
		id = self.kwargs['pk']
		position = Position.objects.get(id=id)
		option = Position_option.objects.filter(in_position=position, in_position__paper_trading__user=user)
		if not option:
			serializer.save(in_position=position)
		else:
			raise serializers.ValidationError("You already have a position option")

class PositionOptionViewset(viewsets.ModelViewSet):
	serializer_class = PositionOptionSerializer
	permission_classes = (UserPositionOption,)
	lookup_field = "in_position"
	def get_queryset(self):
		user = self.request.user
		query = Position_option.objects.filter(in_position__paper_trading__user=user)
		return query

	def perform_create(self, serializer):
		user = self.request.user
		serializer.save(in_position__paper_trading__user=user)

class PapertradingViewSet(viewsets.ModelViewSet):
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

		try:
			serializer.save(user=user)
		except IntegrityError:
			raise serializers.ValidationError("You already have a paper account")
		else:
			raise serializers.ValidationError("Something went wrong")


class PapertradingDetail(RetrieveUpdateDestroyAPIView):
	serializer_class = PaperTradingSerializer
	permission_classes = (UserPapertrading,)

	def get_queryset(self):
		user = self.request.user
		query = Paper_trading.objects.filter(user=user)
		return query
