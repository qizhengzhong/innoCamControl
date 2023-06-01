from django.urls import path

from . import views
from .views import DataList, FloorPlan,GanntChart, DataView, DataCreate, DataUpdateView, DataDeleteView, Prediction, Prescription, Evaluation, GenerateGraphView,Map, Chatbot, ProdAgent, Overview, CoAgent


urlpatterns = [
    #path('add', views.data_req, name='data-request'),
    path('', DataList.as_view(), name='show-data'),
    path('overview', Overview.as_view(), name='overview'),
    path('show/<int:pk>', DataView.as_view(), name='data-detail'),
    path('add', DataCreate.as_view(), name='data-request'),
    path('update/<int:pk>', DataUpdateView.as_view(), name='data-update'),   
    path('delete/<int:pk>', DataDeleteView.as_view(), name='data-delete'),  
    path('prediction', Prediction.as_view(), name='data-prediction'),     
    path('prescription', Prescription.as_view(), name='data-prescription'),   
    path('evaluation', GenerateGraphView.as_view(), name='data-evaluation'), 
    path('resourceagent', Map.as_view(), name='data-map'),
    path('chatbot', Chatbot.as_view(), name='data-chatbot'),
    path('prodagent', ProdAgent.as_view(), name='data-prodAgent'),
    path('dataagent', DataList.as_view(), name='data-dataAgent'),
    path('coagent', CoAgent.as_view(), name='data-coAgent'),
    path('floorplan', FloorPlan.as_view(), name='data-coAgent'),
    path('ganntchart', GanntChart.as_view(), name='data-ganntChart'),
]