from api.models import Watch_list
class WatchList_checker():
	def check(user):
		data = Watch_list.objects.filter(user__id="8")
		return data