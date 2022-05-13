import json
from pyexpat.errors import messages
from asgiref.sync import async_to_sync
# декоратор для работы БД в асинхронном режиме
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import datetime
from .models import Messages, Room
from blog.models import UserProfile



class BaseConsumer(AsyncWebsocketConsumer): # уведомления для всех страниц сайта
    async def connect(self):
        self.user_name = self.scope['url_route']['kwargs']['user_name']
        print(self.user_name)
        self.user = self.scope["user"]
        print('self.user', type(self.user), self.user.username)
        await self.accept()
        await self.sendfish()

    async def sendfish(self):
        user_list = {}
        data = await self.get_historical_data()
        for one_message in data:
            if one_message['user'] not in user_list:
                user_info = await self.get_user_info(one_message['user']) 
                user_list[one_message['user']] = user_info
            if self.user.username != user_list[one_message['user']].user.username:
                text_data={
                        'message': one_message['text'],
                        'username': str(user_list[one_message['user']].user.username),
                        'first_name': str(user_list[one_message['user']].user.first_name),
                        'last_name': str(user_list[one_message['user']].user.last_name),
                        # 'time': str(one_message['created_at'])
                        }
                await self.send(json.dumps(text_data))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # self.user = text_data_json.get('user', None)
        # print(self.user)

    @database_sync_to_async   
    def get_historical_data(self):
        d = list(Messages.objects.order_by('created_at').values('text', 'user', str('created_at')))
        print(d)
        return d

    @database_sync_to_async  
    def get_user_info(self, id_user):
        user_info = UserProfile.objects.get(user_id=id_user)
        print(user_info)
        return user_info


# асинхронное
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print('self.room_name =', self.room_name)
        print('self.room_group_name =', self.room_group_name)
        # Добавление в чат
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # пользователь, который подлючился по вебсокету
        self.user = self.scope["user"]
        print('Пользователь ', self.user)
        print('async_to_sync self.room_group_name, self.channel_name =', self.room_group_name, ', ',  self.channel_name)
        
        await self.accept()  # подлючение пользователя к группе
         # блок отправки истории
        data = await self.get_historical_data()
       
        user_list = {}
        for one_message in data:
            if one_message['user'] not in user_list:
                user_info = await self.get_user_info(one_message['user']) 
                user_list[one_message['user']] = user_info
            
            text_data={
                    'message': one_message['text'],
                    'username': str(user_list[one_message['user']].user.username),
                    'first_name': str(user_list[one_message['user']].user.first_name),
                    'last_name': str(user_list[one_message['user']].user.last_name),
                    'time': str(one_message['created_at']),
                    'scan': str(one_message['is_scanned'])
                    }
            # if self.user != 
            # self.message_id = one_message['id']    
            # await self.scanned_messages()
            await self.send(json.dumps(text_data))
        

    async def disconnect(self, close_code):
        # отключение пользователя от группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # получение сообщения благодаря Websocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        first_name = text_data_json['first_name']
        last_name = text_data_json['last_name']
        time = text_data_json['time']

        await self.new_message(message=message)  # сохранения истории в БД
        print('receive=', text_data_json)

        # Отправка сообщения в группу
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',  # указываем какая функция отбрабатывает отправку сообщения
                'message': message,
                'first_name': first_name,
                'last_name': last_name,
                'time': time,  # время из фронтенда
            })

    # получение сообщения из группы
    async def chat_message(self, event):
        message = event['message']
        first_name = event['first_name']
        last_name = event['last_name']
        time = event['time']
        print('chat_message=', message, ' Длина сообщения = ', len(message))
        # Отправка сообщения в Websocket
        if len(message) != 0:
            await self.send(text_data=json.dumps({
                'message': message,
                'first_name': first_name,
                'last_name': last_name,
                'time': str(datetime.datetime.now()),
            }))

    @database_sync_to_async     # декоратор для работы БД в асинхронном режиме
    def new_message(self, message):
        if len(message) != 0:
            Messages.objects.create(text=message, user=self.user,
                                    room = Room.objects.get(name=self.room_name))

    @database_sync_to_async   
    def get_historical_data(self):
        d = list(Messages.objects.filter(room=Room.objects.get(name=self.room_name)).order_by('created_at').values('id', 'text', 'user', str('created_at'), str('is_scanned')))
        print(d)
        return d
    
    @database_sync_to_async
    def scanned_messages(self):     # отмечаем сообещние просмотренным
        scan = Messages.objects.get(pk=self.message_id)
        scan.is_scanned = True 
        scan.save()

    @database_sync_to_async  
    def get_user_info(self, id_user):
        user_info = UserProfile.objects.get(user_id=id_user)
        print(user_info)
        return user_info     


class LikesConsumer(AsyncWebsocketConsumer):  #лайки чата
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        
        await self.accept()
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        likes = text_data_json.get('likes', None)
        dislikes = text_data_json.get('dislikes', None)
        if likes:
            await self.new_like()
        if dislikes:
            await self.new_dislike()
        
    @database_sync_to_async
    def new_like(self):
        room_instance = Room.objects.get(name=self.room_name)
        room_instance.likes += 1 
        room_instance.save()
        message_instance = Messages.objects.filter(room=Room.objects.get(name=self.room_name)).order_by('-created_at')[0]
        print(message_instance)
        message_instance.likes = True 
        message_instance.save()
    
    
    @database_sync_to_async
    def new_dislike(self):
        room_instance = Room.objects.get(name=self.room_name)
        room_instance.dislikes += 1 
        room_instance.save()
        message_instance = Messages.objects.filter(room=Room.objects.get(name=self.room_name)).order_by('-created_at')[0]
        print(message_instance)
        message_instance.likes = False 
        message_instance.save()


# синхронное соединение
# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
#         print('self.room_name =', self.room_name)
#         print('self.room_group_name =', self.room_group_name)
#         # Добавление в чат
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#         self.user = self.scope["user"]  #пользователь, который подлючился по вебсокету
#         print('self.user', self.user)
#         print('async_to_sync self.room_group_name, self.channel_name =', self.room_group_name, ', ',  self.channel_name)

#         self.accept() #подлючение пользователя к группе

#     def disconnect(self, close_code):
#         # отключение пользователя от группы
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     # получение сообщения благодаря Websocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         first_name = text_data_json['first_name']
#         last_name = text_data_json['last_name']
#         time = text_data_json['time']
#         self.new_message(message=message)       #сохранения истории в БД
#         print('receive=', text_data_json)

#         # Отправка сообщения в группу
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message', #указываем какая функция отбрабатывает отправку сообщения
#                 'message': message,
#                 'first_name': first_name,
#                 'last_name': last_name,
#                 'time': time, #время из фронтенда
#             }
#         )

#     # получение сообщения из группы
#     def chat_message(self, event):
#         message = event['message']
#         first_name = event['first_name']
#         last_name = event['last_name']
#         time = event['time']
#         print('chat_message=', message, ' Длина сообщения = ', len(message))
#         # Отправка сообщения в Websocket
#         if len(message) != 0:
#             self.send(text_data=json.dumps({
#                 'message': message,
#                 'first_name': first_name,
#                 'last_name': last_name,
#                 'time': str(datetime.datetime.now()),
#             }))


#     def new_message(self, message):
#         Messages.objects.create(text=message, user=self.user)
