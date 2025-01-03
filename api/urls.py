# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.message_list, name='message-list'),
    path('messages/<int:pk>/', views.message_detail, name='message-detail'),
    path('product/imges/', views.product_images, name='product_imges'),
        path('product/imges/<int:id>/', views.product_image_id, name='product_imge_id'),

     path('product/imges/<int:pk>/', views.product_imge, name='product_imge'),

    path('product/imges/swapper', views.swapper_images, name='swapper_imges'),
    path('attendance/', views.AttendanceAPIView.as_view(), name='attendance-api'),



     

]
