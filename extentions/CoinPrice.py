import requests
class PriceChecker():
	def check_price(coin1,coin2):
		data = f"https://min-api.cryptocompare.com/data/price?fsym={coin1}&tsyms={coin2}&api_key=f3fd30141d445e2e49a2c3cd84312f2bbd2d67aa508e4dcb2b5ac28201f6b1e7"
		response = requests.get(data)
		response = response.json()
		return response[coin2.upper()]