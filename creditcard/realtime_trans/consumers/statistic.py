import json
from asyncio import sleep
import datetime
from ..models import Creditcard
from django.db.models import Avg
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class StatisticConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_data(self):
        try:
            class0_count = Creditcard.objects.filter(class_field=0).count()
            if class0_count == None:
                class0_count = 0
        except:
            class0_count = 0
        try:
            class1_count = Creditcard.objects.filter(class_field=1).count()
            if class1_count == None:
                class1_count = 0
        except:
            class1_count = 0
        try:
            class0_avg = Creditcard.objects.filter(class_field=0).aggregate(avg=Avg('amount'))['avg']
            if class0_avg == None:
                class0_avg = 0
        except:
            class0_avg = 0
        try:
            class1_avg = Creditcard.objects.filter(class_field=1).aggregate(avg=Avg('amount'))['avg']
            if class1_avg == None:
                class1_avg = 0
        except:
            class1_avg = 0
        try:
            class0_recentId = Creditcard.objects.filter(class_field=0).last().id
        except:
            class0_recentId = ''
        try:
            class1_recentId = Creditcard.objects.filter(class_field=1).last().id
        except:
            class1_recentId = ''
        try:
            class0_recentTime = Creditcard.objects.filter(class_field=0).last().time
        except:
            class0_recentTime = ''
        try:
            class1_recentTime = Creditcard.objects.filter(class_field=1).last().time
        except:
            class1_recentTime = ''
        data = {
            'class0_count': class0_count,
            'class1_count': class1_count,
            'class0_avg': round(class0_avg,2),
            'class1_avg': round(class1_avg,2),
            'class0_recent': {'id':class0_recentId, 'time':class0_recentTime},
            'class1_recent': {'id':class1_recentId, 'time':class1_recentTime}
        }
        return data
    
    async def connect(self):
        await self.accept()
        while True:
            data = await self.get_data()
            await self.send(json.dumps(data))
            await sleep(5)