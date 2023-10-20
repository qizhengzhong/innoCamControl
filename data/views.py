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
import pdb

###############
from multiAgent.init import *

class DataList(ListView):
    model = Data
    context_object_name = 'all_data'

    def get_context_data(self, **kwargs):
        context = super(DataList, self).get_context_data(**kwargs)
        return context


class DataView(DetailView):
    model = Data
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super(DataView, self).get_context_data(**kwargs)
        return context


class DataDeleteView(DeleteView):
    '''suffix of _confirm_delete'''
    # specify the model you want to use
    model = Data
 
    # specify the fields
    success_url ="/"


class DataCreate(CreateView):
    '''suffix of _form'''
    model = Data
    fields = ['number', 'week','sku','weekly_sales','EV','color','price','vendor','functionality']
    success_url ="/"

    def form_valid(self, form):
        x1= form.instance.sku
        x1= form.instance.weekly_sales
        x1= form.instance.price
        x1= form.instance.vendor


        return super(DataCreate, self).form_valid(form)

class DataUpdateView(UpdateView):
    '''suffix of _form'''
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

class CoAgent(View):
    template_name = 'data/coordinator.html'  # Replace 'generate_graph.html' with your actual template file

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
            # G = eval('nx.' + action)
            G = eval('nx.circular_ladder_graph(10)')

            # Convert non-serializable parts of the graph to serializable formats
            G_serializable = nx.DiGraph(G)  # Convert the graph to a serializable format (e.g., DiGraph)

            request.session['GENERATED_GRAPH'] = json_graph.node_link_data(G_serializable)

            data = json_graph.node_link_data(G_serializable)
            return JsonResponse(data, safe=False)
        except:
            return JsonResponse({'error': 'An error occurred'}, status=500)
class Overview(View):
    template_name = 'data/overview.html'  # Replace 'generate_graph.html' with your actual template file

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
            return null

class FloorPlan(View):
    template_name = 'data/floorplan.html'  # Replace 'generate_graph.html' with your actual template file

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return null

class GanntChart(View):
    template_name = 'data/ganntchart.html'  # Replace 'generate_graph.html' with your actual template file

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return null

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
    template="data/resourceagent.html"

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

        print("Hello world")
        #machine
        G0 = nx.DiGraph()
        state2num={}
        for i, vertice in enumerate(listMachineAgent[0].machineCapabilities.vertices):
            print("processCompleted" + vertice.processCompleted.processCompleted)

            state2num[vertice.processCompleted.processCompleted]=i

            G0.add_node(i, name=vertice.processCompleted.processCompleted)

        print("state2num")
        print(state2num)

        for edge in listMachineAgent[0].machineCapabilities.edges:

            print(edge.parent.processCompleted.processCompleted,'->',edge.activeMethod,'->',edge.child.processCompleted.processCompleted)

            G0.add_edge(state2num[edge.parent.processCompleted.processCompleted], state2num[edge.child.processCompleted.processCompleted], name=edge.activeMethod, arrowstyle='->')
        
     
        #G = eval('nx.circular_ladder_graph(10)')

        data = json_graph.node_link_data(G0)
        data= json.dumps(data)

        print(G0)
        print(data)

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
    template = "data/chatbot.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class OntologySim(View):
    template = "data/ontologysim.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class OntologySimKpis(View):
    template = "data/ontologysimkpis.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class OntologyDesign(View):
    template = "data/ontologydesign.html"

    def get(self, request):
        # data3 = "{\"directed\":true,\"multigraph\":false,\"graph\":{},\"nodes\":[{\"name\":\"pos0\",\"id\":0},{\"name\":\"pos1\",\"id\":1},{\"name\":\"pos2\",\"id\":2},{\"name\":\"\",\"id\":3},{\"name\":\"S1\",\"id\":4},{\"name\":\"S2\",\"id\":5},{\"name\":\"\",\"id\":6},{\"name\":\"S1\",\"id\":7},{\"name\":\"S3\",\"id\":8},{\"name\":\"S4\",\"id\":9},{\"name\":\"\",\"id\":10},{\"name\":\"S4\",\"id\":11}],\"links\":[{\"name\":\"move01\",\"arrowstyle\":\"->\",\"source\":0,\"target\":1},{\"name\":\"move02\",\"arrowstyle\":\"->\",\"source\":0,\"target\":2},{\"name\":\"move10\",\"arrowstyle\":\"->\",\"source\":1,\"target\":0},{\"name\":\"move12\",\"arrowstyle\":\"->\",\"source\":1,\"target\":2},{\"name\":\"move20\",\"arrowstyle\":\"->\",\"source\":2,\"target\":0},{\"name\":\"move21\",\"arrowstyle\":\"->\",\"source\":2,\"target\":1},{\"name\":\"Storage1\",\"arrowstyle\":\"->\",\"source\":3,\"target\":3},{\"name\":\"move03\",\"arrowstyle\":\"->\",\"source\":0,\"target\":3},{\"name\":\"move30\",\"arrowstyle\":\"->\",\"source\":3,\"target\":0},{\"name\":\"move34\",\"arrowstyle\":\"->\",\"source\":3,\"target\":4},{\"name\":\"move43\",\"arrowstyle\":\"->\",\"source\":4,\"target\":3},{\"name\":\"move35\",\"arrowstyle\":\"->\",\"source\":3,\"target\":5},{\"name\":\"move53\",\"arrowstyle\":\"->\",\"source\":5,\"target\":3},{\"name\":\"Storage2\",\"arrowstyle\":\"->\",\"source\":6,\"target\":6},{\"name\":\"move16\",\"arrowstyle\":\"->\",\"source\":1,\"target\":6},{\"name\":\"move61\",\"arrowstyle\":\"->\",\"source\":6,\"target\":1},{\"name\":\"move67\",\"arrowstyle\":\"->\",\"source\":6,\"target\":7},{\"name\":\"move76\",\"arrowstyle\":\"->\",\"source\":7,\"target\":6},{\"name\":\"move68\",\"arrowstyle\":\"->\",\"source\":6,\"target\":8},{\"name\":\"move86\",\"arrowstyle\":\"->\",\"source\":8,\"target\":6},{\"name\":\"move69\",\"arrowstyle\":\"->\",\"source\":6,\"target\":9},{\"name\":\"move96\",\"arrowstyle\":\"->\",\"source\":9,\"target\":6},{\"name\":\"Storage3\",\"arrowstyle\":\"->\",\"source\":10,\"target\":10},{\"name\":\"move210\",\"arrowstyle\":\"->\",\"source\":2,\"target\":10},{\"name\":\"move102\",\"arrowstyle\":\"->\",\"source\":10,\"target\":2},{\"name\":\"move1011\",\"arrowstyle\":\"->\",\"source\":10,\"target\":11},{\"name\":\"move1110\",\"arrowstyle\":\"->\",\"source\":11,\"target\":10}]}"
        data3 = "{\r\n  \"directed\": true,\r\n  \"multigraph\": false,\r\n  \"graph\": {},\r\n  \"nodes\": [\r\n    {\r\n      \"name\": \"Sim\",\r\n      \"id\": 0\r\n    },\r\n    {\r\n      \"name\": \"Event List\",\r\n      \"id\": 1\r\n    },\r\n    {\r\n      \"name\": \"Event\",\r\n      \"id\": 2\r\n    },\r\n    {\r\n      \"name\": \"Product\",\r\n      \"id\": 3\r\n    },\r\n    {\r\n      \"name\": \"Product Type\",\r\n      \"id\": 4\r\n    },\r\n    {\r\n      \"name\": \"Transition\",\r\n      \"id\": 5\r\n    },\r\n    {\r\n      \"name\": \"Place\",\r\n      \"id\": 6\r\n    },\r\n    {\r\n      \"name\": \"Tokens\",\r\n      \"id\": 7\r\n    },\r\n    {\r\n      \"name\": \"Prod-Process\",\r\n      \"id\": 8\r\n    },\r\n    {\r\n      \"name\": \"Service-Station\",\r\n      \"id\": 9\r\n    },\r\n    {\r\n      \"name\": \"Service-Items\",\r\n      \"id\": 10\r\n    },\r\n    {\r\n      \"name\": \"Transporters\",\r\n      \"id\": 11\r\n    },\r\n    {\r\n      \"name\": \"Location\",\r\n      \"id\": 12\r\n    },\r\n    {\r\n      \"name\": \"Queue\",\r\n      \"id\": 13\r\n    },\r\n    {\r\n      \"name\": \"Task\",\r\n      \"id\": 14\r\n    },\r\n    {\r\n      \"name\": \"Position\",\r\n      \"id\": 15\r\n    },\r\n    {\r\n      \"name\": \"Machines\",\r\n      \"id\": 16\r\n    }\r\n  ],\r\n  \"links\": [\r\n    {\r\n      \"name\": \"has\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 0,\r\n      \"target\": 1\r\n    },\r\n    {\r\n      \"name\": \"has\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 1,\r\n      \"target\": 2\r\n    },\r\n    {\r\n      \"name\": \"has\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 1,\r\n      \"target\": 3\r\n    },\r\n    {\r\n      \"name\": \"has\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 3,\r\n      \"target\": 4\r\n    },\r\n    {\r\n      \"name\": \"has\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 3,\r\n      \"target\": 5\r\n    },\r\n    {\r\n      \"name\": \"has\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 3,\r\n      \"target\": 6\r\n    },\r\n    {\r\n      \"name\": \"has\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 3,\r\n      \"target\": 7\r\n    },\r\n    {\r\n      \"name\": \"is\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 5,\r\n      \"target\": 8\r\n    },\r\n    {\r\n      \"name\": \"has\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 0,\r\n      \"target\": 9\r\n    },\r\n    {\r\n      \"name\": \"has\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 9,\r\n      \"target\": 10\r\n    },\r\n    {\r\n      \"name\": \"has\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 0,\r\n      \"target\": 11\r\n    },\r\n    {\r\n      \"name\": \"has\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 11,\r\n      \"target\": 12\r\n    },\r\n    {\r\n      \"name\": \"has_for_drive_queue\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 11,\r\n      \"target\": 13\r\n    },\r\n    {\r\n      \"name\": \"has\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 14,\r\n      \"target\": 11\r\n    },\r\n    {\r\n      \"name\": \"has\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 13,\r\n      \"target\": 15\r\n    },\r\n    {\r\n      \"name\": \"has\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 16,\r\n      \"target\": 13\r\n    }\r\n  ]\r\n}"
        context = {'graph3': data3}

        return render(request, self.template, context)
class ProdAgent(View):
    template = "data/prodAgent.html"

    def get(self, request):
        #data3 = "{\"directed\":true,\"multigraph\":false,\"graph\":{},\"nodes\":[{\"name\":\"pos0\",\"id\":0},{\"name\":\"pos1\",\"id\":1},{\"name\":\"pos2\",\"id\":2},{\"name\":\"\",\"id\":3},{\"name\":\"S1\",\"id\":4},{\"name\":\"S2\",\"id\":5},{\"name\":\"\",\"id\":6},{\"name\":\"S1\",\"id\":7},{\"name\":\"S3\",\"id\":8},{\"name\":\"S4\",\"id\":9},{\"name\":\"\",\"id\":10},{\"name\":\"S4\",\"id\":11}],\"links\":[{\"name\":\"move01\",\"arrowstyle\":\"->\",\"source\":0,\"target\":1},{\"name\":\"move02\",\"arrowstyle\":\"->\",\"source\":0,\"target\":2},{\"name\":\"move10\",\"arrowstyle\":\"->\",\"source\":1,\"target\":0},{\"name\":\"move12\",\"arrowstyle\":\"->\",\"source\":1,\"target\":2},{\"name\":\"move20\",\"arrowstyle\":\"->\",\"source\":2,\"target\":0},{\"name\":\"move21\",\"arrowstyle\":\"->\",\"source\":2,\"target\":1},{\"name\":\"Storage1\",\"arrowstyle\":\"->\",\"source\":3,\"target\":3},{\"name\":\"move03\",\"arrowstyle\":\"->\",\"source\":0,\"target\":3},{\"name\":\"move30\",\"arrowstyle\":\"->\",\"source\":3,\"target\":0},{\"name\":\"move34\",\"arrowstyle\":\"->\",\"source\":3,\"target\":4},{\"name\":\"move43\",\"arrowstyle\":\"->\",\"source\":4,\"target\":3},{\"name\":\"move35\",\"arrowstyle\":\"->\",\"source\":3,\"target\":5},{\"name\":\"move53\",\"arrowstyle\":\"->\",\"source\":5,\"target\":3},{\"name\":\"Storage2\",\"arrowstyle\":\"->\",\"source\":6,\"target\":6},{\"name\":\"move16\",\"arrowstyle\":\"->\",\"source\":1,\"target\":6},{\"name\":\"move61\",\"arrowstyle\":\"->\",\"source\":6,\"target\":1},{\"name\":\"move67\",\"arrowstyle\":\"->\",\"source\":6,\"target\":7},{\"name\":\"move76\",\"arrowstyle\":\"->\",\"source\":7,\"target\":6},{\"name\":\"move68\",\"arrowstyle\":\"->\",\"source\":6,\"target\":8},{\"name\":\"move86\",\"arrowstyle\":\"->\",\"source\":8,\"target\":6},{\"name\":\"move69\",\"arrowstyle\":\"->\",\"source\":6,\"target\":9},{\"name\":\"move96\",\"arrowstyle\":\"->\",\"source\":9,\"target\":6},{\"name\":\"Storage3\",\"arrowstyle\":\"->\",\"source\":10,\"target\":10},{\"name\":\"move210\",\"arrowstyle\":\"->\",\"source\":2,\"target\":10},{\"name\":\"move102\",\"arrowstyle\":\"->\",\"source\":10,\"target\":2},{\"name\":\"move1011\",\"arrowstyle\":\"->\",\"source\":10,\"target\":11},{\"name\":\"move1110\",\"arrowstyle\":\"->\",\"source\":11,\"target\":10}]}"
        data3 = "{\n  \"directed\": true,\n  \"multigraph\": false,\n  \"graph\": {},\n  \"nodes\": [\n    {\n      \"name\": \"pos0\",\n      \"id\": 0\n    },\n    {\n      \"name\": \"pos1\",\n      \"id\": 1\n    },\n    {\n      \"name\": \"pos2\",\n      \"id\": 2\n    },\n    {\n      \"name\": \"\",\n      \"id\": 3\n    },\n    {\n      \"name\": \"S1\",\n      \"id\": 4\n    },\n    {\n      \"name\": \"S2\",\n      \"id\": 5\n    },\n    {\n      \"name\": \"\",\n      \"id\": 6\n    },\n    {\n      \"name\": \"S1\",\n      \"id\": 7\n    },\n    {\n      \"name\": \"S3\",\n      \"id\": 8\n    },\n    {\n      \"name\": \"S4\",\n      \"id\": 9\n    },\n    {\n      \"name\": \"\",\n      \"id\": 10\n    },\n    {\n      \"name\": \"S4\",\n      \"id\": 11\n    }\n  ],\n  \"links\": [\n    {\n      \"name\": \"move01\",\n      \"arrowstyle\": \"->\",\n      \"source\": 0,\n      \"target\": 1,\n      \"color\": \"red\"\n    },\n    {\n      \"name\": \"move02\",\n      \"arrowstyle\": \"->\",\n      \"source\": 0,\n      \"target\": 2\n    },\n    {\n      \"name\": \"move10\",\n      \"arrowstyle\": \"->\",\n      \"source\": 1,\n      \"target\": 0\n    },\n    {\n      \"name\": \"move12\",\n      \"arrowstyle\": \"->\",\n      \"source\": 1,\n      \"target\": 2\n    },\n    {\n      \"name\": \"move20\",\n      \"arrowstyle\": \"->\",\n      \"source\": 2,\n      \"target\": 0\n    },\n    {\n      \"name\": \"move21\",\n      \"arrowstyle\": \"->\",\n      \"source\": 2,\n      \"target\": 1\n    },\n    {\n      \"name\": \"Storage1\",\n      \"arrowstyle\": \"->\",\n      \"source\": 3,\n      \"target\": 3\n    },\n    {\n      \"name\": \"move03\",\n      \"arrowstyle\": \"->\",\n      \"source\": 0,\n      \"target\": 3\n    },\n    {\n      \"name\": \"move30\",\n      \"arrowstyle\": \"->\",\n      \"source\": 3,\n      \"target\": 0\n    },\n    {\n      \"name\": \"move34\",\n      \"arrowstyle\": \"->\",\n      \"source\": 3,\n      \"target\": 4\n    },\n    {\n      \"name\": \"move43\",\n      \"arrowstyle\": \"->\",\n      \"source\": 4,\n      \"target\": 3\n    },\n    {\n      \"name\": \"move35\",\n      \"arrowstyle\": \"->\",\n      \"source\": 3,\n      \"target\": 5\n    },\n    {\n      \"name\": \"move53\",\n      \"arrowstyle\": \"->\",\n      \"source\": 5,\n      \"target\": 3\n    },\n    {\n      \"name\": \"Storage2\",\n      \"arrowstyle\": \"->\",\n      \"source\": 6,\n      \"target\": 6\n    },\n    {\n      \"name\": \"move16\",\n      \"arrowstyle\": \"->\",\n      \"source\": 1,\n      \"target\": 6\n    },\n    {\n      \"name\": \"move61\",\n      \"arrowstyle\": \"->\",\n      \"source\": 6,\n      \"target\": 1\n    },\n    {\n      \"name\": \"move67\",\n      \"arrowstyle\": \"->\",\n      \"source\": 6,\n      \"target\": 7\n    },\n    {\n      \"name\": \"move76\",\n      \"arrowstyle\": \"->\",\n      \"source\": 7,\n      \"target\": 6\n    },\n    {\n      \"name\": \"move68\",\n      \"arrowstyle\": \"->\",\n      \"source\": 6,\n      \"target\": 8\n    },\n    {\n      \"name\": \"move86\",\n      \"arrowstyle\": \"->\",\n      \"source\": 8,\n      \"target\": 6\n    },\n    {\n      \"name\": \"move69\",\n      \"arrowstyle\": \"->\",\n      \"source\": 6,\n      \"target\": 9\n    },\n    {\n      \"name\": \"move96\",\n      \"arrowstyle\": \"->\",\n      \"source\": 9,\n      \"target\": 6\n    },\n    {\n      \"name\": \"Storage3\",\n      \"arrowstyle\": \"->\",\n      \"source\": 10,\n      \"target\": 10\n    },\n    {\n      \"name\": \"move210\",\n      \"arrowstyle\": \"->\",\n      \"source\": 2,\n      \"target\": 10\n    },\n    {\n      \"name\": \"move102\",\n      \"arrowstyle\": \"->\",\n      \"source\": 10,\n      \"target\": 2\n    },\n    {\n      \"name\": \"move1011\",\n      \"arrowstyle\": \"->\",\n      \"source\": 10,\n      \"target\": 11\n    },\n    {\n      \"name\": \"move1110\",\n      \"arrowstyle\": \"->\",\n      \"source\": 11,\n      \"target\": 10\n    }\n  ]\n}"
        jinglongdata ="{\r\n  \"directed\": true,\r\n  \"multigraph\": false,\r\n  \"graph\": {},\r\n  \"nodes\": [\r\n    {\r\n      \"name\": \"pos1\",\r\n      \"id\": 0\r\n    },\r\n    {\r\n      \"name\": \"pos2\",\r\n      \"id\": 1\r\n    },\r\n    {\r\n      \"name\": \"pos3\",\r\n      \"id\": 2\r\n    },\r\n    {\r\n      \"name\": \"pos4\",\r\n      \"id\": 3\r\n    },\r\n    {\r\n      \"name\": \"工位1\",\r\n      \"id\": 4\r\n    },\r\n    {\r\n      \"name\": \"工位2\",\r\n      \"id\": 5\r\n    },\r\n    {\r\n      \"name\": \"工位3\",\r\n      \"id\": 6\r\n    },\r\n    {\r\n      \"name\": \"库存\",\r\n      \"id\": 7\r\n    },\r\n    {\r\n      \"name\": \"送料机器\",\r\n      \"id\": 8\r\n    }\r\n  ],\r\n  \"links\": [\r\n    {\r\n      \"name\": \"加工1\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 0,\r\n      \"target\": 4\r\n    },\r\n    {\r\n      \"name\": \"复位1\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 4,\r\n      \"target\": 0\r\n    },\r\n    {\r\n      \"name\": \"移动1\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 0,\r\n      \"target\": 1\r\n    },\r\n    {\r\n      \"name\": \"加工2\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 1,\r\n      \"target\": 5\r\n    },\r\n    {\r\n      \"name\": \"复位2\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 5,\r\n      \"target\": 1\r\n    },\r\n    {\r\n      \"name\": \"移动2\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 1,\r\n      \"target\": 2\r\n    },\r\n    {\r\n      \"name\": \"加工3\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 2,\r\n      \"target\": 6\r\n    },\r\n    {\r\n      \"name\": \"复位3\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 6,\r\n      \"target\": 2\r\n    },\r\n    {\r\n      \"name\": \"移动3\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 2,\r\n      \"target\": 3\r\n    },\r\n    {\r\n      \"name\": \"配送\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 7,\r\n      \"target\": 8\r\n    },\r\n    {\r\n      \"name\": \"取料\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 8,\r\n      \"target\": 7\r\n    },\r\n    {\r\n      \"name\": \"送料\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 8,\r\n      \"target\": 0\r\n    },\r\n    {\r\n      \"name\": \"复位\",\r\n      \"arrowstyle\": \"->\",\r\n      \"source\": 0,\r\n      \"target\": 8\r\n    }\r\n  ]\r\n}"
        context = { 'graph3': jinglongdata }

        return render(request, self.template, context)

class SalesOrders(View):
    template = "data/frepple/sales/sales_orders.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class SalesOrdersItems(View):
    template = "data/frepple/sales/items.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class SalesOrdersLocations(View):
    template = "data/frepple/sales/locations.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class SalesOrdersCustomers(View):
    template = "data/frepple/sales/customers.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class SalesConstraint(View):
    template = "data/frepple/sales/constraint.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class SalesDataForecastForecast(View):
    template = "data/frepple/sales/data_forecast_forecast.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class SalesDeliveryOrder(View):
    template = "data/frepple/sales/deliveryorder.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class SalesDemand(View):
    template = "data/frepple/sales/demand.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class SalesForecastMeasure(View):
    template = "data/frepple/sales/forecaset_measure.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class SalesForecast(View):
    template = "data/frepple/sales/forecast.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class SalesForecastEditor(View):
    template = "data/frepple/sales/forecasteditor.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class SalesProblem(View):
    template = "data/frepple/sales/problem.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class InventoryBuffer(View):
    template = "data/frepple/inventory/buffer.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class InventoryBufferData(View):
    template = "data/frepple/inventory/buffer_data.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class InventoryDistribution(View):
    template = "data/frepple/inventory/distribution.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class InventoryProblem(View):
    template = "data/frepple/inventory/problem.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class InventoryDistributionOrders(View):
    template = "data/frepple/inventory/distribution_orders.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class InventoryDistributionOrderSummary(View):
    template = "data/frepple/inventory/distribution_orders_summary.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class InventoryDetails(View):
    template = "data/frepple/inventory/inventory_detail.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class InventoryItemDistribution(View):
    template = "data/frepple/inventory/item_distribution.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class ManufacturingCalendars(View):
    template = "data/frepple/manufacturing/calendars.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null
class ManufacturingOrders(View):
    template = "data/frepple/manufacturing/manufacturing_orders.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class ManufacturingOrdersSummary(View):
    template = "data/frepple/manufacturing/manufacturing_orders_summary.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class ManufacturingOperationsDependencies(View):
    template = "data/frepple/manufacturing/operation_dependencies.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class ManufacturingOperationMaterials(View):
    template = "data/frepple/manufacturing/operation_materials.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class ManufacturingOperations(View):
    template = "data/frepple/manufacturing/operations.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null

class ManufacturingSubOperations(View):
    template = "data/frepple/manufacturing/sub_operations.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        return null