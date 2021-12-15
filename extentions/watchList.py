from api.models import Watch_list

class WatchList_checker():
	def check(coin1,coin2,user):
		data = Watch_list.objects.filter(coin1=coin1,coin2=coin2,user=user)
		data = data.first()
		if data ==None:
			Watch_list.objects.create(coin1=coin1,coin2=coin2,user=user)
			return True
		else:
			return False