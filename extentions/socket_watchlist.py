from api.models import Watch_list
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
import asyncio
class WatchList_socket():
	@database_sync_to_async
	def check(self):
		print("jo")
		print(user)
		data = Watch_list.objects.filter(user=self.user)
		print(*data)

		return data