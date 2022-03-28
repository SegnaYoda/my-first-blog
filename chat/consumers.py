import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print('self.room_name =', self.room_name)
        print('self.room_group_name =', self.room_group_name)
        # Добавление в чат
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print('async_to_sync self.channel_name =', self.channel_name)

        self.accept()

    def disconnect(self, close_code):
        # Покинуть чат
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # получение сообщения благодаря Websocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print('receive=', message)

        # Отправка сообщения в группу
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # получение сообщения из группы
    def chat_message(self, event):
        message = event['message']
        print('chat_message=', message)
        # Отправка сообщения в Websocket
        self.send(text_data=json.dumps({
            'message': message
        }))