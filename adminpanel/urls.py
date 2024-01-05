from django.urls import path,include
from .import views




urlpatterns = [
    path('dashboard',views.dashboard, name ='dashboard'),
     path("manageuser",views.manageuser,name="manageuser"),
    path('user_block/<int:id>/',views.user_block,name="user_block"),
    path('user_unblock/<int:id>/',views.user_unblock,name="user_unblock"),

     # product management
    path('product',views.product,name="product"),
    path('product/edit/<int:id>/', views.edit_product, name='edit_product'),
    path('product_block/<id>',views.product_block,name="product_block"),
    path('product_unblock/<id>',views.product_unblock,name="product_unblock"),
    path('add_product', views.add_product, name='add_product'),
    path('product_view',views.product_view,name='product_view'),

    # category management
    path('category', views.category, name="category"),
    path('category_block/<id>',views. category_block,name="category_block"),
    path('category_unblock/<id>',views. category_unblock,name="category_unblock"),
    path('add_category', views.add_category,name="add_category"),
    path('category/edit/<int:id>',views.edit_category,name="edit_category"),
    
    # variant management

    path('colour/<int:id>', views.colour, name="colour"),
    path('colour_details/<int:id>',views.colour_details, name="colour_details"),
    path('delete_colour/<int:id>', views.delete_colour, name="delete_colour"),

    
    # brand management
     path('brand', views.brand, name="brand"),
    path('add_brand', views.add_brand, name="add_brand"),
    path('brand_block/<int:brand_id>/', views.brand_block, name="brand_block"),
    path('brand_unblock/<int:brand_id>/', views.brand_unblock, name="brand_unblock"),

     # coupon managemnt
    path('coupon', views.coupon, name="coupon"),
    path('add_coupon',views.add_coupon, name="add_coupon"),
    path('coupon_block/<int:coupon_id>/', views.coupon_block, name="coupon_block"),
    path('coupon_unblock/<int:coupon_id>/', views.coupon_unblock, name="coupon_unblock"),

    # user order management
    path('manageorder', views.manage_order, name="manage_order"),
    path('manage_orderstatus/<int:id>',views.manage_orderstatus,name="manage_orderstatus"),
    
    path('sales_report', views.sales_report, name="sales_report"),

    # path('adminpanel/account_register',views.account_register, name ='account_register'),
    # path('categories/', views.category_view, name='category_view'),
    # # Define URL patterns for specific actions
    # path('categories/add/', views.category_view, name='add_category'),
    # path('categories/edit/', views.category_view, name='edit_category'),
    # path('categories/delete/', views.category_view, name='delete_category'),
    # path('sub_categories/', views.sub_category_view, name='sub_category_view'),
    # # Define URL patterns for specific actions
    # path('sub_categories/add/', views.sub_category_view, name='add_sub_category'),
    # path('sub_categories/edit/', views.sub_category_view, name='edit_sub_category'),
    # path('sub_categories/delete/', views.sub_category_view, name='delete_sub_category'),
    # path('brands/',views.brand_view, name ='brand_view'),
    # # Define URL patterns for specific actions
    # path('brands/add/', views.brand_view, name='add_brand'),
    # path('brands/edit/', views.brand_view, name='edit_brand'),
    # path('brands/delete/', views.brand_view, name='delete_brand'),
    
    # path('adminpanel/error_404',views.error_404, name ='error_404'),
    # path('add_product',views.add_product, name ='add_product'),
    # path('product_view',views.product_view,name='product_view'),
    # path('update_product/<int:product_id>/',views.update_product,name='update_product'),
    # path('product_block/<id>',views.product_block,name="product_block"),
    # path('product_unblock/<id>',views.product_unblock,name="product_unblock"),
    # # path('delete_product/',views.delete_product,name='delete_product'),
    # path('product_filter',views.product_filter, name ='product_filter'),


    # path('adminpanel/form_product_2',views.form_product_2, name ='form_product_2'),
    # path('adminpanel/form_product_3',views.form_product_3, name ='form_product_3'),
    # path('adminpanel/form_product_4',views.form_product_4, name ='form_product_4'),
    # path('adminpanel/orders_1',views.orders_1, name ='orders_1'),
    # path('adminpanel/orders_2',views.orders_2, name ='orders_2'),
    # path('adminpanel/products_grid',views.products_grid, name ='products_grid'),
    
    # path('adminpanel/products_list',views.products_list, name ='products_list'),
    # path('adminpanel/reviews',views.reviews, name ='reviews'),
    # path('adminpanel/seller_detail',views.seller_detail, name ='seller_detail'),
    # path('adminpanel/settings_1',views.settings_1, name ='settings_1'),
    # path('adminpanel/settings_2',views.settings_2, name ='settings_2'),
    #  path('adminpanel/transactions_1',views.transactions_1, name ='transactions_1'),
    #   path('adminpanel/transactions_2',views.transactions_2, name ='transactions_2'),
    #   path('adminpanel/sellers_cards',views.sellers_cards, name ='sellers_cards'),
    #   path('adminpanel/sellers_list',views.sellers_list, name ='sellers_list'),
    #   path('adminpanel/orders_detail',views.orders_detail, name ='orders_detail'),
    


    
    
]

