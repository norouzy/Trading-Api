from api.models import Wallet

class ValidateWalletCoin():
	def check(coin,amount,user):
		try :
			wallet_coin = Wallet.objects.filter(paper_trading__user__id=user,coin=coin)
			wallet_coin = wallet_coin[0]
			print(wallet_coin.coin)
			if wallet_coin:
				if wallet_coin.amount >= abs(amount):
					return True
				else:
					return "not enough coin"
			else:
				return "coin not found"
		except:
			return "some thing went wrong"