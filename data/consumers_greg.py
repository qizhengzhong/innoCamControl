from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
import requests

wrapper_group_name = "wrapper_in"

class StateUpdateConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(wrapper_group_name,self.channel_name)
        await self.accept()

    async def disconnect(self,close_code):
        pass
    
    async def receive_json(self,content):
        print(f"Websocket got:{content}")
        tag = content.get('tag',None)
        content = content.get('content',None)
        if tag is not None and content is not None:
            print("sending on channel layer")
            await self.channel_layer.send(
                    "wrapper_out",
                    {
                        'topic':tag,
                        'content':content,
                    }
                )
    
    async def wrapper_in(self,event): # change topic to mqtt topic
        await self.mqtt_update(event)

    async def mqtt_update(self,event):
        message = json.loads(event['message'])
        print("CONSUMER GOT", message)
        if message['state'] == 'entered' or message['state'] == 'changed':
            ws_message = message
            await self.send_json(
                    {
                        "tag":"state-update",
                        "content":ws_message,
                        },
                    )

