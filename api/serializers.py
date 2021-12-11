from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

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

class PositionUpdateSerializer(serializers.ModelSerializer):
	status = serializers.ReadOnlyField(source='c')
	class Meta:
		model = Position
		fields = ['status',]

class PositionAddSerializer(serializers.ModelSerializer):
	paper_trading = serializers.ReadOnlyField(source='paper_trading.id')
	class Meta:
		model = Position
		fields = "__all__"

class PositionOptionSerializer(serializers.ModelSerializer):
	in_position = serializers.ReadOnlyField(source='in_position.id')
	trade_type = serializers.ReadOnlyField(source='w')
	oreder_reach_date = serializers.ReadOnlyField(source='')
	class Meta:
		model = Position_option
		fields ="__all__"
