from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email']


class PaperTradingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Paper_trading
		fields = "__all__"


class PositionSerializer(serializers.ModelSerializer):
	def get_coin1(self, obj):
		return obj.coin1.coin

	def get_coin2(self, obj):
		return obj.coin2.coin
	coin1 = serializers.SerializerMethodField('get_coin1')
	coin2 = serializers.SerializerMethodField('get_coin2')

	class Meta:
		model = Position
		fields = "__all__"

class PositionCreateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Position
		fields = ['status','oreder_reach_date']

class PositionAddSerializer(serializers.ModelSerializer):
	paper_trading = serializers.ReadOnlyField(source='paper_trading.id')
	class Meta:
		model = Position
		fields = "__all__"
