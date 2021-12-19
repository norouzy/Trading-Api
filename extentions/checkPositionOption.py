from api.models import Position, Position_option
import requests
import calendar, time
from .addToWallet import WalletManagment
from .UpdatePositionOption import UpdatePositionOption
class Position_option_checker():
	def requestPrice(coin1,coin2):
		data = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={coin1}&tsym={coin2}&limit=1"
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
			position_option = Position_option.objects.filter(in_position=position,status="w")
			key = list(myDic)
			if position_option:
				positionPair = position.coin1+"/"+position.coin2
				if not positionPair in key:
					myDic[positionPair]=[position.id]
				else:
					myDic[positionPair].append(position.id)
		return myDic
	
	def check_price(coin1,coin2):
		data = f"https://min-api.cryptocompare.com/data/price?fsym={coin1}&tsyms={coin2}"
		response = requests.get(data)
		response = response.json()
		return response[coin2.upper()]
	
	def position_option_update_status(status,pos,closeType):
		Position_option.objects.filter(in_position=pos).update(status=status,trade_type=closeType)
		return True

	def position_option_process(pos,trade_type,position_option):
		try :
			result =Position_option_checker.position_option_update_status("c", pos,trade_type)
			# result = True
		except:
			result = ""
		if result:
			try :
				coin2_amount =position_option.amount * Position_option_checker.check_price(pos.coin1, pos.coin2)
				add_result1 = WalletManagment.check(pos.coin2, coin2_amount, pos.paper_trading)
			except:
				add_result1 = ""
			if not add_result1 :
				Position_option_checker.position_option_update_status("w", pos,trade_type)

	def proccess_to_add_and_delete(key,myDic,positions):
		for coins in key:
			coinarray = coins.split("/")
			coin1 = coinarray[0]
			coin2 = coinarray[1]
			prices=Position_option_checker.requestPrice(coin1,coin2)
			for coin in myDic[coins]:
				for pos in positions:
					if coin == pos.id:
						timestamp = Position_option_checker.timeToTimeStamp(pos)
						timeDifference = prices["time1"] - timestamp
						if timeDifference >= 0 or True:
							position_option = Position_option.objects.filter(in_position=pos)
							position_option=position_option[0]
							if position_option.take_profit>= prices["min"] and position_option.take_profit<=prices["max"]:
								Position_option_checker.position_option_process(pos, "t",position_option)
							elif position_option.stoploss>= prices["min"] and position_option.stoploss<=prices["max"]:
								Position_option_checker.position_option_process(pos, "s",position_option)
									
										
											

	def check():
		positions = Position.objects.filter(order_type="l")

		myDic = Position_option_checker.makeKeyDic(positions)
		print(myDic)
		
		key = list(myDic)
		Position_option_checker.proccess_to_add_and_delete(key,myDic,positions)
		


							

