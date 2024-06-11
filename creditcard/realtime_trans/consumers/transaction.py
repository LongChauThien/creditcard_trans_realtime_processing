import json
from asyncio import sleep
import datetime
from ..models import Creditcard
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import time

class CreditcardConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.id = None
        self.time = None
        self.amount = None
        self.class_field = None

    @database_sync_to_async
    def get_creditcard(self):
        record = Creditcard.objects.last()
        if record is None:
            return None, False
        has_changed = False
        if self.id==None or record.id != self.id:
            has_changed = True
            self.id = record.id
            self.time = record.time
            self.amount = record.amount
            self.class_field = record.class_field
            current_refresh_time = 'Current Refresh Time: {date:%Y-%m-%d %H:%M:%S}'.format(date=datetime.datetime.now())
            data = {
                'id': self.id,
                'time': self.time,
                'amount': self.amount,
                'class_field': self.class_field,
                'current_refresh_time': current_refresh_time
            }
            # print(data)
            return data, has_changed
        return None, has_changed
        # time = []
        # amount = []
        # class_field = []
        # for trans in querryset:
        #     time.append(trans.time)
        #     amount.append(trans.amount)
        #     class_field.append(trans.class_field)
        # current_refresh_time = 'Current Refresh Time: {date:%Y-%m-%d %H:%M:%S}'.format(date=datetime.datetime.now())
        # data = {
        #     'time': time,
        #     'amount': amount,
        #     'class_field': class_field,
        #     'current_refresh_time': current_refresh_time
        # }
        # print(data)
        # return data
    async def connect(self):
        await self.accept()
        while True:
            data, has_changed = await self.get_creditcard()
            if has_changed:
                # start = time.time()
                await self.send(json.dumps(data))
                # end = time.time()
                # print('Time taken to send: ', end-start)