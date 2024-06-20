import json
from asyncio import sleep
import datetime
from ..models import Creditcard
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChartConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def get_data(self):
        records = Creditcard.objects.order_by('-id')[:100]
        dataClass0 = []
        dataClass1 = []
        for record in records:
            if record:
                if record.class_field == 0:
                    dataClass0.append({
                        'x': record.time,
                        'y': record.amount
                    })
                else:
                    dataClass1.append({
                        'x': record.time,
                        'y': record.amount
                    })
        data = {
                'datasets': [
                    {
                        'label': 'Class 0',
                        'data': dataClass0,
                        'backgroundColor': 'rgba(54, 162, 235, 0.7)',
                        'borderColor': 'rgba(54, 162, 235, 1)'
                        
                    },
                    {
                        'label': 'Class 1',
                        'data': dataClass1,
                        'backgroundColor': 'rgba(255, 99, 132, 0.7)',
                        'borderColor': 'rgba(255, 99, 132, 1)'
                    }
                ]
            }
        # print(dataClass0)
        # print(dataClass1)
        return data
    

    async def connect(self):
        await self.accept()
        while True:
            data = await self.get_data()
            await self.send(json.dumps(data))
            await sleep(5)