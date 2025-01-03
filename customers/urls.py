from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  
    path('', views.customer_bills_chart, name='customer_panel'),
    path('edit/' , views.edit_profile , name="edit_profile"),
    path('password/' , views.change_password , name="change_password"),
       path('delete/<int:id>/', views.delete_costomers, name='delete_costomers'),
    path('editing/<int:id>/' , views.edit_customer , name="edit_customer"),
    path('add/' , views.add_costomer , name="add_costomer"),
    path('list/' , views.costomers_List , name="costomers_List"),
      path('login/', views.customer_login, name='customer_login'),
    path('login/tex/', views.customer_login_tex, name='customer_login_tex'),
       path('logout/', views.customer_logout, name='customer_logout'),
    path('bill/usd/' , views.fetch_bills_usd_list , name="fetch_bills_usd_list"),
        path('bill/tr/' , views.fetch_bills_tr_list , name="fetch_bills_tr_list"),
    path('bill/usd/<int:id>' , views.view_bill , name="view_bill_usd"),
        path('bill/tr/<int:id>' , views.view_bill_tr , name="view_bill_tr"),
  path('<int:id>/', views.customer_bills_chart_admin, name='customer_bills_chart_admin'),
    #  path('payment/tl/<int:customer_id>/', views.customer_paymenttl_view, name='customer_paymenttl'),
      path('payment/tl/<int:customer_id>/', views.add_payment_and_list_tr, name='add_payment_and_list_tr'),


  # path('payment/usd/<int:customer_id>/', views.customer_paymentUSD_view, name='customer_paymentusd'),
      path('payment/usd/<int:customer_id>/', views.add_payment_and_list_usd, name='add_payment_and_list_usd'),

      



   
      path('payment/usd/<int:id>/delete/ok', views.delete_paymentokusd, name='delete_paymentokusd'),


 path('payment/tr/<int:id>/delete', views.delete_paymentTr, name='delete_paymentTr'),
      path('payment/tr/<int:id>/delete/ok', views.delete_paymentokTr, name='delete_paymentokTr'),


    

    path('chat/tl/', views.customer_list_view, name='customer_list_tl'),
    path('chattl/<int:customer_id>/', views.billsTL_and_payments_view, name='bills_and_payments'),

    path('chat/usd/', views.costomer_chat_usd, name='customer_list_usd'),
    path('chatusd/<int:customer_id>/', views.billsusd_and_payments_view, name='chat_usd'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
