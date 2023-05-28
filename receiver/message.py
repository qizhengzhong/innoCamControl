import sys
sys.path.append('')
import json
class topic_msg:
    def __init__(self):
        self.msg1=0

    def encode(self):
        message={'msg1':self.msg1}
        json_message=json.dumps(message)
        return json_message

    def decode(self,inputs=None):
        if inputs!="": 
            if isinstance(inputs,bytes):
                inputs=inputs.decode()
            json_message=json.loads(inputs)
            self.msg1=json_message['msg1']
