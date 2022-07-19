import requests
import environ,os
environ.Env.read_env()
api_key = os.environ['api_key_price']
class PriceChecker():
	def check_price(coin1,coin2):
		data = f"https://min-api.cryptocompare.com/data/price?fsym={coin1}&tsyms={coin2}&api_key={api_key}"
		response = requests.get(data)
		response = response.json()
		return response[coin2.upper()]