from django.urls import path,include
from .import views


urlpatterns = [
    # path('add_to_cart/<int:id>',views.add_to_cart, name ='add_to_cart'),
    # path('remove_from_cart/<int:cart_item_id>',views.remove_from_cart, name ='remove_from_cart'),
    # path('update_cart/<int:cart_item_id>',views.update_cart, name ='update_cart'),
    # path('cart',views.cart, name ='cart'),
     path('', views.cart, name='cart'),
     path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
     # path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
     path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
     # path('update_cart_item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
     path('update_quantity', views.update_quantity, name='update_quantity'),
     path('checkout/', views.checkout, name='checkout'),
     path('wishlist_to_cart/<int:product_id>/<int:colour_id>/',views.wishlist_to_cart,name='wishlist_to_cart'),

    #wishlist
    path('wishlist/',views.wishlist,name="wishlist"),
    path('add_to_wishlist/<int:colour_id>/',views.add_to_wishlist,name="add_to_wishlist"),
    # path('remove_wishlist_item/<int:product_id>/<int:wishlist_id>/',views.remove_wishlist_item,name="remove_wishlist_item"),
    path('remove_wishlist_item/<int:product_id>/<int:wishlist_id>/', views.remove_wishlist_item, name="remove_wishlist_item"),
]   