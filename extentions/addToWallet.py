from api.models import WalletItem

class WalletManagment():
	def check(coin, amount, user, wallet):
		try:
			obj = WalletItem.objects.get(coin=coin, wallet__paper_trading__user=user)
			obj.amount += amount
			obj.save()
		except:
			obj = WalletItem.objects.create(wallet=wallet, coin=coin, amount=amount)
			obj.save()

		return obj
