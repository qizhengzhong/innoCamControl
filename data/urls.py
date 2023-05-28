from django.urls import path

from . import views
from .views import DataList, DataView, DataCreate, DataUpdateView, DataDeleteView, Prediction, Prescription, Evaluation, GenerateGraphView,Map


urlpatterns = [
    #path('add', views.data_req, name='data-request'),
    path('', DataList.as_view(), name='show-data'),
    path('show/<int:pk>', DataView.as_view(), name='data-detail'),
    path('add', DataCreate.as_view(), name='data-request'),
    path('update/<int:pk>', DataUpdateView.as_view(), name='data-update'),   
    path('delete/<int:pk>', DataDeleteView.as_view(), name='data-delete'),  
    path('prediction', Prediction.as_view(), name='data-prediction'),     
    path('prescription', Prescription.as_view(), name='data-prescription'),   
    path('evaluation', GenerateGraphView.as_view(), name='data-evaluation'), 
    path('map', Map.as_view(), name='data-map'),     
]