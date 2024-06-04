import json
from asyncio import sleep
from .models import Creditcard
import datetime

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class CreditcardConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_creditcard(self):
        querryset = Creditcard.objects.all().order_by('-time')[:10]
        time = []
        amount = []
        class_field = []
        for trans in querryset:
            time.append(trans.time)
            amount.append(trans.amount)
            class_field.append(trans.class_field)
        current_refresh_time = 'Current Refresh Time: {date:%Y-%m-%d %H:%M:%S}'.format(date=datetime.datetime.now())
        data = {
            'time': time,
            'amount': amount,
            'class_field': class_field,
            'current_refresh_time': current_refresh_time
        }
        print(data)
        return data
    async def connect(self):
        await self.accept()

        while True:
            data = await self.get_creditcard()
            await self.send(json.dumps(data))
            await sleep(5)