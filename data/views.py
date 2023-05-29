from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import View

from .models import Data
from .forms import DataForm
#from pages.models import Page

from ml.process_data import *
import numpy

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from networkx.readwrite import json_graph
import networkx as nx
import json


###############
from multiAgent.init import *

class DataList(ListView):
    model = Data
    context_object_name = 'all_data'

    def get_context_data(self, **kwargs):
        context = super(DataList, self).get_context_data(**kwargs)
       # context['page_list'] = Page.objects.all()
        return context


class DataView(DetailView):
    model = Data
    context_object_name = 'data'
    
    def get_context_data(self, **kwargs):
        context = super(DataView, self).get_context_data(**kwargs)
       # context['page_list'] = Page.objects.all()
        return context


class DataDeleteView(DeleteView):
    # specify the model you want to use
    model = Data
 
    # specify the fields
    success_url ="/" 


class DataCreate(CreateView):
    model = Data
    fields = ['week','sku','weekly_sales','EV','color','price','vendor','functionality']
    success_url ="/" 

    def form_valid(self, form):
        x1= form.instance.sku
        x1= form.instance.weekly_sales
        x1= form.instance.price
        x1= form.instance.vendor


        return super(DataCreate, self).form_valid(form)

class DataUpdateView(UpdateView):
    model = Data
    fields = ['week','sku','weekly_sales','EV','color','price','vendor','functionality']
    success_url ="/" 

    def form_valid(self, form):
        x1= form.instance.sku
        x1= form.instance.weekly_sales
        x1= form.instance.price
        x1= form.instance.vendor


        return super(DataUpdateView, self).form_valid(form)

#    def post(self, request, **kwargs):
#        request.POST = request.POST.copy()
#        request.POST['some_key'] = 'some_value'
#        return super(DataUpdateView, self).post(request, **kwargs)


class Prediction(View):
    template="data/prediction.html"

    def get(self,request):

        print('I am here')

        queryset = Data.objects.all()
 
        date=[]
        price=[]
        for orders in queryset:
            date.append(str(getattr(orders, 'week')))
            price.append(str(getattr(orders, 'price')))

 
        results,methods=evaluation() 
        raw_list,predict_list,y_train_primer,y_test_primer,y_pred_primer=predict()

        x=raw_list+predict_list
        y_raw=y_train_primer+  [-10] * len(y_test_primer)
        y_pred=[-10] * len(y_train_primer)+y_pred_primer
        y_test=[-10] * len(y_train_primer)+y_test_primer


        context={"page_title":"Prediction",'bar_data':results,'bar_labels':methods,'line_labels':date,'line_data':price,'line0_labels':x,'line1_data':y_raw,'line2_data':y_pred,'line3_data':y_test,'x':x,'y1':y_raw,'y2':y_pred}

        #print('finish')
        return render(request,self.template,context)


class Prescription(View):
    template="data/prescription.html"

    def get(self,request):


        queryset = Data.objects.all()
        date=[]
        price=[]
        for orders in queryset:
            date.append(str(getattr(orders, 'week')))
            price.append(str(getattr(orders, 'price')))


        
        scatter1,scatter2,scatter3,scatter4=read_churn()


        context={"page_title":"XYZ",'scatter1':scatter1,'scatter2':scatter2,'scatter3':scatter3,'scatter4':scatter4}

        return render(request,self.template,context)


class Evaluation(View):
    template="data/evaluation.html"

    def get(self,request):


        queryset = Data.objects.all()
        date=[]
        price=[]
        for orders in queryset:
            date.append(str(getattr(orders, 'week')))
            price.append(str(getattr(orders, 'price')))

        context={"page_title":"Overview",'data':price,'labels':date}

        return render(request,self.template,context)


class GenerateGraphView(View):
    template_name = 'data/agentMonitor.html'  # Replace 'generate_graph.html' with your actual template file

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            print('received!!!')
            print(request.body)
            action = json.loads(request.body.decode('utf-8'))['userAction']

            print(action)
            #G = eval('nx.' + action)
            G= eval('nx.circular_ladder_graph(10)')

    # Convert non-serializable parts of the graph to serializable formats
            G_serializable = nx.DiGraph(G)  # Convert the graph to a serializable format (e.g., DiGraph)
            
            request.session['GENERATED_GRAPH'] = json_graph.node_link_data(G_serializable)
            
            data = json_graph.node_link_data(G_serializable)
            return JsonResponse(data, safe=False)
        except:
            return JsonResponse({'error': 'An error occurred'}, status=500)


class Map(View):
    #template="data/map.html"
    template="data/demo.html"

    def get(self,request):


        #queryset = Data.objects.all()
        #date=[]
        #price=[]
        #for orders in queryset:
        #    date.append(str(getattr(orders, 'week')))
        #    price.append(str(getattr(orders, 'price')))



        machineX,machineY,robotX,robotY,listMachineAgent,listBufferAgent,listRobotAgent,productHistory,environmentModel=setupAgents()

        #robot
        scatter1=[1]
        scatter2=[1]     

        #machine
        G0 = nx.DiGraph()
        state2num={}
        for i, vertice in enumerate(listMachineAgent[0].machineCapabilities.vertices):
            print(vertice.processCompleted.processCompleted)

            state2num[vertice.processCompleted.processCompleted]=i

            G0.add_node(i, name=vertice.processCompleted.processCompleted)

        print(state2num)

        for edge in listMachineAgent[0].machineCapabilities.edges:

            print(edge.parent.processCompleted.processCompleted,'->',edge.activeMethod,'->',edge.child.processCompleted.processCompleted)

            G0.add_edge(state2num[edge.parent.processCompleted.processCompleted], state2num[edge.child.processCompleted.processCompleted], name=edge.activeMethod,arrowstyle='->')
        
     
        #G = eval('nx.circular_ladder_graph(10)')

        data = json_graph.node_link_data(G0)
        data= json.dumps(data)


        #buffer
        print('buffer')
        G1 = nx.DiGraph()
        state2num={}
        for i, vertice in enumerate(listBufferAgent[0].bufferCapabilities.vertices):
            print(vertice.processCompleted.processCompleted)

            state2num[vertice.processCompleted.processCompleted]=i

            G1.add_node(i, name=vertice.processCompleted.processCompleted)

        print(state2num)

        for edge in listBufferAgent[0].bufferCapabilities.edges:

            print(edge.parent.processCompleted.processCompleted,'->',edge.activeMethod,'->',edge.child.processCompleted.processCompleted)

            G1.add_edge(state2num[edge.parent.processCompleted.processCompleted], state2num[edge.child.processCompleted.processCompleted], name=edge.activeMethod,arrowstyle='->')
        
     
        #G = eval('nx.circular_ladder_graph(10)')

        data1= json_graph.node_link_data(G1)
        data1= json.dumps(data1)

        #robot
        print('robot')
        G2 = nx.DiGraph()
        state2num={}
        name_list=[]
        #for i, vertice in enumerate(listRobotAgent[0].robotCapabilities.vertices):
        #    print(vertice.processCompleted.processCompleted)

            #if vertice.processCompleted.processCompleted not in name_list:
        #    state2num[vertice.processCompleted.processCompleted]=i
        #    G2.add_node(i, name=vertice.processCompleted.processCompleted)
            #name_list.append(vertice.processCompleted.processCompleted)

        #use above code , node will be repeated 
        G2.add_node(0, name='pos0')
        G2.add_node(1, name='pos1')
        G2.add_node(2, name='pos2')
        state2num={'pos0': 0, 'pos1': 1, 'pos2': 2}

        print(name_list, state2num)

        for edge in listRobotAgent[0].robotCapabilities.edges:

            print(edge.parent.processCompleted.processCompleted,'->',edge.activeMethod,'->',edge.child.processCompleted.processCompleted)

            print(state2num[edge.parent.processCompleted.processCompleted], state2num[edge.child.processCompleted.processCompleted])
            G2.add_edge(state2num[edge.parent.processCompleted.processCompleted], state2num[edge.child.processCompleted.processCompleted], name=edge.activeMethod,arrowstyle='->')
        
     
        #G = eval('nx.circular_ladder_graph(10)')

        data2= json_graph.node_link_data(G2)
        data2= json.dumps(data2)

        #print('data1',data1)


        print('productHistory')
        G3 = nx.DiGraph()
        #state2num={}
        for i, vertice in enumerate(environmentModel.vertices):
            #print(vertice.processCompleted.processCompleted)
            print(vertice.getProcessCompleted())

            state2num[vertice.getProcessCompleted()]=i

            G3.add_node(i, name=vertice.getProcessCompleted())

        #print(state2num)

        for edge in environmentModel.edges:

            print(edge.parent.getProcessCompleted(),'->',edge.activeMethod,'->',edge.child.getProcessCompleted())

            G3.add_edge(state2num[edge.parent.getProcessCompleted()], state2num[edge.child.getProcessCompleted()], name=edge.activeMethod,arrowstyle='->')
        
     

        data3= json_graph.node_link_data(G3)
        data3= json.dumps(data3)
        


        context={"page_title":"XYZ",'scatter1':scatter1,'scatter2':scatter2,'scatter3':machineX,'scatter4':machineY,'scatter5':robotX,'scatter6':robotY,'graph':data,'graph1':data1,'graph2':data2,'graph3':data3}

        return render(request,self.template,context)


class Chatbot(View):
    # template="data/map.html"
    template = "data/chatbot.html"

    def get(self, request):

        # queryset = Data.objects.all()
        # date=[]
        # price=[]
        # for orders in queryset:
        #    date.append(str(getattr(orders, 'week')))
        #    price.append(str(getattr(orders, 'price')))

        machineX, machineY, robotX, robotY, listMachineAgent, listBufferAgent, listRobotAgent, productHistory, environmentModel = setupAgents()

        # robot
        scatter1 = [1]
        scatter2 = [1]

        # machine
        G0 = nx.DiGraph()
        state2num = {}
        for i, vertice in enumerate(listMachineAgent[0].machineCapabilities.vertices):
            print(vertice.processCompleted.processCompleted)

            state2num[vertice.processCompleted.processCompleted] = i

            G0.add_node(i, name=vertice.processCompleted.processCompleted)

        print(state2num)

        for edge in listMachineAgent[0].machineCapabilities.edges:
            print(edge.parent.processCompleted.processCompleted, '->', edge.activeMethod, '->',
                  edge.child.processCompleted.processCompleted)

            G0.add_edge(state2num[edge.parent.processCompleted.processCompleted],
                        state2num[edge.child.processCompleted.processCompleted], name=edge.activeMethod,
                        arrowstyle='->')

        # G = eval('nx.circular_ladder_graph(10)')

        data = json_graph.node_link_data(G0)
        data = json.dumps(data)

        # buffer
        print('buffer')
        G1 = nx.DiGraph()
        state2num = {}
        for i, vertice in enumerate(listBufferAgent[0].bufferCapabilities.vertices):
            print(vertice.processCompleted.processCompleted)

            state2num[vertice.processCompleted.processCompleted] = i

            G1.add_node(i, name=vertice.processCompleted.processCompleted)

        print(state2num)

        for edge in listBufferAgent[0].bufferCapabilities.edges:
            print(edge.parent.processCompleted.processCompleted, '->', edge.activeMethod, '->',
                  edge.child.processCompleted.processCompleted)

            G1.add_edge(state2num[edge.parent.processCompleted.processCompleted],
                        state2num[edge.child.processCompleted.processCompleted], name=edge.activeMethod,
                        arrowstyle='->')

        # G = eval('nx.circular_ladder_graph(10)')

        data1 = json_graph.node_link_data(G1)
        data1 = json.dumps(data1)

        # robot
        print('robot')
        G2 = nx.DiGraph()
        state2num = {}
        name_list = []
        # for i, vertice in enumerate(listRobotAgent[0].robotCapabilities.vertices):
        #    print(vertice.processCompleted.processCompleted)

        # if vertice.processCompleted.processCompleted not in name_list:
        #    state2num[vertice.processCompleted.processCompleted]=i
        #    G2.add_node(i, name=vertice.processCompleted.processCompleted)
        # name_list.append(vertice.processCompleted.processCompleted)

        # use above code , node will be repeated
        G2.add_node(0, name='pos0')
        G2.add_node(1, name='pos1')
        G2.add_node(2, name='pos2')
        state2num = {'pos0': 0, 'pos1': 1, 'pos2': 2}

        print(name_list, state2num)

        for edge in listRobotAgent[0].robotCapabilities.edges:
            print(edge.parent.processCompleted.processCompleted, '->', edge.activeMethod, '->',
                  edge.child.processCompleted.processCompleted)

            print(state2num[edge.parent.processCompleted.processCompleted],
                  state2num[edge.child.processCompleted.processCompleted])
            G2.add_edge(state2num[edge.parent.processCompleted.processCompleted],
                        state2num[edge.child.processCompleted.processCompleted], name=edge.activeMethod,
                        arrowstyle='->')

        # G = eval('nx.circular_ladder_graph(10)')

        data2 = json_graph.node_link_data(G2)
        data2 = json.dumps(data2)

        # print('data1',data1)

        print('productHistory')
        G3 = nx.DiGraph()
        # state2num={}
        for i, vertice in enumerate(environmentModel.vertices):
            # print(vertice.processCompleted.processCompleted)
            print(vertice.getProcessCompleted())

            state2num[vertice.getProcessCompleted()] = i

            G3.add_node(i, name=vertice.getProcessCompleted())

        # print(state2num)

        for edge in environmentModel.edges:
            print(edge.parent.getProcessCompleted(), '->', edge.activeMethod, '->', edge.child.getProcessCompleted())

            G3.add_edge(state2num[edge.parent.getProcessCompleted()], state2num[edge.child.getProcessCompleted()],
                        name=edge.activeMethod, arrowstyle='->')

        data3 = json_graph.node_link_data(G3)
        data3 = json.dumps(data3)

        context = {"page_title": "XYZ", 'scatter1': scatter1, 'scatter2': scatter2, 'scatter3': machineX,
                   'scatter4': machineY, 'scatter5': robotX, 'scatter6': robotY, 'graph': data, 'graph1': data1,
                   'graph2': data2, 'graph3': data3}

        return render(request, self.template, context)