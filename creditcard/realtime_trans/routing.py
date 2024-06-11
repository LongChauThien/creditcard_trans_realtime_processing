from django.urls import path

from .consumers.transaction import CreditcardConsumer
from .consumers.chart import ChartConsumer
from .consumers.statistic import StatisticConsumer

ws_urlpatterns = [
    path('ws/realtime_trans/', CreditcardConsumer.as_asgi()),
    path('ws/realtime_chart/', ChartConsumer.as_asgi()),
    path('ws/realtime_statistic/', StatisticConsumer.as_asgi())
]