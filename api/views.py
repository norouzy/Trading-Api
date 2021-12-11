from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .serializers import *
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from django.contrib.auth import get_user_model
from .permissions import IsSuperUser, IsUser, UserPosition, UserPositionOption
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

class PositionOption(ListCreateAPIView):
	queryset = Position_option.objects.all()
	serializer_class = PositionOptionSerializer
	# permission_classes = (UserPositionOption,)
	def get_queryset(self):
		user = self.request.user
		id = self.kwargs['pk']
		query = Position_option.objects.filter(in_position=id,in_position__paper_trading__user=user)
		return query
	def perform_create(self, serializer):
		user = self.request.user
		id = self.kwargs['pk']
		
		is_in_position = Position_option.objects.filter(in_position=id)
		if is_in_position:
			return JsonResponse(serializers.errors, status=404)
		else:
			position = Position.objects.filter(id=id)
			position = position.first()

		serializer.save(in_position=position)

