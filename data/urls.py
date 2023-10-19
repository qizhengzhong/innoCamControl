from django.urls import path

from . import views
from .views import *


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
    path('ontologysim', OntologySim.as_view(), name='data-ontologySim'),
    path('ontologysimkpis', OntologySimKpis.as_view(), name='data-ontologySimKpis'),
    path('ontologydesign', OntologyDesign.as_view(), name='data-ontologyDesign'),
    path('salesorders', SalesOrders.as_view(), name='data-SalesOrders'),
    path('salesordersitems', SalesOrdersItems.as_view(), name='data-SalesOrdersItems'),
    path('salesorderslocations', SalesOrdersLocations.as_view(), name='data-SalesOrdersLocations'),
    path('salesorderscustomers', SalesOrdersCustomers.as_view(), name='data-SalesOrdersCustomers'),
    path('salesconstraint', SalesConstraint.as_view(), name='data-SalesConstraint'),
    path('salesdataforecastforecast', SalesDataForecastForecast.as_view(), name='data-SalesDataForecastForecast'),
    path('salesdeliveryorder', SalesDeliveryOrder.as_view(), name='data-SalesDeliveryOrder'),
    path('salesdemand', SalesDemand.as_view(), name='data-SalesDemand'),
    path('salesforecastmeasure', SalesForecastMeasure.as_view(), name='data-SalesForecastMeasure'),
    path('salesforecast', SalesForecast.as_view(), name='data-SalesForecast'),
    path('salesforecasteditor', SalesForecastEditor.as_view(), name='data-SalesForecastEditor'),
    path('salesproblem', SalesProblem.as_view(), name='data-SalesProblem'),
    path('inventorybuffer', InventoryBuffer.as_view(), name='data-InventoryBuffer'),
    path('inventorydistributionorders', InventoryDistributionOrders.as_view(), name='data-InventoryDistributionOrders'),
    path('inventorydistributionordersummary', InventoryDistributionOrderSummary.as_view(), name='data-InventoryDistributionOrderSummary'),
    path('inventorydetails', InventoryDetails.as_view(), name='data-InventoryDetails'),
    path('inventoryitemdistribution', InventoryItemDistribution.as_view(), name='data-InventoryItemDistribution'),
    path('manufacturingcalendars', ManufacturingCalendars.as_view(), name='data-ManufacturingCalendars'),
    path('manufacturingorders', ManufacturingOrders.as_view(), name='data-ManufacturingOrders'),
    path('manufacturingorderssummary', ManufacturingOrdersSummary.as_view(), name='data-ManufacturingOrdersSummary'),
    path('manufacturingoperationsdependencies', ManufacturingOperationsDependencies.as_view(), name='data-ManufacturingOperationsDependencies'),
    path('manufacturingoperationmaterials', ManufacturingOperationMaterials.as_view(), name='data-ManufacturingOperationMaterials'),
    path('manufacturingoperations', ManufacturingOperations.as_view(), name='data-ManufacturingOperations'),
    path('manufacturingsuboperations', ManufacturingSubOperations.as_view(), name='data-ManufacturingSubOperations'),

]