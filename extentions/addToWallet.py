from api.models import Wallet,Paper_trading

class WalletManagment():
	def check(coin,amount,user):
		
		paper_trading =  Paper_trading.objects.get(user=user)
		
		data = Wallet.objects.filter(coin=coin,paper_trading__id=paper_trading.id)
		data = data.first()
		if not data ==None:
			value = data.amount + amount
			results = Wallet.objects.get(id=data.id)
			if value <= 0:
				results.delete()
			else :
				results.amount = value
				results.save()
			return True
		else:
			if not amount <= 0:
				value = amount
				Wallet.objects.create(coin=coin,amount=value,paper_trading=paper_trading)
			else:
				return "amount coin cant be zero or under zero";
			