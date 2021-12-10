from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Position, Coin_list, Paper_trading

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id','username']



