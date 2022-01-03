from channels.generic.websocket import AsyncWebsocketConsumer
import json,requests
from asyncio import sleep
from extentions.socket_watchlist import WatchList_socket


class TableData(AsyncWebsocketConsumer):

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
                'type':'randomFunction',
                'value':text_data,
            }
        )

    async def randomFunction(self,event):
        val = json.loads(event['value'])
        coin1 = val['coin1']
        coin2 = val['coin2']
        url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={coin1}&tsym={coin2}&limit=1"
        while True:
            watchlist = WatchList_socket.check(self.user)
            print(watchlist)
            response = requests.get(url)
            response = response.json()
            context = response['Data']['Data']
            res = context[1]['close']
            await self.send(json.dumps({'value': res}))
            await sleep(1)
        await self.send(event['value'])



