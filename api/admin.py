#.........
from django.contrib.auth.models import User
from django.contrib import admin
from .models import *
# Register your models here.

class positonAdmin(admin.ModelAdmin):
	list_display = (
		'position_name',
		'trade_type',
		'status',
		'amount',
		'oreder_set_date',
		'oreder_reach_date',
		'entert_price',
		)
admin.site.register(Position,positonAdmin)

class positon_optionAdmin(admin.ModelAdmin):
	list_display = (
		'position_name',
		'trade_type',
		'status',
		'amount',
		'oreder_reach_date',
		'stoploss',
		'take_profit',
		)
admin.site.register(Position_option,positon_optionAdmin)

class paper_tradingAdmin(admin.ModelAdmin):
	list_display = (
		'user',
		'balance',
		'enter_balance',
		'enter_date'
		)
admin.site.register(Paper_trading,paper_tradingAdmin)
admin.site.register(Coin_list)




