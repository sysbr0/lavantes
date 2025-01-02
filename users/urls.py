from django.urls import path
from  . import views


urlpatterns = [

          path('',views.user_profile, name='user_profile'),
          path('signup/', views.user_signup, name='signup'),
         
          path('logout/', views.user_logout, name='logout'),
      
            path('login/' , views.login_view , name="login"),
          





]