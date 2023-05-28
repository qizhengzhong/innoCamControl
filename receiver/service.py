from communication import *
from codes import *
import time
import threading

class ServiceThread(threading.Thread):
    def __init__(self):
        self.com=Communication() 
        self.code=Code() 
        self.code.init() 
        self.pre_topic={} 
        self.control='on'
        self.lock = threading.RLock()
        super(ServiceThread, self).__init__()

    def run(self):
        while True:
            if self.control=='on':
                self.run_body()
            elif self.control=='run':# once
                self.run_body()
                self.control='stop'
            elif self.control=='off':# close
                break
        self.code.close()
        print('service1_service1_DataStorageandManagement service closed!')

    def run_body(self):

        if self.com.update_topic==True:
            self.com.update_topic= False
            self.code.input_topic(self.com.msg_topic)

            self.code.impl0()

        if self.code.is_stop()==True:
            self.control='off'

    def set_params(self, params):
        #with self.lock:
        self.code.set_parameters(params)

    def get_params(self):
        return self.code.get_parameters()

    def get_input_msgs(self):
        return self.code.get_input_msgs()

    def get_output_msgs(self):
        return self.code.get_output_msgs()

    def set_control(self,condition):
        self.control=condition

if __name__ == "__main__":
    service1= ServiceThread()
    service1.run()
