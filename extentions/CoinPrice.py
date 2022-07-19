import requests
api_key = "a39ee3e464409f1fd796dc0dac0901575522a2bf02ef989f018ed978baebba02"
class PriceChecker():
	def check_price(coin1,coin2):
		data = f"https://min-api.cryptocompare.com/data/price?fsym={coin1}&tsyms={coin2}&api_key={api_key}"
		response = requests.get(data)
		response = response.json()
		return response[coin2.upper()]