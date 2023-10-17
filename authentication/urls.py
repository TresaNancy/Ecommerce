from django.urls import path,include
from .import views
from django.conf.urls.static import static



urlpatterns = [
    path('signin',views.signin, name ='signin'),
    path('signup',views.signup, name='signup'),
    path('home',views.home, name='home'),
    path('user_logout',views.user_logout, name='user_logout'),
    path('forgetpassword',views.forgetpassword, name='forgetpassword'),
    path('otp_verification',views.otp_verification, name='otp_verification'),
    path('change_password',views.change_password, name='change_password'),
 
 
 
 

    
]