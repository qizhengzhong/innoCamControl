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

class DataConfig(AppConfig):
    name = 'data'

    def ready(self):

        TestThread().start()
        #pass

