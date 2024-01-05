from django.urls import path,include
from .import views
from django.conf.urls.static import static


urlpatterns = [
    # path('cart/<int:id>/',views.cart, name ="cart"),
    # path('checkout/',views.checkout, name="checkout"),
    # # path('contact/',views.contact, name ="contact"),
    path('product_details/<int:id>/',views.product_details, name="product_details"),
    path('',views.index, name="index"),
    path('shop/',views.shop,name="shop"),

    # path('',views.home,name="home"),
    path('contact',views.contact,name="contact"),
    # path('checkout',views.checkout,name="checkout"),
    # path('payment',views.payment,name="payment"),
    # path('store',views.store,name="store"),
    # path('banner',views.banner,name="banner"),
    # path('shop',views.shop,name="shop"),
    # path('about',views.about,name="about"),
   
    # path('product_details/<int:productid>',views.product_details,name="product_details"),
    # path('categories/<int:categoryid>',views.categories, name="categories"),
    # path('get-variant-details/', views.get_variant_details, name='get-variant-details'),
    # path('get-variant-stock-status/', views.get_variant_stock_status, name='get_variant_stock_status'),
    # # search and filter
    # path('search',views.search, name="search"),
    # path('filter_products_by_price',views.filter_products_by_price,name="filter_products_by_price"),

    
  
    

    
]