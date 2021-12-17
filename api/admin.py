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


class walletAdmin(admin.ModelAdmin):
	list_display = (
		'paper_trading',
		# 'coin',
		# 'amount'
		)
admin.site.register(Wallet, walletAdmin)


class watchListAdmin(admin.ModelAdmin):
	list_display = (
		'user',
		# 'coin1',
		# 'coin2',
		)
admin.site.register(Watch_list, watchListAdmin)


class walletItemAdmin(admin.ModelAdmin):
	list_display = (
		# 'user',
		'wallet',
		'coin',
		'amount'
		)
# <<<<<<< HEAD
admin.site.register(WalletItem, walletItemAdmin)

# =======
# admin.site.register(Wallet,walletAdmin)
# >>>>>>> parent of 5b4ba91... fixed model wallet bugs

admin.site.register(Coin_list)