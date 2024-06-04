from django.urls import path

from .consumers import CreditcardConsumer

ws_urlpatterns = [
    path('ws/realtime_trans/', CreditcardConsumer.as_asgi())
]