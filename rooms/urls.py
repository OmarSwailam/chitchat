from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rooms/<str:rooms_type>', views.rooms, name='rooms'),
    path('create-room', views.create_room, name='create_room'),
    path('join/<pk>', views.join_room, name='join_room'),
    path('room/<pk>', views.room, name='room'),
]
