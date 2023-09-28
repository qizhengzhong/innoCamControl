import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone


import sqlite3
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('connect')
        #self.user = self.scope['user']
        #self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = 'chat_1'
        # join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # accept connection
        await self.accept()

    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()

        print('message',message)

        #write to database

        cursor.execute('''SELECT number FROM data_data''')
        conn.commit()
        number_list = [int(list(i)[0]) for i in cursor.fetchall()]


        num=1

        if num in number_list:
            print('number exists')
            num=max(number_list)+1

        num=str(num)
        week='2017'+'-'+str(3)+'-'+str(3)
        sku=str(33)
        weekly_sales=str(33)
        EV='white'
        color='red'
        price=str(33)
        vendor=str(33)
        function='car'

        sql = ''' INSERT INTO data_data(number,week,sku,weekly_sales,EV,color,price,vendor,functionality)
                     VALUES('''+'"'+num+'"'+''','''+'"'+week+'"'+''','''+sku+''','''+weekly_sales+''','''+'"' +EV+'"'+''','''+'"'+color+'"'+''','''+price+''','''+vendor+''','''+'"'+function+'"'+''') '''

        cursor.execute(sql)
        print(cursor.fetchall())
        conn.commit()

        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': [num,week,sku,weekly_sales,EV,color,price,vendor,function],
                'user': 'Alex',
                'datetime': now.isoformat(),
            }
        )

    # receive message from room group
    async def chat_message(self, event):
        # send message to WebSocket
        await self.send(text_data=json.dumps(event))
