from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone

class Paper_trading(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="paper_trading", verbose_name="paper trading", blank=True)
	enter_balance = models.FloatField()
	balance = models.FloatField()
	enter_date = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return str(self.user)

class Coin_list(models.Model):
	coin = models.CharField(max_length=20)
	def __str__(self):
		return self.coin

class Position(models.Model):

	TRADE_TYPE_CHOISES = (
			("b","Buy"),
			("s","Sell"),
		)
	STATUS_CHOICES = (
			("w","Working"),
			("d","Done"),
			("c","close"),
		)


	paper_trading = models.ForeignKey(Paper_trading, on_delete=models.CASCADE, related_name="position", verbose_name="paper_trading")
	trade_type = models.CharField(max_length=1, choices=TRADE_TYPE_CHOISES, verbose_name="type")
	amount = models.FloatField(verbose_name="token amount")
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="trade status")
	entert_price = models.FloatField()
	oreder_set_date = models.DateTimeField(auto_now_add=True)
	oreder_reach_date = models.DateTimeField(blank=True, null=True)
	coin1 = models.ForeignKey(Coin_list,models.CASCADE, related_name="coin1")
	coin2 = models.ForeignKey(Coin_list,models.CASCADE, related_name="coin2")
	
	def position_name(self):
		return str(self.user)+"/"+str(self.coin1)+str(self.coin2)
	def __str__(self):
		return str(self.user)+"/"+str(self.coin1)+str(self.coin2)

class Position_option(models.Model):
	TRADE_TYPE_CHOISES = (
				("t","Take Profit"),
				("s","Stop loss"),
				("w","Working"),
			)
	
	STATUS_CHOICES = (
			("p","Pending"),
			("w","Working"),
			("d","Done"),
			("c","close"),
		)

	in_position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="in_position", verbose_name="in_position")
	amount = models.FloatField(verbose_name="token amount")
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="trade status")
	oreder_reach_date = models.DateTimeField(default=timezone.now,blank=True)
	stoploss = models.FloatField(blank=True, null=True)
	take_profit  = models.FloatField(blank=True, null=True)
	status = models.CharField(max_length=1, choices=TRADE_TYPE_CHOISES, verbose_name="trade status")

	
	def position_name(self):
		return str(self.in_position.user)+"/"+str(self.in_position.coin1)+str(self.in_position.coin2)

class Close_info(models.Model):
	position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="close_date_position", verbose_name="position", blank=True)
	date = models.DateTimeField(auto_now_add=True)
	close_price = models.FloatField()
	def close_info_name(self):
		return str(self.position.user)+"/"+str(self.position.coin1)+str(self.position.coin2)