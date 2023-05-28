#Author:Zhengyang Ling
#Email:zl461@cam.ac.uk
import numpy as np


class Args:
    def __init__(self,tp,name,value,idx=None):
        self.tp= tp
        self.name = name
        self.value=value
        self.idx=idx

def checkArgsType(define,args):
    args_dict={}
    args_name=[]
    for arg in define:
        args_dict[arg.name]=arg.tp
        args_name.append(arg.name)

    for i,arg in enumerate(args):
        if arg in args_name:    
            tp=args_dict[arg]
            if args[arg]!='null':
                if tp=="int" or tp=="double" or tp=="float": 
                    str1=tp+'('+str(args[arg])+')'
                    #print('str1',str1)
                    args[arg]=eval(str1)  

    #print(args)                      
    return args

def bgr2rgb(image):

    if len(image.shape)==3: #color

        array = np.array(image)
        array[:,:,0]=image[:,:,2]
        array[:,:,1]=image[:,:,1]
        array[:,:,2]=image[:,:,0]

        #b,g,r = cv2.split(image)       # get b,g,r
        #image = cv2.merge([r,g,b])     # switch it to rgb

        return array
    else:
        return image    

class Blockbase():
    def __init__(self,set_mutator=0,set_dropdown_pos=[1,0],set_color='1',set_inline=1,statement=None,type_check=0,nextstatement=1,prevstatement=1,set_output=0,set_appendstate=0):

        self.set_mutator=set_mutator
        self.set_dropdown_pos=set_dropdown_pos
        self.set_color=set_color
        self.set_inline=set_inline 
        self.statement=statement 
        self.type_check=type_check
        self.nextstatement=nextstatement
        self.prevstatement=prevstatement
        self.set_output=set_output
        self.set_appendstate=set_appendstate

        self.input=[] #from msg #record message name used in impl
        self.output=[] #to msg
        self.second_input=None #

        self.args_dict={}
  
    def get_args(self):
        return self.args_dict

    def close(self):
        pass    



class Impybase():
    def __init__(self):

        #self.states={}
        self.bbs={}  #{bb_name:bb_class}
        self.id={}   #{id_num:bb_name}
        self.pub_msg={} #dictionary {message_name:data}
        self.cur_data=['data',0]
        self.out_data={} # all blocks output
        self.debug=['allall'] #debug blocks
        self.is_stop=False
        self.debug_data=[] #debug data


    def input_data(self,data):
        self.cur_data[0]='data'
        self.cur_data[1]=data


    def output_data(self):
        return self.cur_data[1]


    def input_service_message(self,msg,data):
    
        self.pub_msg[msg]=data

    def output_service_message(self,msg):

        pub_msg_name=list(self.pub_msg.keys()) #register message name
        if msg in pub_msg_name:      
            return self.pub_msg[msg]

    def get_blocks_parameter(self):

        params={}
        for key in self.bbs:
            params[key]=self.bbs[key].get_args()    

        return params
        
    def set_blocks_parameter(self,param_dict):

        for key in param_dict:
            block=self.bbs[key] 

            old_param_dict=block.get_args() # get old parameters
            new_param_dict=param_dict[key]

            #print('old_param_dict',old_param_dict)
            #print('new_param_dict',new_param_dict)

            for param in  new_param_dict:
                if str(old_param_dict[param]) != str(new_param_dict[param]):
                    block.init(new_param_dict) #compare to the old one , if it is different, then init
                    print(block.name+" was changed!")
                    break


    def block(self,id_num,class_name,args): # initialize blocks, add message name in input and run init()

        
        #creat bbs
        bb_name=list(args.keys())[0]+"_"+str(id_num) #must add '_' for api param set!

        #print('bb_name',bb_name)
        self.bbs[bb_name]=class_name
        self.id[id_num]=bb_name

        block=self.bbs[bb_name]


        #define input and output for bbs
        pub_msg_name=list(self.pub_msg.keys()) #register all message name

        for key in args:

            if key[0:4]=='msgm':
                msg_method=args[key]
             
            if key[0:4]=='msgc':  
                msg_name=args[key]

                #process recv
                if msg_method=='input/output':
                    msg=msg_name.split('/')
                    #if msg[0] in pub_msg_name: #input could form service module
                    block.input.append(msg[0]) 
                    #else:
                    #    print("recv not find")  

                    block.output.append(msg[1])
                    self.pub_msg[msg[1]]=None


                if msg_method=='input':
                    #if msg_name in pub_msg_name:
                    block.input.append(msg_name)
                    #else:
                    #    print("recv not find")

                #publish message
                if msg_method=='output':
                    block.output.append(msg_name)
                    self.pub_msg[msg_name]=None


        #define args without msg 
        new_args={}
        for i,key in enumerate(args):
            if key[0:4]!="msgm" and key[0:4]!="msgc":   
                new_args[key]=args[key]
              
        #try:

        print('new_args',new_args)

        if list(args.keys())[0]=='userFunction':
            block.init(new_args,block.input,block.output) 
        else:
            block.init(new_args) 

        #except Exception as e:
            #print('error',e)
            
    def impl(self,id_num): #add message to impl()

        pub_msg_name=list(self.pub_msg.keys()) #register message name  
        block_name=self.id[id_num]
        block=self.bbs[block_name]

        #process input
        #len(block.input)==0 from previous bb
        #len(block.input)==1 one meassge
        #len(block.input)>1 list message
        if len(block.input)!=0: 

            if len(block.input)==1: 
                msg_name=block.input[0]
                    #initilaize from external message 
                if msg_name in pub_msg_name:
                    self.cur_data[1]=self.pub_msg[msg_name]

            if len(block.input)>1: 
                self.cur_data[1]=[]
                for msg_name in block.input:
                    if msg_name in pub_msg_name:
                        #only use for user define funtion
                        self.cur_data[1].append(self.pub_msg[msg_name])


        #second input might remove 
        if block.second_input !=None:
            if block.second_input in pub_msg_name:
                second_input=self.pub_msg[block.second_input]  

    #try:
        if block.second_input !=None:
            self.cur_data=block.impl(self.cur_data[1],second_input) #return format: ['type',data]                    
        else:
            self.cur_data=block.impl(self.cur_data[1]) #return format: ['type',data]
    #except Exception as e:
        #print('error',e)     

       
        #debug 
        if self.cur_data[0]=='debug':   
            self.debug=[]        
            self.debug.append(self.cur_data[1])

        elif self.cur_data[0]=='stop':
            self.is_stop=True    
        else:    
            # save each block output data ={block_name:[data type:data]}
            if self.cur_data[0]=='img':
                self.out_data[block_name]=self.cur_data.copy() #add copy
            else:
                self.out_data[block_name]=self.cur_data #add copy               



        #process output (inlcude list ['data',msg0,msg1])
        if len(block.output)!=0:
            for i,msg_name in enumerate(block.output):
                self.pub_msg[msg_name]=self.cur_data[i+1]   

    def close(self,id_num): #add message to impl()

        block_name=self.id[id_num]
        block=self.bbs[block_name]
        block.close()


    def get_debug(self):


        #print('self.debug',self.debug)
        #print('self.out_data',self.out_data)
        #print('self.pub_msg',self.pub_msg)

        if "allall" in self.debug:
            #show all images from self.out_data
            for key in self.out_data:
                cur_data=self.out_data[key]

                if cur_data[0]=='img':
                    print('add debug image',key)

                    if isinstance(cur_data[1],list)==False: # current output is image or imeg_list , need to change later 
                        #debug_img=cur_data[1].copy() # copy
                        debug_img=bgr2rgb(cur_data[1])
                        self.debug_data.append([key,debug_img])
                    else:
                        for i,img in enumerate(cur_data[1]):
                        #    #debug_img=img.copy() # copy
                            if i <5:
                                debug_img=bgr2rgb(img)
                                self.debug_data.append([key,debug_img])

        else:
            # according to message name from self.pub_msg
            for img_name in self.debug:
                image=self.pub_msg[img_name]


                if isinstance(image,list)==False: # current output is image or imeg_list , need to change later 
                    #debug_img=cur_data[1].copy() # copy
                    debug_img=bgr2rgb(image)
                    self.debug_data.append([img_name,debug_img])
                else:
                    for i,img in enumerate(image):
                    #    #debug_img=img.copy() # copy
                        if i <5:
                            debug_img=bgr2rgb(img)
                            self.debug_data.append([img_name,debug_img])


        return self.debug_data

    def plot_debug(self):
        #############plot###########
        import matplotlib.pyplot as plt
        
        plt.close("all")
        fig=plt.figure(figsize=(8, 8))

        for i,img in enumerate(self.debug_data):


            fig.add_subplot(3, 3, i+1)

            plt.title(img[0])
            #if len(img[1].shape)==2: #grey
            plt.imshow(img[1],'gray')

            #else:

            #    plt.imshow(img[1])
            

            #name = './image/'+str(i)+'.png'
            #cv2.imwrite(name, img[1])

            #plt.title(titles[i]) plt.xticks([]),plt.yticks([])

        plt.show()
