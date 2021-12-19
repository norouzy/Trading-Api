import requests
class PriceChecker():
	def check_price(coin1,coin2):
		data = f"https://min-api.cryptocompare.com/data/price?fsym={coin1}&tsyms={coin2}"
		response = requests.get(data)
		response = response.json()
		return response[coin2.upper()]