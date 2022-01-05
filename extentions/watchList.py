from api.models import Watch_list
from .checkCoin import Coinlist
class WatchList_checker():
	def check(coin1,coin2,user):
		if not Coinlist.check(coin1) and not Coinlist.check(coin2) \
		or not Coinlist.check(coin1) and Coinlist.check(coin2) \
		or Coinlist.check(coin1) and not Coinlist.check(coin2) \
		or coin1==coin2:
			return False      
		data = Watch_list.objects.filter(coin1=coin1,coin2=coin2,user=user)
		data = data.first()
		if data ==None:
			Watch_list.objects.create(coin1=coin1,coin2=coin2,user=user)
			return True
		else:
			return False
