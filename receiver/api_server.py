import threading
import time
import service
import json

from flask import Flask, request, render_template                                    
from flask_restful import Resource, Api, reqparse, inputs                           

# Flask & Flask-RESTful instance variables
app = Flask(__name__) # Core Flask app.                                              
api = Api(app) # Flask-RESTful extension wrapper                                    


service_thread = service.ServiceThread()
service_thread.start()
bbs=service_thread.get_params()            
msgs_input_dic=service_thread.get_input_msgs()   
msgs_output_dic=service_thread.get_output_msgs()  

def save_bbs(bbs):

        
        with open('code_new.py', 'w') as outputFile:
            for listitem in line_list[0:line_bbs[1]-2]:
                outputFile.write('%s' % listitem)

            for num_line,listitem in enumerate(line_list[line_bbs[1]-2:line_bbs[-1]]):

                result = listitem .find('msgm')                
                params=listitem[0:result].split('{')[1].split(',')
                line=''
                left_line=listitem[result:]



                for num,param in enumerate(params[:-1]):
                    key=param.split(':')[0].replace(" ","")
                    value=param.split(':')[1].replace(" ","")
                    
                    if value[1:-1] !='null':
                        if num==0:
                            block_name=key[1:-1]
                            key=key[1:-1]
                            key_name=key
                        else:
                            key_name=key[1:-1]
                            key=block_name+'_'+key[1:-1]

                        print('key',key)
                        line+="'"+key_name+"':'"+bbs[key]+"',"
                    
                    else:
                        line+="'"+key[1:-1]+"':'null',"
                    

                line+="'"+left_line  

                new_line='        self.bbs.block('+str(num_line)+",'"+block_name+"',{"+line 
                outputFile.write('%s' % new_line)                


            for listitem in line_list[line_bbs[-1]:-1]:
                outputFile.write('%s' % listitem)


def read_bbs(bbs): #change list to dictionary, all bbs params in one dict
    
    bbs_dic={}
    bbs_name=[]
    for bb in bbs:
        param_dic=bbs[bb]
        for num,key in enumerate(param_dic):
            
            if num==0:
                name=bb
                bbs_dic[name]=param_dic[key]
                bbs_name.append(name)
            else:
                if param_dic[key]!='null' and key!='msgc' and key !='msgm':
                    bb_name=name+'_'+key  #change name to block_param 
                    bbs_dic[bb_name]=param_dic[key]


    #print(bbs_dic)         
    return bbs_dic,bbs_name           

bbs_dic,bbs_name=read_bbs(bbs)


def write_bbs(bbs,bbs_name):
    
    new_bbs_param_dict={}
    new_bbs_param={}    
    num=0

    for key in bbs: #{'Generator_0': 'ramp', 'Generator_0_name': 'Werner', 'Generator_1': 'ramp', 'Generator_1_name': 'cdcd'}
        
        if key in bbs_name:
            block=key

            if num==0:
                new_bbs_param={} 
                first_key=key.split('_')[0] #remove the number of bb '_', 
 
                first_key=first_key[0].lower()+first_key[1:]
                new_bbs_param[first_key]=bbs[key]   
                num=1
            else:    
                new_bbs_param_dict[key]=new_bbs_param
                first_key=key.split('_')[0]
                first_key=first_key[0].lower()+first_key[1:]
                new_bbs_param={} 
                new_bbs_param[first_key]=bbs[key] 

        else:
            new_key=key.replace(block+'_','') #change block_param to param
            new_bbs_param[new_key]=bbs[key]

 
        new_bbs_param_dict[block]=new_bbs_param # example {'Generator_0': {'Generator': 'ramp', 'name': 'Werner'}, 'Generator_1': {'Generator': 'ramp', 'name': 'cdcd'}}


    print('new_bbs_param',new_bbs_param_dict) 

    return new_bbs_param_dict

#msgs=json.loads(service_thread.get_msgs())
#bbs_dic.update(service_thread.get_msgs())

# @app.route applies to the core Flask instance (app).
# Here we are serving a simple web page.
@app.route('/', methods=['GET'])                                                     # (8)
def index():
    """Make sure inde.html is in the templates folder
    relative to this Python file."""
    return render_template('index_api_client.html',bbs=bbs_dic,msgi=msgs_input_dic,msgo=msgs_output_dic,cond={'condition':'on'} )                # (9)


# Flask-restful resource definitions.
# A 'resource' is modeled as a Python Class.
class Params(Resource):  # (10)

    def __init__(self):
        self.bbs=bbs_dic

    def get(self):
    
        return self.bbs  # (13) change it show blocks


    def post(self):

        #only set params !!!!
        json_data = request.get_json(force=True)
        #json_data = request.get_json()

        print('json_data',json_data)

        for key in json_data:
            self.bbs[key]= str(json_data[key])    


        service_thread.set_params(write_bbs(self.bbs,bbs_name))
        service_thread.set_control('run')
        
        return self.bbs                                                             

class Control(Resource):  # (10)

    def __init__(self):
        self.condition='on'

    def get(self):
        #only initial        
        return {'condition':self.condition} 


    def post(self):


        json_data = request.get_json(force=True)
        print('json_control',json_data)
        service_thread.set_control(json_data['control'])

        #close API
        if json_data['control']=='close':
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()

            print('API closed!')
  
        return {'condition':json_data['control']}   

# Register Flask-RESTful resource and mount to server end point /led
api.add_resource(Params, '/params')   
api.add_resource(Control, '/control')     

class Topic(Resource):
    def __init__(self):
        pass

    def get(self):
        msg_json=service_thread.com.msg_topic
        msg_dict=json.loads(msg_json)
        data={}
        for item in msg_dict:
            data[item]=msg_dict[item]
        
        if len(msg_dict)>0:
            return data
        else:
            {'x':'x'}

api.add_resource(Topic, '/topic')
import socket
if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address=s.getsockname()[0]
    s.close()
    app.run(host=ip_address, port=5001,debug=False)
