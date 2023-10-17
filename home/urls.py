from django.urls import path,include
from .import views
from django.conf.urls.static import static


urlpatterns = [
    path('cart/',views.cart, name ="cart"),
    path('checkout/',views.checkout, name="checkout"),
    path('contact/',views.contact, name ="contact"),
    path('detail/<int:id>/',views.detail, name="detail"),
    path('',views.index, name="index"),
    path('shop/',views.shop,name="shop"),
    path('singin/',views.singin,name="singin"),
    

    
]