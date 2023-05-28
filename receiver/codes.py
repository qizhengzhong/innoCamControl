from .message import *

import sys
sys.path.append('')
from .blocks.signal_blocks.signal_blocks import SignalImpy
from .blocks.baseblock.code_base_class import Impybase

class Code:
    def __init__(self):
        self.init_msg()
        pass

    def init(self):
        self.bbs=Impybase()
        self.bbs.block(0,SignalImpy.Receiver(),{'receiver': 'receiver', 'msgin': 'int/float/string', 'msgout': 'none', 'msgm0': 'input', 'msgc0': 'msg1'})
        pass

    def impl0(self):
        self.bbs.input_service_message('msg1',self.topic_msg1)

        self.bbs.impl(0)


    def close(self):
        self.bbs.close(0)
        pass
    def input_topic(self,data):
        topic=topic_msg()
        topic.decode(data)
        self.topic_msg1=topic.msg1



    def get_parameters(self):
        return self.bbs.get_blocks_parameter()

    def set_parameters(self,param_list):
        return self.bbs.set_blocks_parameter(param_list)

    def get_input_msgs(self):
        return {'topic':{'msg1':''}}

    def get_output_msgs(self):
        return {}

    def is_stop(self):
        return self.bbs.is_stop


    def init_msg(self):
        self.topic_msg1=0
        pass

    def debug(self):
        self.bbs.get_debug()
        self.bbs.plot_debug()

if __name__ == "__main__":
    code1= Code()
    code1.init()
    code1.impl0()
    code1.debug()
