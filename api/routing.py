from django.urls import path, re_path
from .consumers import *

ws_urlpatterns = [
    # path('ws/rooms/', RoomsSocket.as_asgi()),
    path('ws/rooms/', RoomSocket.as_asgi()),
    path('ws/books/', BookSocket.as_asgi()),
    path('ws/room/<str:room_name>/', RoomItemSocket.as_asgi()),
    path('ws/cook/<str:room_name>/', CookSocket.as_asgi()),
]
