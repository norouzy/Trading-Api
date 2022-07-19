from api.models import Position, Position_option
import requests
import calendar, time
from .addToWallet import WalletManagment
from .UpdatePositionOption import UpdatePositionOption
import datetime
import environ,os
environ.Env.read_env()
api_key = os.environ['api_key_price']
# api_key = "a39ee3e464409f1fd796dc0dac0901575522a2bf02ef989f018ed978baebba02"
class Position_checker():
	def requestPrice(coin1,coin2):
		data = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={coin1}&tsym={coin2}&limit=1&api_key={api_key}"
		response = requests.get(data)
		response = response.json()
		times = []
		if response['Response'] == "Success":
			context = response['Data']['Data']
			for time in context:
				times.append(time['high'])
				times.append(time['low'])
		time1 = context[0]['time']
		time2 = context[1]['time']
		return {"max":max(times),"min":min(times),"time1":time1,"time2":time2}

	def timeToTimeStamp(pos):
		myTime = str(pos.oreder_set_date.year)+" "+str(pos.oreder_set_date.month)+" "+str(pos.oreder_set_date.day)+" "+str(pos.oreder_set_date.hour)+" "+str(pos.oreder_set_date.minute)
		
		timestamp = calendar.timegm(time.strptime((myTime), '%Y %m %d %H %M'))
		return timestamp

	def makeKeyDic(positions):
		myDic={}
		for position in positions:
			if position.status == "w":

				key = list(myDic)
				positionPair = position.coin1+"/"+position.coin2
				if not positionPair in key:
					myDic[positionPair]=[position.id]
				else:
					myDic[positionPair].append(position.id)
		return myDic
	
	def check_price(coin1,coin2):
		data = f"https://min-api.cryptocompare.com/data/price?fsym={coin1}&tsyms={coin2}&api_key={api_key}"
		response = requests.get(data)
		response = response.json()
		return response[coin2.upper()]
	
	def position_update_status(typeTrade,pos):
		achive_position=Position.objects.get(id=pos.id)
		achive_position.status = typeTrade
		achive_position.save()
		return True

	def position_oreder_reach_date_update(status,pos):
		achive_position=Position.objects.get(id=pos.id)
		if status =="ok":
			achive_position.oreder_reach_date = datetime.datetime.now()
		else:
			achive_position.oreder_reach_date = ""
		achive_position.save()
		return True

	def proccess_to_add_and_delete(key,myDic,positions):
		for coins in key:
			coinarray = coins.split("/")
			coin1 = coinarray[0]
			coin2 = coinarray[1]
			prices=Position_checker.requestPrice(coin1,coin2)
			print(prices)
			print(coins)
			print(positions)
			print(myDic)
			for coin in myDic[coins]:
				for pos in positions:
					print(coin)
					print(pos.id)
					if coin == pos.id:
						timestamp = Position_checker.timeToTimeStamp(pos)

						timeDifference = prices["time1"] - timestamp
						print(timeDifference)
						if timeDifference >= 0:
							print(prices)
							if pos.entert_price>= prices["min"] and pos.entert_price<=prices["max"]:
								if pos.trade_type =="b":
									try :
										result =Position_checker.position_update_status("d", pos)
									except:
										result = ""
									if result:
										try :
											update_order_date=Position_checker.position_oreder_reach_date_update("ok",pos)
											coin1_amount =pos.amount / pos.entert_price
											add_result = WalletManagment.check(pos.coin1, coin1_amount, pos.paper_trading)
										except:
											add_result = ""
											update_order_date = ""
										if add_result :
											
											try:
												is_positionOption = Position_option.objects.get(in_position__id = pos.id)
											except:
												print("no position option")
												is_positionOption=""

											if is_positionOption:
												UpdatePositionOption.check(pos,"w")
												WalletManagment.check(pos.coin1, is_positionOption.amount*-1, pos.paper_trading)
										else:
											Position_checker.position_update_status("w", pos)
											Position_checker.position_oreder_reach_date_update("back",pos)
								elif pos.trade_type == "s":
									try :
										result =Position_checker.position_update_status("d", pos)
										# result = True
									except:
										result = ""
									if result:
										try :
											coin1_amount =pos.amount * pos.entert_price
											add_result = WalletManagment.check(pos.coin1, coin1_amount, pos.paper_trading)
										except:
											add_result = ""
											print(add_result)
										if not add_result :
											print("hi")
											Position_checker.position_update_status("w", pos)
					else:
						print("else")
						print(coin)
						print(pos.id)
								
																		

	def check():
		positions = Position.objects.filter(order_type="l",status="w")
		myDic = Position_checker.makeKeyDic(positions)
		key = list(myDic)
		Position_checker.proccess_to_add_and_delete(key,myDic,positions)
		


							

