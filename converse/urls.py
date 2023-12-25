from django.urls import path
from . import views


urlpatterns = [
    path('',views.chat,name='chat'),
    path('lobby/',views.lobby,name='lobby'),
    path('create-message/',views.create_message,name='create-message'),
    path('stream-chat-messages/',views.stream_chat_messages,name='stream-chat-messages'),
]
