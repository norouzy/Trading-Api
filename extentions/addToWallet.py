from api.models import Wallet,Paper_trading

class WalletManagment():
	def check(coin,amount,user):
		
		paper_trading =  Paper_trading.objects.get(user=user)
		data = Wallet.objects.filter(coin=coin,paper_trading__id=paper_trading.id)
		data = data.first()
		if not data ==None:
			value = data.amount + amount
			results = Wallet.objects.get(id=data.id)
			results.amount = value
			results.save()
		else:
			value = amount
			Wallet.objects.create(coin=coin,amount=value,paper_trading=paper_trading)
		
			
