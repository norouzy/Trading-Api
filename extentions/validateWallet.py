from api.models import Wallet

class ValidateWalletCoin():
	def check(coin,amount,user):
		# try :
		wallet_coin = list(Wallet.objects.all().filter(paper_trading__user__id=user,coin=coin))
		print(wallet_coin)
		if wallet_coin:
			if wallet_coin[0].amount >= abs(amount):
				return True
			else:
				return "not enough coin"
		else:
			return "coin not found in wallet"