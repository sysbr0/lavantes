from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
  
    path('view/<int:id>/', views.fatch_clints, name='fatch_clints'),
    path('<int:id>/' , views.clint_bills_chart_admin , name="clint_bills_chart_admin"),
    path('chart/' , views.bills_chart_admin , name="bills_chart_admin"),

    path('chat/', views.clint_chat, name='clint_chat'),
    path('chat/<int:id>/', views.bills_and_payments_view, name='bills_and_payments_view'),
    path('payment/edit/<int:pk>/', views.edit_clintPymant, name='edit_clintPymant'),

     path('add/payment/<int:clint_id>/', views.add_payment_and_list, name='add-payment'),
    path('delete/payment/<int:payment_id>/', views.delete_payment, name='delete-payment'),



    path('repor/<int:client_id>/', views.client_report, name='client_report'),


]


    