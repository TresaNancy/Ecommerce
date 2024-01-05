from django.urls import path,include
from .import views
from django.conf.urls.static import static


urlpatterns = [

    path('user_page',views.user_page, name="user_page"),
    path('update_profile',views.update_profile, name="update_profile"),
    path('my_profile',views.my_profile, name="my_profile"),
   
   #address Management
   path('address',views.address,name="address"),
   path('add_address',views.add_address,name="add_address"),
   path('edit_address/<int:id>', views.edit_address, name="edit_address"),
   path('delete_address/<int:id>',views.delete_address,name="delete_address"),
   path('set_default/<int:id>',views.set_default, name="set_default"),

   # orders
    path('order_detail',views.order_detail, name="order_detail"),
    path('order_detail_view/<uuid:bulk_order_id>',views.order_detail_view,name="order_detail_view"),
    path('cancel_order/<int:order_id>/',views.cancel_order,name="cancel_order"),
    
    path('user_coupon', views.user_coupon, name="user_coupon"),
    


    
]