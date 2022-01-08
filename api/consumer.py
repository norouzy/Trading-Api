from channels.generic.websocket import AsyncWebsocketConsumer
import json,requests
from asyncio import sleep
import asyncio
from api.models import Watch_list,Wallet, Position,Position_option, Paper_trading
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from urllib.parse import urlparse, parse_qs

User = get_user_model()


class TradeConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        # GETTING DATA FROM URL
        self.user = self.scope['user']
        # parsed_link = urlparse(str(self.scope['query_string'])[2:-1])
        # captured_value = parse_qs(parsed_link.path)
        # print(captured_value)

        # try:
        #     self.coin1 = captured_value["coin"][0]
        #     self.coin2 = captured_value["to"][0]
        # except:
        #     self.coin1 = 'btc'
        #     self.coin2 = 'usdt'

        # GET LAST POSITIONS COUNT FROM URL
        # try:
        #     self.p_count = int(captured_value["p"][0])
        # except:
        #     self.p_count = 10

        self.group_name='tableData'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'main',
                'value': text_data,
            }
        )

    async def main(self, event):

        # GET DATA FROM VAL
        val = json.loads(event['value'])
        coin1 = val['coin1']
        coin2 = val['coin2']
        try:
            last_positions_count = val['lpc']
        except:
            last_positions_count = 10

        # SENDING DATA TO SOCKET
        while True:
            wallet_coin = []
            watchlist_coin = {"coin1": [], "coin2": []}

            
            # get models data
            if self.user.is_authenticated:
                data = {
                    "watchlist": [],
                    "wallet": {
                        "coin": [], "balance": 0
                    },
                    "position": [],
                    "last_positions": [],
                    coin1 + "/" + coin2: 0,
                }

                checked_paper = await self.check_paper_trading()

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

                # SET USER POSITIONS
                for position in positions:
                    position_option = await self.get_position_option(position.id)
                    data = self.position_option(data, position_option, position)

                if not checked_paper:
                    data['position'] = 'Paper trading does not exist'
                    data['wallet'] = 'Paper trading does not exist'
            else:
                data = {
                    "last_positions": [],
                    coin1 + "/" + coin2: 0,
                }

            # GET COIN PRICE
            data[coin1 + "/" + coin2] = self.get_price(coin1, coin2)[coin2.upper()]

            # GET LAST POSITIONS
            last_positions = await self.get_last_positions(last_positions_count, coin1, coin2)

            # SET LAST POSITIONS
            for position in last_positions:
                data = self.set_last_positions(data, position)

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
        results = list(Position.objects.all().filter(paper_trading__user=self.user))
        return results

    @database_sync_to_async
    def get_last_positions(self, count, coin1, coin2):
        results = list(Position.objects.filter(coin1=coin1, coin2=coin2).order_by('-oreder_set_date')[:count])
        return results

    @database_sync_to_async
    def get_position_option(self, id):
        return list(Position_option.objects.all().filter(in_position=id))

    @database_sync_to_async
    def check_paper_trading(self):
        paper = Paper_trading.objects.filter(user=self.user)
        if paper:
            return True
        else:
            return False

    def time_format(self, position):
        return str(position.year)+"-"+str(position.month)+"-"+str(position.day)+" "+str(position.hour)+":"+str(position.minute)

    def get_multi_price_wallet(self, coins):
        coins = ",".join(coins)
        # url = f"https://min-api.cryptocompare.com/data/pricemulti?fsyms={coins}&tsyms=USDT"
        url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={coins}&tsyms=USDT"
        response = requests.get(url)
        response = response.json()
        return response
    
    def get_multi_price_watchlist(self, coins):
        coins1 = ",".join(coins["coin1"])
        coins2 = ",".join(coins["coin2"])
        # url = f"https://min-api.cryptocompare.com/data/pricemulti?fsyms={coins1}&tsyms={coins2}"
        url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={coins1}&tsyms={coins2}"
        response = requests.get(url)
        response = response.json()
        return response

    def get_price(self, coin1, coin2):
        url = f"https://min-api.cryptocompare.com/data/price?fsym={coin1}&tsyms={coin2}"
        response = requests.get(url)
        response = response.json()
        return response

    def balance(self, coins):
        key = list(coins)
        balance_total = 0
        for coin in key:
            balance_total += coins[coin]['USDT']

    def wallet(self, data, wallets, wallet_coin):
        tot_balance = 0
        wallet_coin_price = self.get_multi_price_wallet(wallet_coin)
        for wallet in wallets:
            set_data = {
                "id": wallet.id,
                "coin": wallet.coin,
                "amount": wallet.amount,
                "price": wallet_coin_price["RAW"][(wallet.coin).upper()]['USDT']["PRICE"],
                "1HChange": wallet_coin_price["RAW"][(wallet.coin).upper()]['USDT']["CHANGEPCTHOUR"]
            }
            tot_balance = tot_balance + wallet_coin_price["RAW"][(wallet.coin).upper()]['USDT']["PRICE"] * wallet.amount
            data['wallet']["coin"].append(set_data)
        data['wallet']["balance"] = tot_balance
        return data

    def watchlist(self, data, watchlists, watchlist_coin):
        watchlist_coin_price = self.get_multi_price_watchlist(watchlist_coin)
        for watchlist in watchlists:
            set_data = {
                "id": watchlist.id,
                "coin1": watchlist.coin1,
                "coin2": watchlist.coin2,
                "price": watchlist_coin_price["RAW"][(watchlist.coin1).upper()][(watchlist.coin2).upper()]["PRICE"],
                "1HChange": watchlist_coin_price["RAW"][(watchlist.coin1).upper()][(watchlist.coin2).upper()]["CHANGEPCTHOUR"]
            } 
            data['watchlist'].append(set_data)
        return data

    def position_option(self, data, position_option, position):
        if position_option:
            set_data = {
                "id":position.id,
                "trade_type": position.trade_type,
                "order_type": position.order_type,
                "coin1": position.coin1,
                "coin2": position.coin2,
                "entert_price": position.entert_price,
                "amount": position.amount,
                "status": position.status,
                "oreder_set_date": self.time_format(position.oreder_set_date) if position.oreder_set_date else "",
                "oreder_reach_date": self.time_format(position.oreder_reach_date) if position.oreder_reach_date else "",
                "position_option": {
                        "amount": position_option[0].amount,
                        "status": position_option[0].status,
                        "trade_type": position_option[0].trade_type,
                        "stoploss": position_option[0].stoploss,
                        "take_profit": position_option[0].take_profit,
                        "oreder_reach_date": self.time_format(position_option[0].oreder_reach_date) if position_option[0].oreder_reach_date else "",
                    }
                }
            data["position"].append(set_data)
        else:
            set_data = {
                "id": position.id,
                "trade_type": position.trade_type,
                "order_type": position.order_type,
                "coin1": position.coin1,
                "coin2": position.coin2,
                "entert_price": position.entert_price,
                "amount": position.amount,
                "status": position.status,
                "oreder_set_date": self.time_format(position.oreder_set_date) if position.oreder_set_date else "",
                "oreder_reach_date": self.time_format(position.oreder_reach_date) if position.oreder_reach_date else "",
                }
            data["position"].append(set_data)
        return data

    def set_last_positions(self, data, position):
        set_data = {
            "id": position.id,
            "trade_type": position.trade_type,
            "order_type": position.order_type,
            "coin1": position.coin1,
            "coin2": position.coin2,
            "entert_price": position.entert_price,
            "amount": position.amount,
            "status": position.status,
            "oreder_set_date": self.time_format(position.oreder_set_date) if position.oreder_set_date else "",
            "oreder_reach_date": self.time_format(position.oreder_reach_date) if position.oreder_reach_date else "",
        }
        data["last_positions"].append(set_data)

        return data


class HomePageConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = 'homeData'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'main',
                'value': text_data,
            }
        )

    async def main(self, event):
        val = json.loads(event['value'])

        # LAST POSITIONS COUNT
        try:
            last_positions_count = val['lpc']
        except:
            last_positions_count = 10

        # TOP COINS COUNT
        try:
            top_coins_count = val['tcc']
            if top_coins_count > 100:
                top_coins_count = 100
        except:
            top_coins_count = 50

        # TOP COINS PAGE
        try:
            top_coins_page = val['page']
        except:
            top_coins_page = 0
        while True:
            data = {
                "last_positions": [],
                "top_coins": [],
            }

            # GET LAST POSITIONS
            last_positions = await self.get_last_positions(last_positions_count)

            # GET TOP COINS
            top_coins = self.get_top_coins(top_coins_count, top_coins_page)

            # SET LAST POSITIONS
            for position in last_positions:
                data = self.set_last_positions(data, position)

            # SET TOP COINS
            for coin in top_coins['Data']:
                data = self.set_top_coins(data, coin)

            await self.send(json.dumps(data))
            await sleep(1)

    @database_sync_to_async
    def get_last_positions(self, count):
        results = list(Position.objects.all().order_by('-oreder_set_date')[:count])
        return results

    def get_top_coins(self, top_coins_count, page):
        url = f"https://min-api.cryptocompare.com/data/top/mktcapfull?limit={top_coins_count}&tsym=USD&page={page}"
        response = requests.get(url)
        response = response.json()
        return response

    def set_last_positions(self, data, position):
        set_data = {
            "id": position.id,
            "trade_type": position.trade_type,
            "order_type": position.order_type,
            "coin1": position.coin1,
            "coin2": position.coin2,
            "entert_price": position.entert_price,
            "amount": position.amount,
            "status": position.status,
            "oreder_set_date": TradeConsumer.time_format(data, position.oreder_set_date) if position.oreder_set_date else "",
            "oreder_reach_date": TradeConsumer.time_format(data, position.oreder_reach_date) if position.oreder_reach_date else "",
        }
        data["last_positions"].append(set_data)

        return data

    def set_top_coins(self, data, coin):
        res = coin['RAW']['USD']
        name = res['FROMSYMBOL']
        price = res['PRICE']
        val24h = res['VOLUME24HOUR']
        coinImg = "https://www.cryptocompare.com/"+coin['CoinInfo']['ImageUrl']
        marketCap = res['MKTCAP']
        changePctIn24h = coin['coinInfo']['CHANGEPCT24HOUR']

        set_data = {
            'coin': name,
            'price': price,
            'val24h': val24h,
            'coinImg': coinImg,
            'marketCap': marketCap,
            'changePctIn24h': changePctIn24h,

        }
        data['top_coins'].append(set_data)
        return data

