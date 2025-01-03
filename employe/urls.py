from django.urls import path
from  . import views



urlpatterns = [
     # ++ today attandnce list 
     path('' , views.today_attaned , name="today_attaned"),
          # ++ today attandnce list 
     path('today/added/' , views.attendance_panel , name="today_attaned"),
     path('attendance/json/' , views.attendance_json , name="get_latest_attendance"),
     
     

    # ++ public fo viwing the list of attandince 
    
   path('calendar/', views.calendar_view, name='calendar'), #clander view 
       path('calendar/<int:year>/<int:month>/<int:day>/', views.attendance_view, name='attendance'),


# -- list of employe 
    path('list/' , views.employee_list_view , name="employee_list_view"),
# -- edit employe
    path('edit/<int:id>/' , views.edit_employee , name="edit_employee"),
 # -- add attancde today    
     path('attendance/add/<int:id>/', views.add_attendance, name='add_attendance'),

# -- search from to
    path('from/to/', views.attendance_views, name='attendance_from_to'),


# + ID serch 
    path('search/', views.tc_input_view, name='tc_input_view'),
        path('<int:id>/', views.serch_result_new, name='serch_result'),
        path('<int:id>/report/', views.employee_report, name='employee_report'),
 

   
# + log in 
 path('login/', views.employ_login_view, name='employ_login_view'),
    
  
  path('today/' , views.today_attaned_admin , name="today_attaned_admin"),



path('admin/pyment/', views.pyment, name='pyment'),


    path('download/employee-csv/', views.download_employee_csv, name='download_employee_csv'),
        path('download/attendance-csv/', views.download_attendance_csv, name='download_attendance_csv'),


    path('admin/list/' , views.employee_list_view , name="employee_list_view"),


#

  path('admin/attendance/<int:year>/<int:month>/<int:day>/', views.attendance_view_admin, name='attendance_view_admin'),
  
     

    path('admin/pyment/<int:id>/', views.mark_attendance_paid, name='mark_attendance_paid'),
    path('admin/pyment/all/<int:id>/',views.mark_all_attendance_paid, name='mark_all_attendance_paid'),



# path('employ/<int:employee_id>/', views.employee_detail, name='employee_detail'),
 



      path('admin/attendance/delete/<int:id>/', views.delete_attendance, name='delete_attendance'),

 
  path('admin/today/' , views.today_attaned_admin , name="today_attaned_admin"),
      path('admin/today/add/' , views.add_today , name="add_today"),
         path('admin/calendar/', views.calendar_view, name='calendar'), #clander view 
            path('admin/add/' , views.add_employee , name="add_employe"),


       path('chat/<int:id>/', views.chat_view, name='chat_view'),

       path('chat/', views.admin_chat, name='admin_chat'),

       


    path('export_attendance_csv/', views.export_attendance_csv, name='export_attendance_csv'),



            

# salory 

path('admin/salary/add/<int:id>', views.salary_create, name="salary_create") , 
path('admin/salary/edit/<int:id>/<int:pk>/', views.salary_update_view, name="salary_update_view") , 
path('admin/salary/', views.salary_list, name="salary_list") , 

path('admin/salary/not/', views.employee_Salary_not_add, name="employee_Salary_not_add") , 


path('admin/pyment/add/<int:id>/', views.employee_payment_view, name="employee_payment_view") , 
path('admin/pyment/delete/<int:id>/', views.delete_payment, name="delete_payment") ,
path('admin/pyment/delete/<int:id>/ok/', views.delete_paymentok, name="delete_paymentok") ,









path('admin/', views.dashboard , name="dashboard" ), 
path('chart/', views.employee_attendance_chart , name="employee_attendance_chart" ),
path('ch/', views.checker , name="checker" ),

path("admin/employe/add/" ,views.Admin_add_employee , name="Admin_add_employee"),



    
         

]



