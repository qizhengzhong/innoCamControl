#Author:Zhengyang Ling
#Email:zl461@cam.ac.uk

import sys
sys.path.append('')

from .. baseblock.code_base_class import Blockbase,Args,checkArgsType

import numpy as np


class SignalImpy():
    def __init__(self):
     
        self.blocks=['generator',
                     'receiver',
                     'process',
                     'calibration'
                     
                     ]

    class Receiver(Blockbase):
        def __init__(self):

            Blockbase.__init__(self,set_color='3')

            self.name='receiver' #block name 
            self.fun=['receiver']
            self.args=[]

            self.msg_in=['int/float/string']
            self.msg_out=['none']

        def init(self,args=None):  
            self.args_dict=args
            self.args_input=checkArgsType(self.args,args) 
            args=self.args_input   

        def impl(self,data=None):

            print('receiver',data)

            return ['data',data]



