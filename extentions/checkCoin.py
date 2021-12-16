from api.models import Coin_list

class Coinlist():
	def check(coin):
		coin = Coin_list.objects.filter(coin=coin)
		if not coin.first()==None:
			return True
		else:
			return False
