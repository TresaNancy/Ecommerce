from django.urls import path,include
from .import views




urlpatterns = [
    path('dashboard',views.dashboard, name ='dashboard'),
    path('adminpanel/account_register',views.account_register, name ='account_register'),
    path('adminpanel/brands',views.brands, name ='brands'),
    path('adminpanel/categories',views.categories, name ='categories'),
    path('adminpanel/error_404',views.error_404, name ='error_404'),
    path('add_product',views.add_product, name ='add_product'),
    path('product_filter',views.product_filter, name ='product_filter'),
    path('adminpanel/form_product_2',views.form_product_2, name ='form_product_2'),
    path('adminpanel/form_product_3',views.form_product_3, name ='form_product_3'),
    path('adminpanel/form_product_4',views.form_product_4, name ='form_product_4'),
    path('adminpanel/orders_1',views.orders_1, name ='orders_1'),
    path('adminpanel/orders_2',views.orders_2, name ='orders_2'),
    path('adminpanel/products_grid',views.products_grid, name ='products_grid'),
    path('adminpanel/products_grid_2',views.products_grid_2, name ='products_grid_2'),
    path('adminpanel/products_list',views.products_list, name ='products_list'),
    path('adminpanel/reviews',views.reviews, name ='reviews'),
    path('adminpanel/seller_detail',views.seller_detail, name ='seller_detail'),
    path('adminpanel/settings_1',views.settings_1, name ='settings_1'),
    path('adminpanel/settings_2',views.settings_2, name ='settings_2'),
     path('adminpanel/transactions_1',views.transactions_1, name ='transactions_1'),
      path('adminpanel/transactions_2',views.transactions_2, name ='transactions_2'),
      path('adminpanel/sellers_cards',views.sellers_cards, name ='sellers_cards'),
      path('adminpanel/sellers_list',views.sellers_list, name ='sellers_list'),
      path('adminpanel/orders_detail',views.orders_detail, name ='orders_detail'),
    


    
    
]

