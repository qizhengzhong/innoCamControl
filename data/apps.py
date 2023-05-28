from django.apps import AppConfig
from threading import Thread

from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time

from receiver.communication import *
from receiver.codes import *


import sqlite3

from networkx.readwrite import json_graph
import networkx as nx

class TestThread(Thread):


    def run(self):

        print('Thread running')

        com=Communication()
        code=Code()
        code.init()

        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()

        while True:

            if com.update_topic==True:
                com.update_topic= False
                code.input_topic(com.msg_topic)
                code.impl0()

                print('receiver_msg',code.topic_msg1)



                
                #c.execute('''SELECT number FROM data_data''')
                #conn.commit()
                #number_list = [int(list(i)[0]) for i in c.fetchall()]

                

                    
                #num=max(number_list)+1
                #print('number exists',num)

                #num=str(num)
                #week='2016'+'-'+str(3)+'-'+str(3)
                #sku=str(33)
                #weekly_sales=str(33)
                #EV='white'
                #color='red'
                #price=str(33)
                #vendor=str(33)
                #function='car'
           
                #sql = ''' INSERT INTO data_data(number,week,sku,weekly_sales,EV,color,price,vendor,functionality)
                #             VALUES('''+'"'+num+'"'+''','''+'"'+week+'"'+''','''+sku+''','''+weekly_sales+''','''+'"' +EV+'"'+''','''+'"'+color+'"'+''','''+price+''','''+vendor+''','''+'"'+function+'"'+''') '''

                #c.execute(sql)
                #conn.commit()
                

                now = timezone.now()
                channel_layer = get_channel_layer()


                async_to_sync(channel_layer.group_send)('chat_1', 

                    {
                        'type': 'chat_message',
                        'message': code.topic_msg1,#[num,week,sku,weekly_sales,EV,color,price,vendor,function],#code.topic_msg1,
                        'user': 'Alex',
                        'datetime': now.isoformat(),
                    }
                )
                
                time.sleep(2)
            ##############
            
            now = timezone.now()
            channel_layer = get_channel_layer()


            for i in range(1,101,20):
                for j in range(1,101,20):
                    msg=[i,j]





                    G = eval('nx.circular_ladder_graph('+str(i)+')')

                    # Convert non-serializable parts of the graph to serializable formats
                    G_serializable = nx.DiGraph(G)  # Convert the graph to a serializable format (e.g., DiGraph)
            
                    #request.session['GENERATED_GRAPH'] = json_graph.node_link_data(G_serializable)
            
                    data = json_graph.node_link_data(G_serializable)
            


                    async_to_sync(channel_layer.group_send)('chat_1', 

                        {
                            'type': 'chat_message',
                            'message': msg,#[num,week,sku,weekly_sales,EV,color,price,vendor,function],#code.topic_msg1,
                            'data': data,
                            'datetime': now.isoformat(),
                        }
                    )
                    #print('send!',msg)
                    time.sleep(2)    
                

class DataConfig(AppConfig):
    name = 'data'

    def ready(self):

        TestThread().start()
        #pass

