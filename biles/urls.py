from django.urls import path
from  . import views


urlpatterns = [
    path('product/Ham/add/', views.addProductHam, name='addProductham'),
    path('Product/Ham/', views.ProductHam_List, name='ProductHam_List'),
    path('Product/Ham/<int:id>/', views.fatch_ProductHam, name='fatch_ProductHam'),
    path('Product/Ham/edit/<int:id>/', views.update_ProductHam, name='update_ProductHam'),
    path('Product/Ham/delete/<int:id>/', views.delete_ProductHamm, name='delete_ProductHamm'),
    path('Product/Ham/uplode/', views.uplode_ProductHam, name='uplode_ProductHam'),
    path('Product/ham/download/',views.download_ProductHam_csv, name='download_ProductHam_csv'),

    #end of  Product Ham

     path('pakage/add/', views.addPakage, name='addPakage'),
    path('pakage/', views.pakage_List, name='pakage_List'),
    path('pakage/<int:id>/', views.fatch_pakage, name='fatch_pakage'),
   path('pakage/edit/<int:id>/', views.update_pakage, name='update_pakage'),
    path('pakage/delete/<int:id>/', views.delete_pakage, name='delete_pakage'),
    path('pakage/uplode/', views.uplode_package, name='uplode_package'),
    path('pakage/download/',views.download_pakage_csv, name='download_pakage_csv'),


  #end of  project
    path('jar/add/', views.addjar, name='addjar'),
   path('jar/', views.jar_List, name='jar_List'),
    path('jar/<int:id>/', views.fatch_jar, name='fatch_jar'),
   path('jar/edit/<int:id>/', views.update_jar, name='update_jar'),
    path('jar/delete/<int:id>/', views.delete_jar, name='delete_jar'),
   path('jar/uplode/', views.uplode_jar, name='uplode_jar'),
    path('jar/download/',views.download_jar_csv, name='download_jar_csv'),


    #end of  jar

    path('product/add/', views.addProduct, name='addProduct'),
    path('product/', views.Product_List, name='Product_List'),
    path('product/<int:id>/', views.fatch_Product, name='fatch_Product'),
    path('Product/edit/<int:id>/', views.update_Product, name='update_Product'),
    path('Product/delete/<int:id>/', views.delete_Product, name='delete_Product'),
    path('Product/uplode/', views.uplode_product, name='uplode_product'),
    path('Product/download/',views.download_product_csv, name='download_Product_csv'),
    path('product/refresh/', views.refresh, name='refresh'),


    



  path('costomers/add', views.add_costomer, name='add_costomer'),
 
  
      path('costomers/uplode/', views.upload_customers, name='uplode_costomers'),
      path('costomers/download/',views.download_costomers_csv, name='download_costomers_csv'), #upload_uds_bills



    


    path('usd/', views.fetch_bills_list_usd, name='fetch_bills_list_usd'),   # for list 1
   
    path('usd/uplode/', views.upload_uds_bills, name='upload_uds_bills'), #uplude 3
    path('usd/<int:id>/', views.view_bill, name='view_bills'), # view4
    path('recalculate/', views.recalculate, name='recalculate_uds_bills'), # recalculating all fileds 5
    path('usd/recalculate/<int:pk>/', views.recalculate_view, name='recalculate'), # recalculating one bill 6
    path('usd/inner/uplode/', views.upload_uds_bills_inner, name='upload_uds_bills_inner'), #7
    path('usd/inner/update/<int:pk>/', views.fatch_usd, name='fatch_usd'),#8
    path('usd/inner/update/filed/<int:pk>/', views.edit_uds_bill_inner_single, name='edit_uds_bill_inner_single'), 
    path('usd/inner/filed/delete/<int:pk>/', views.delete_usd_inner, name="delete_usd_inner"), 
     path('usd/delete/<int:pk>/', views.delete_bill_usd, name='delete_bill_usd'), # view 12






    path('tr/', views.fetch_bills_list_Tr, name='fetch_bills_list_Tr'), #for list 1
 
 #  path('tr/uplode/', views.upload_uds_bills, name='upload_uds_bills'), #uplode 3
     path('tr/<int:id>/', views.view_bill_tr, name='view_bill_tr_admin'), # view 4
     path('tr/recalculate/', views.recalculate_tr_bills_view, name='recalculate_tr_bills_view'), # recalculating all fileds 5
   # path('tr/recalculate/<int:pk>/', views.recalculate_view, name='recalculate'), # recalculating one bill 6
  #  path('usd/inner/uplode/', views.upload_uds_bills_inner, name='upload_uds_bills_inner'), #7
    path('tr/inner/update/<int:pk>/', views.fatch_tr, name='fatch_tr'), #8
    path('tr/inner/<int:pk>/', views.edit_tr_bill_inner_single, name='edit_tr_bill_inner_single'),
    path('tr/inner/filed/delete/<int:pk>/', views.delete_tr_inner, name="delete_tr_inner"), 
    path('tr/delete/<int:pk>/', views.delete_bill_tr, name='delete_bill_tr'), # view 12

     path('c/', views.tr_bills_data, name='tr_bills_data'),


       path('', views.bills_chart_admin, name='bills_chart_admin'),
       path('product/json/', views.product_list_json, name='bills_chart'),
              path('product/r/', views.sales_report, name='sales_report'),






    path('us/', views.list_bills, name='list_bills'),  # List bills URL
    path('us/mark_done/<int:bill_id>/', views.mark_bill_done, name='mark_bill_done'),  # Mark bill as done


    path('tt/', views.list_bills_tt, name='list_bills_tr'),  # List bills URL
    path('tt/mark_done/<int:bill_id>/', views.mark_bill_done_tt, name='mark_bill_done_tt'),  # Mark bill as done




    





]



