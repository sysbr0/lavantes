from django.urls import path
from  . import views


urlpatterns = [

         path('test/',views.test, name='test'),


        path('buying-types/', views.buying_type_list, name='buying_type_list'),
        path('buying-types/new/', views.buying_type_create, name='buying_type_create'),
        path('buying-types/<int:pk>/edit/', views.buying_type_update, name='buying_type_update'),
        path('buying-types/<int:pk>/delete/', views.buying_type_delete, name='buying_type_delete'),




        path('buying/', views.general_buying_list, name='general_buying_list'), 
        path('buying/new/', views.create_general_buying, name='create_general_buying'),
        path('general_buying/edit/<int:pk>/', views.edit_general_buying, name='edit_general_buying'),
        path('general_buying/delete/<int:pk>/', views.delete_general_buying, name='delete_general_buying'),
        path('general_buying/view/<int:id>/', views.view, name="view_buying"),
        
    path('buying/jar/<int:pk>/', views.buying_jar, name='buying_jar'),
    path('buying/jar/<int:pk>/<int:id>/delete/', views.delete_jar_innner,name="delete_jar_innner"),

path('buying/<str:name>/<int:pk>/edit/', views.swiching, name="swiching"),



    path('buying/jar_off/<int:pk>/', views.buying_jar_off, name='buying_jar_off'),

    path('buying/jar_off/<int:pk>/<int:id>/delete/', views.delete_jar_off_innner,name="delete_jar_off_innner"),

      path('buying/pakage/<int:pk>/', views.buying_pakage, name='buying_pakage'),
      path('buying/pakage/<int:pk>/<int:id>/delete/', views.delete_pakage_inner,name="delete_pakage_inner"),



    


 path('material/', views.material_list, name='material-list'),  # List all materials
    path('material/add/', views.material_create, name='material-create'),  # Add a new material
    path('material/edit/<int:pk>/', views.material_edit, name='material-edit'),  # Edit a specific material
    path('material/delete/<int:pk>/', views.material_delete, name='material-delete'), 

   



path('material/raw/', views.raw_materials_list, name='raw_materials_list'),  # List page
    path('material/raw/add/', views.add_raw_material, name='add_raw_material'),  # Add page

      path('material/raw/update/<int:pk>/', views.raw_material_update, name='raw_material_update'),
    path('material/raw/delete/<int:pk>/', views.raw_material_delete, name='raw_material_delete'),


  path('buying/material/raw/<int:pk>/', views.buying_Rawmaterials, name='buying_Rawmaterials'),
  path('buying/material/raw/', views.raw_materials_summary,name="raw_materials_summary"),
      path('buying/material/raw/<int:pk>/<int:id>/delete/', views.delete_Rawmaterials,name="delete_Rawmaterials"),





path('material/Factor/', views.Factor_materials_list, name='Factor_materials_list'),  # List page
    path('material/Factor/add/', views.add_Factor_material, name='add_Factor_material'),  # Add page

      path('material/Factor/update/<int:pk>/', views.Factor_material_update, name='Factor_material_update'),
    path('material/Factor/delete/<int:pk>/', views.Factor_material_delete, name='Factor_material_delete'),




 path('buying/material/Factor/<int:pk>/', views.buying_Factormaterials, name='buying_Factormaterials'),
  path('buying/material/Factor/', views.factory_materials_summary, name='factory_materials_summary'),
 
      path('buying/material/Factor/<int:pk>/<int:id>/delete/', views.delete_Facorymaterials,name="delete_Factormaterials"),
       path('assets/', views.assets_list_view, name='assets-list'),  # List all materials
       path('assets/add/', views.Asstes_create, name='assets-create'),  # Add
      path('assets/edit/<int:pk>/', views.Asstes_edit, name='assets-edit'),  # Edit a specific material
      path('assets/delete/<int:pk>/', views.Asstes_delete, name='assets-delete'),  # Edit a specific material

          path('assets/json/', views.assets_list_json, name='assets-list-json'),
            path('buying/assets/<int:pk>/', views.buying_assets_inner,name="buying_assets_inner"),
                  path('buying/assets/<int:pk>/<int:id>/delete/', views.delete_assets,name="delete_assets"),
                  path('buying/pay/<int:id>/', views.create_clint_payment,name="makePyment"),

                #  path('buying/pay/', views.create_clint_payment,name="create_clint_payment"),



            path('buying/spendes/<int:pk>/', views.buying_Spendes_inner,name="buying_Spendes_inner"),
     path('buying/spendes/<int:pk>/<int:id>/delete/', views.delete_spendes,name="delete_spendes"),
                  









      

  

 


]
