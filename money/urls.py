from django.urls import path
from .views import money_source_list, money_source_create, money_source_update, money_source_delete , genaral_pyment_list  

urlpatterns = [
    path('source/', money_source_list, name='moneysource_list'),
    path('source/add/', money_source_create, name='moneysource_add'),
    path('source/<int:pk>/edit/', money_source_update, name='moneysource_edit'),
    path('source/<int:pk>/delete/', money_source_delete, name='moneysource_delete'),
    path('history/', genaral_pyment_list, name='general_payment_list'),
     

    

]
