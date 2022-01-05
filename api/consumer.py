from channels.generic.websocket import AsyncWebsocketConsumer
import json,requests
from asyncio import sleep
from extentions.socket_watchlist import WatchList_socket
import asyncio
from api.models import Watch_list,Wallet, Position,Position_option
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
User = get_user_model()
class TradeConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        self.user = self.scope['user']
        self.group_name='tableData'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self,close_code):
        pass

    async def receive(self,text_data):
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type':'main',
                'value':text_data,
            }
        )

    async def main(self,event):
        val = json.loads(event['value'])
        coin1 = val['coin1']
        coin2 = val['coin2']
        while True:
            wallet_coin = []
            watchlist_coin = {"coin1":[],"coin2":[]}
            data = {
                "watchlist":[],
                "wallet":{
                    "coin":[],"balance":0
                },
                "position":[],
                coin1+"/"+coin2:0,
            }
            
            # get models data
            positions = await self.get_position()
            watchlists = await self.get_watchlist()
            wallets = await self.get_wallet()

            # get coin name and save it in array to get multi price
            for wallet in wallets:
                wallet_coin.append(wallet.coin)
            for watchlist in watchlists:
                watchlist_coin["coin1"].append(watchlist.coin1)
                watchlist_coin["coin2"].append(watchlist.coin2)
            

            # add data to json 
            data = self.wallet(data, wallets, wallet_coin)
            data = self.watchlist(data, watchlists, watchlist_coin)

            data[coin1+"/"+coin2] = self.get_price(coin1,coin2)[coin2.upper()]
            
            for position in positions:
                position_option = await self.get_position_option(position.id)
                data = self.position_option(data,position_option,position)
                
            
            await self.send(json.dumps(data))
            await sleep(1)


    @database_sync_to_async
    def get_watchlist(self):
        return list(Watch_list.objects.all().filter(user=self.user))

    @database_sync_to_async
    def get_wallet(self):
        return list(Wallet.objects.all().filter(paper_trading__user=self.user))


    @database_sync_to_async
    def get_position(self):
        results =  list(Position.objects.all().filter(paper_trading__user=self.user))
        return results

    @database_sync_to_async
    def get_position_option(self,id):
        return list(Position_option.objects.all().filter(in_position=id))
    
    def time_format(self,position):
        return str(position.year)+"-"+str(position.month)+"-"+str(position.day)+" "+str(position.hour)+":"+str(position.minute)

    def get_multi_price_wallet(self,coins):
        coins = ",".join(coins)
        url = f"https://min-api.cryptocompare.com/data/pricemulti?fsyms={coins}&tsyms=USDT"
        response = requests.get(url)
        response = response.json()
        return response
    
    def get_multi_price_watchlist(self,coins):
        coins1 = ",".join(coins["coin1"])
        coins2 = ",".join(coins["coin2"])
        url = f"https://min-api.cryptocompare.com/data/pricemulti?fsyms={coins1}&tsyms={coins2}"
        response = requests.get(url)
        response = response.json()
        return response

    def get_price(self,coin1,coin2):
        url = f"https://min-api.cryptocompare.com/data/price?fsym={coin1}&tsyms={coin2}"
        response = requests.get(url)
        response = response.json()
        return response

    def balance(self,coins):
        key = list(coins)
        balance_total = 0
        for coin in key:
            balance_total+=coins[coin]['USDT']

    def wallet(self,data,wallets,wallet_coin):
        tot_balance = 0
        wallet_coin_price = self.get_multi_price_wallet(wallet_coin)
        for wallet in wallets:
            set_data = {
                "id":wallet.id,
                "coin":wallet.coin,
                "amount":wallet.amount,
                "price":wallet_coin_price[(wallet.coin).upper()]['USDT']
            }
            tot_balance = tot_balance + wallet_coin_price[(wallet.coin).upper()]['USDT'] * wallet.amount
            data['wallet']["coin"].append(set_data)
        data['wallet']["balance"]=tot_balance
        return data

    def watchlist(self,data,watchlists,watchlist_coin):
        watchlist_coin_price = self.get_multi_price_watchlist(watchlist_coin)
        for watchlist in watchlists:
            set_data = {
                "id":watchlist.id,
                "coin1":watchlist.coin1,
                "coin2":watchlist.coin2,
                "price": watchlist_coin_price[(watchlist.coin1).upper()][(watchlist.coin2).upper()]
            } 
            data['watchlist'].append(set_data)
        return data

    def position_option(self,data,position_option,position):
        if position_option:
            set_data = {
                "id":position.id,
                "trade_type":position.trade_type,
                "order_type":position.order_type,
                "coin1":position.coin1,
                "coin2": position.coin2,
                "entert_price":position.entert_price,
                "amount":position.amount,
                "status": position.status,
                "oreder_set_date":self.time_format(position.oreder_set_date) if position.oreder_set_date else "",
                "oreder_reach_date":self.time_format(position.oreder_reach_date) if position.oreder_reach_date else "",
                "position_option":{
                        "amount":position_option[0].amount,
                        "status":position_option[0].status,
                        "trade_type":position_option[0].trade_type,
                        "stoploss":position_option[0].stoploss,
                        "take_profit":position_option[0].take_profit,
                        "oreder_reach_date": self.time_format(position_option[0].oreder_reach_date) if position_option[0].oreder_reach_date else "",
                    }
                }
            data["position"].append(set_data)
        else:
            set_data = {
                "id":position.id,
                "trade_type":position.trade_type,
                "order_type":position.order_type,
                "coin1":position.coin1,
                "coin2": position.coin2,
                "entert_price":position.entert_price,
                "amount":position.amount,
                "status": position.status,
                "oreder_set_date":self.time_format(position.oreder_set_date) if position.oreder_set_date else "",
                "oreder_reach_date":self.time_format(position.oreder_reach_date) if position.oreder_reach_date else "",
                }
            data["position"].append(set_data)
        return data
