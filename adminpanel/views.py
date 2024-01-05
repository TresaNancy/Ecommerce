from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .models import *
from orders.models import *
from cart.models import *
from authentication.models import CustomUser
from django.contrib import messages
from django.db.models import Q,Sum
import json
from datetime import datetime


# Create your views here.
@never_cache
@login_required(login_url='/signin')
def dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser==True:
        status_order_totals = Order.objects.values('status').annotate(total_amount=Sum('order_total'))
    else:
        return redirect('admin_login')

    orders = Order.objects.all()
    print(orders,"kkkkkkkkkkkkkkkkk")

    data_dict = {}  # Dictionary to store counts per category per interval

    interval = request.GET.get('interval', 'monthly')  # Get the selected interval (default: monthly)
    current_datetime = timezone.now()

    for order in orders:
        if interval == 'monthly':
            time_period = order.created_at.strftime('%b %Y')  # Monthly interval
        elif interval == 'yearly':
            time_period = order.created_at.strftime('%Y')  # Yearly interval
        elif interval == 'weekly':
            time_period = f"Week {current_datetime.strftime('%A')}, {current_datetime.year}"  # Weekly interval
        else:
            # Default to monthly if interval is not recognized
            time_period = order.created_at.strftime('%b %Y')
        
        category = order.product.category.category_name
        
        if time_period not in data_dict:
            data_dict[time_period] = {}
        
        if category not in data_dict[time_period]:
            data_dict[time_period][category] = 0
        
        data_dict[time_period][category] += 1

    # Convert data_dict to JSON format
    data_dict_json = json.dumps(data_dict)
    context = {
        'data_dict_json' : data_dict_json,
        'status_order_totals': status_order_totals,
    }
    return render(request,'adminpanel/dashboard.html',context)

@never_cache
@login_required(login_url='signin')
def manageuser(request):
    if not request.user.is_authenticated or request.user.is_superuser==False:
        return redirect('signin')
    if request.user.is_authenticated and request.path!= reverse('manageuser'):
        return redirect('manageuser')
    
    user_list = CustomUser.objects.filter(is_superuser=False)

    if 'search' in request.GET:
        q= request.GET['search']
        user_list = CustomUser.objects.filter(Q(name__icontains=q) | Q(email__icontains=q) | Q(id__icontains=q))

    context = {'user_list':user_list}
    return render(request, 'adminpanel/userdetail.html', context)  

@never_cache
@login_required(login_url='signin')
def user_block(request,id):
    d= CustomUser.objects.get(id=id)
    d.is_active=False
    d.save()
    messages.error(request,"Blocked Successfully")
    return redirect('manageuser')

@never_cache
@login_required(login_url='signin')
def user_unblock(request,id):
    d=CustomUser.objects.get(id=id)
    d.is_active=True
    d.save()
    messages.success(request,"Unblock Successfully")
    return redirect("manageuser")


# product management
@never_cache
@login_required(login_url='/signin')
def product(request):
        if not request.user.is_authenticated or request.user.is_superuser==False:
            return redirect('admin_login')

        products = Product.objects.all()
        categories = Category.objects.filter(is_available=True)
        product_count = products.count()
        brands = Brand.objects.all()
        activebrands = Brand.objects.filter(is_active = True)
        colour = Colour.objects.all()
        print(activebrands,"BRANDSSSS")
        
        context = {
            "products" : products,
            "product_count" : product_count,
            "categories" : categories,
            "brands" : brands,
            "colour":colour,
            "activebrands":activebrands, 
           
        }
        return render(request, "adminpanel/products_list.html",context)

@never_cache
@login_required(login_url='/signin')
def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        category_id = request.POST.get('product_category')
        new_arrival = request.POST.get('product_new_arrival')
        brand_id = request.POST.get('product_brand')
        product_description = request.POST.get('product_description')
        product_image = request.FILES.get('product_image')
        product_price = request.POST.get('product_price')
        category = get_object_or_404(Category, id=category_id)
        brand = get_object_or_404(Brand, id=brand_id)

        print(new_arrival,"newwwwwwwwwarrivalllll")
        
        product = Product(
            product_name=product_name,
            category=category,
            new_arrival=(new_arrival == '1'),  # Convert to boolean
            brand=brand,
            product_description=product_description,
            product_price = product_price,
        
            images=product_image
        )
        product.save()

        return redirect('product')  # Replace 'product' with the name of the view that displays the list of products
    categories = Category.objects.all()
    brands = Brand.objects.all()
    activebrands = Brand.objects.filter(is_active = True)
    return render(request, 'adminpanel/products_list.html', {'categories': categories, 'brands': brands,'activebrands':activebrands})

@never_cache
@login_required(login_url='signin')
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        brand_id = request.POST.get('brand')  
        category_id = request.POST.get('category') 
        new_arrival = request.POST.get('product_new_arrival')
        product_price = request.POST.get('product_price')
        product_stock = request.POST.get('product_stock')
        product_description = request.POST.get('product_description')

        print(new_arrival,"newwwwwwwwwarrivalllll")

        # Retrieve the updated 'images' field value
        product_thumbnail = request.FILES.get('product_images')
        print(product_thumbnail,"thumbbbbbbbbbbbbbbbbbb",product_price)

        # Update other product details
        product.product_name = product_name
        product.brand = get_object_or_404(Brand, id=brand_id)
        product.category = get_object_or_404(Category, id=category_id)
        if new_arrival == '1':
            product.new_arrival = True
        else:
            product.new_arrival = False
        product.product_price = product_price
        product.stock = product_stock
        product.description = product_description


        # Only update 'images' if a new file was provided
        if product_thumbnail:
            product.images = product_thumbnail

        # Save the updated product
        product.save()

        return redirect('product')

    return redirect('product')

never_cache
@login_required(login_url='signin')
def product_block(request,id):
    block = Product.objects.filter(id=id).update(is_available=False)
    return redirect("product")

@never_cache
@login_required(login_url='signin')
def product_unblock(request,id):
    un_block = Product.objects.filter(id=id).update(is_available=True)
    return redirect("product")


#category management
@never_cache
@login_required(login_url='signin')
def category(request):
    if not request.user.is_authenticated or request.user.is_superuser==False:
        return redirect('signin')
    categories = Category.objects.all()
    return render(request,"adminpanel/category.html",{'categories': categories})

def category_block(request,id):
    block = Category.objects.filter(id=id).update(is_available = False)
    return redirect("category")

def category_unblock(request,id):
    un_block = Category.objects.filter(id=id).update(is_available = True)
    return redirect("category")


@never_cache
@login_required(login_url='/signin')
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_description = request.POST.get('category_description')
        Is_available = request.POST.get('Is_available')
        productImage = request.FILES.get('productImage')
        category = Category.objects.create(
            category_name=category_name,
            description=category_description,
            category_image=productImage,
            is_available=Is_available
        )
        return redirect('category')

    return render(request, "adminpanel/category.html")

@never_cache
@login_required(login_url='/signin')
def edit_category(request, id):
    category = get_object_or_404(Category,id=id)
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_description = request.POST.get('category_description')
        category_thumbnail = request.FILES.get('category_images')


        category.category_name = category_name
        category.description = category_description

        if category_thumbnail:
            category.cat_image = category_thumbnail

        category.save()

        return redirect('category')    

    return render(request,"adminpanel/category.html")


# variant management
@never_cache
@login_required(login_url='signin')
def colour(request,id):
    if not request.user.is_authenticated or request.user.is_superuser==False:
        return redirect('signin')
    if request.method == 'POST':
        product_colour = request.POST.get('product_colour')
        colour_stock =request.POST.get('colour_stock')
        is_available = request.POST.get('colour_is_available')
        variant_image = request.FILES.get('variant_image')
        # variant_mrp = request.POST.get('variant_price')
        
       
        product = get_object_or_404(Product, id=id)
        colour = Colour.objects.create(  
            product = product,
            product_colour = product_colour,
            colour_stock = colour_stock,
            is_available = is_available,
            variant_image = variant_image,
            # variant_price = variant_mrp,
           
        )
        return redirect('product')

    return render(request,"adminpanel/product.html",{'colour':colour})

@never_cache
@login_required(login_url='signin')
def colour_details(request,id):
    colour = get_object_or_404(Colour, id=id)
    if request.method == 'POST':
        product_colour = request.POST.get('product_colour')
        colour_stock =request.POST.get('colour_stock')
        is_available = request.POST.get('colour_is_available')
        variant_image = request.FILES.get('variant_image')
        # variant_mrp = request.POST.get('variant_price')

        colour.product_colour = product_colour
        colour.colour_stock = colour_stock
        colour.is_available = is_available
        # variant.variant_price = variant_mrp

        if variant_image:
            colour.variant_image = variant_image

        colour.save()
        return redirect('product')


    return render(request,"adminpanel/product.html")

@never_cache
@login_required(login_url='signin')
def delete_colour(request, id):
    delete_colour = Colour.objects.filter(id=id)
    if delete_colour:
        delete_colour.delete()
        return redirect('product')
    return render(request,"adminpanel/product.html")

@never_cache
@login_required(login_url='signin')
def brand(request):
    if not request.user.is_authenticated or request.user.is_superuser==False:
        return redirect('signin')
    brands = Brand.objects.all()
    return render(request,"adminpanel/brands.html",{'brands': brands})

@never_cache
@login_required(login_url='/siginin')
def add_brand(request):
    if not request.user.is_authenticated or request.user.is_superuser == False:
        return redirect('signin')
    if request.method =='POST':
        brand_name = request.POST.get('brand_name')
        brands = Brand.objects.create(brand_name=brand_name)
        return redirect ('product')
    return render(request,'adminpanel/brands.html')

@never_cache
@login_required(login_url='signin')
def brand_block(request,brand_id):
    brand = Brand.objects.get(id=brand_id)
    brand.is_active = False
    brand.save()
    return redirect('product')

@never_cache
@login_required(login_url='signin')
def brand_unblock(request,brand_id):
    brand = Brand.objects.get(id=brand_id)
    brand.is_active = True
    brand.save()
    return redirect ('product')

@never_cache
@login_required(login_url='/signin')
def coupon(request):
    # if not request.user.is_authenticated or request.user.is_superuser==False:
    #    return redirect('signin')
    coupons = Coupon.objects.all() 
    return render(request,'adminpanel/coupon.html',{'coupons': coupons})

@never_cache
@login_required(login_url='/signin')
def add_coupon(request):
    if not request.user.is_authenticated or request.user.is_superuser==False:
       return redirect('signin')
    if request.method == 'POST':
        coupon_id =request.POST.get('coupon_id')
        Is_available = request.POST.get('Is_available')
        discount_price = request.POST.get('discount_price')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')
        coupon = Coupon.objects.create(
            code = coupon_id,
            is_active = Is_available,
            discount_price=discount_price,
            start_date=start_date,
            end_date=end_date,
            min_price=min_price,
            max_price=max_price,
        )
        return redirect('coupon')
    return render(request,'adminpanel/coupon.html')

@never_cache
@login_required(login_url='signin')
def coupon_block(request,coupon_id):
    if not request.user.is_authenticated or request.user.is_superuser==False:
       return redirect('signin')
    coupon = Coupon.objects.get(id=coupon_id)
    coupon.is_active=False
    coupon.save()
    return redirect('coupon')

@never_cache
@login_required(login_url='signin')
def coupon_unblock(request,coupon_id):
    if not request.user.is_authenticated or request.user.is_superuser==False:
       return redirect('signin')
    coupon = Coupon.objects.get(id=coupon_id)
    coupon.is_active=True
    coupon.save()
    return redirect('coupon')

@never_cache
@login_required(login_url='/signin')
def manage_order(request):
    if not request.user.is_authenticated or request.user.is_superuser==False:
        return redirect('signin')
    orders = Order.objects.all().order_by('-id')
    print(orders,"ORDERSS")
    statuses =Order.STATUS

    context = {
        'orders' : orders,
        'statuses' : statuses,
    
    }
    return render(request, 'adminpanel/order.html',context)

@never_cache
@login_required(login_url='signin')
def manage_orderstatus(request,id):
    order = get_object_or_404(Order,id=id)
    if request.method =='POST':
        order_status = request.POST.get('status')
        order_status = order_status
        order.save()
        return redirect('manage_order')
    return render(request,'adminpanel/order.html')

@never_cache
@login_required(login_url='signin')
def sales_report(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('signin')
    
    sales_report = Order.objects.all().order_by('id')

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if start_date and end_date:
            # Convert the date strings to datetime objects
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        
            # Filter orders based on the created_date field
            sales_report = sales_report.filter(created_at__range=(start_date, end_date))
        else:
            sales_report = Order.objects.all().order_by('id')


    context = {
        'sales_report': sales_report
    }
    return render(request, "adminpanel/sales_report.html", context)

    
# @never_cache
# @login_required(login_url='/signin')
# def add_product(request):
#     if request.method == 'POST':
#         product_name = request.POST.get('product_title')
#         product_description = request.POST.get('product_description')
#         product_code = request.POST.get('product_code')
#         regular_price = request.POST.get('regular_price')
#         quantity = request.POST.get('quantity')
#         regular_size = request.POST.get('regular_size')
#         brand_id = request.POST.get('brand')
#         width = request.POST.get('width')
#         height = request.POST.get('height')
#         weight = request.POST.get('weight')
#         product_image = request.FILES.get('product_image')
#         category_name = request.POST.get('category')
#         sub_category_name = request.POST.get('sub_category')
#         product_colour = request.POST.get('product_colour')

#         # Check for required fields
#         if not (product_title and regular_price and quantity and product_image and category_name and sub_category_name and product_code):
#             messages.error(request, 'Please fill in all required fields.')
#             return redirect('adminpanel/add_product')  # Redirect to the same page to correct errors.

#         try:
#             regular_size, _ = get_object_or_404(Size, regular_size=regular_size)
#             brand_name, _ = get_object_or_404(Brand, id=brand_id)
#             category, _ = get_object_or_404(Category, category_name=category_name)
#             sub_category, _ = get_object_or_404(Sub_category, sub_category_name=sub_category_name, category=category)
#             product_colour, _ = get_object_or_404(Colour, product_colour=product_colour)

#             product = Product(
#                 product_title=product_title,
#                 product_description=product_description,
#                 product_code=product_code,
#                 regular_price=regular_price,
#                 quantity=quantity,
#                 available_sizes=regular_size,
#                 brand_name=brand_id,
#                 width=width,
#                 height=height,
#                 weight=weight,
#                 product_image=product_image,
#                 category=category_name,
#                 sub_category=sub_category_name,
#                 available_colours=product_colour,
#             )
#             product.save()
#             messages.success(request, 'Product added successfully!')

#             return redirect('product_view')  # Redirect to the home page after a successful addition.

#         except Exception as e:
#             messages.error(request, f'An error occurred: {str(e)}')
#             return redirect('add_product')  # Redirect back to the form with an error message.

#     # If it's not a POST request, render the form.
#     categories = Category.objects.all()
#     sub_categories = Sub_category.objects.all()
#     brands = Brand.objects.all()
#     sizes = Size.objects.all()
#     colours = Colour.objects.all()
#     return render(request, 'adminpanel/add_product.html',{
#         'categories': categories,
#         'sub_categories': sub_categories,
#         'brands': brands,
#         'sizes': sizes,
#         'colours' : colours,
#     })




@login_required
@login_required(login_url='/signin')
def product_view(request):
    if not request.user.is_authenticated or request.user.is_superuser==False:
        return redirect('signin')
    products = Product.objects.all()
    context = {
        'products' : products,
    }
    return render(request,'adminpanel/product_view.html',context)



# def update_product(request, product_id):
#     products = get_object_or_404(Product, id=product_id)
#     categories = Category.objects.all()
#     brands = Brand.objects.all()
#     sub_categories = Sub_category.objects.all()
#     sizes = Size.objects.all()
#     colours = Colour.objects.all()

#     if request.method =='POST':
#         edited_product_title= request.POST.get('product_title')
#         edited_product_description = request.POST.get('product_description')
#         edited_product_code = request.POST.get('product_code')
#         regular_price = request.POST.get('regular_price')
#         quantity = request.POST.get('quantity')
#         regular_size = request.POST.get('size')
#         brand_id = request.POST.get('brand')
#         width = request.POST.get('width')
#         height = request.POST.get('height')
#         weight = request.POST.get('weight')
#         product_image = request.FILES.get('product_image')
#         category_name = request.POST.get('category')
#         sub_category_name = request.POST.get('sub_category')
#         product_colour = request. POST.get('product_colour')
#         categories = Category.objects.get(id=category_name)
#         brands = Brand.objects.get(id=brand_id)
#         sub_categories = Sub_category.objects.get(id=sub_category_name)
#         sizes = Size.objects.get(id=regular_size)
#         colours = Colour.objects.get(id=product_colour)
#         print(colours,"COLOURSSSSSSSSSS")
#         print(sizes,"SSSSSSSSSSSSSSSSSSSSS")
#         print(product_image,"PPPPPPP")
    
#         print(edited_product_title,"TITLEE")
#         print(regular_size, "SIZEEEE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#         print(quantity,"QUANTITYYY")
#         print(category_name,"CATEGORYYYYY")
#         print(category_name,"CATEGORYYYYY")
#         print(category_name,"CATEGORYYYYY")
        

#         products.product_title = edited_product_title
#         products.product_description =edited_product_description
#         products.product_code = edited_product_code
#         products.regular_price = regular_price
#         products.quantity = quantity
#         products.size = sizes
#         products.brand_name = brands
#         products.width = width
#         products.height = height
#         products.weight= weight
#         products.product_image = product_image
#         products.category = categories
#         products.sub_category = sub_categories
#         products.colour = colours
#         products.save()
#         return redirect('product_view')


#     context = {
#         'products': products,
#         'categories': categories,
#         'brands': brands,
#         'sub_categories': sub_categories,
#         'sizes': sizes,
#         'colours': colours
#     }

#     return render(request, 'adminpanel/update_product.html', context)



# def product_block(request,id):
#     block = Product.objects.filter(id=id).update(is_available = False)
#     return redirect(product_view)

# def product_unblock(request,id):
#     block = Product.objects.filter(id=id).update(is_available= True)
#     return redirect(product_view)

# def product_filter(request):
#     # Fetch all available filter options from your database
#     sizes = Size.objects.all()
#     colours = Colour.objects.all()
#     categories = Category.objects.all()
#     subcategories = Sub_category.objects.all()
#     brands = Brand.objects.all()

#     # Initialize a queryset with all products
#     filtered_products = Product.objects.all()

#     # Filter based on selected options

#     # Size filter
#     selected_size = request.GET.get('size')
#     if selected_size:
#         filtered_products = filtered_products.filter(size__regular_size=selected_size)

#     # Color filter
#     selected_colour = request.GET.get('colour')
#     if selected_colour:
#         filtered_products = filtered_products.filter(colour__colour=selected_colour)

#     # Category filter
#     selected_category = request.GET.get('category')
#     if selected_category:
#         filtered_products = filtered_products.filter(category__id=selected_category)

#     # Subcategory filter
#     selected_subcategory = request.GET.get('subcategory')
#     if selected_subcategory:
#         filtered_products = filtered_products.filter(sub_category__id=selected_subcategory)

#     # Brand filter
#     selected_brand = request.GET.get('brand')
#     if selected_brand:
#         filtered_products = filtered_products.filter(brand_name__id=selected_brand)

#     # Pass the filtered products and filter options to your template
#     context = {
#         'filtered_products': filtered_products,
#         'sizes': sizes,
#         'colours': colours,
#         'categories': categories,
#         'subcategories': subcategories,
#         'brands': brands,
#     }

#     return render(request, 'adminpanel/shop.html', context)

# # @never_cache
# # @login_required(login_url='/signin')
# def category_view(request):
#     categories = Category.objects.all()

#     if request.method == 'POST':
#         if 'add_category' in request.POST:
#             # Handle adding a new category
#             category_name = request.POST.get('category_name')
#             category_title = request.POST.get('category_title')
#             description = request.POST.get('description')
#             category_image = request.FILES.get('category_image')

#             category = Category(
#                 category_name=category_name,
#                 category_title=category_title,
#                 description=description,
#                 category_image=category_image
#             )
#             category.save()
#             messages.success(request, 'Category added successfully.')
            
            
#         elif 'edit_category' in request.POST:
#             # Handle editing an existing category
#             category_id = request.POST.get('edit_category')
#             category = get_object_or_404(Category, id=category_id)
#             category.category_name = request.POST.get('category_name')
#             category.category_title = request.POST.get('category_title')
#             category.description = request.POST.get('description')
#             category.category_image = request.FILES.get('category_image')
#             category.save()
#             print(category,"SAVEDDDD")
#             messages.success(request, 'Category has been sucessfully updated.')
#             d=Category.objects.get(id=category_id)
#             context = {"d":d}
#             return render(request,'adminpanel/category.html',context)
            
#         elif 'delete_category' in request.POST:
#             # Handle deleting a category
#             category_id = request.POST.get('delete_category')
#             category = get_object_or_404(Category, id=category_id)
#             category.delete()
#         return redirect('category_view')

#     return render(request, 'adminpanel/category.html', {'categories': categories})


# @never_cache
# @login_required(login_url='/signin')
# def sub_category_view(request):
#     sub_categories = Sub_category.objects.all()
#     categories = Category.objects.values('category_name').distinct()
#     category = None
#     if request.method == 'POST':
#         if 'create_sub_category' in request.POST:
#             # Handle adding a new category
#             sub_category_name = request.POST.get('sub_category_name')
#             sub_category_title = request.POST.get('sub_category_title')
#             sub_category_description = request.POST.get('sub_category_description')
#             print("sub category_description:", sub_category_description)
#             category_id = request.POST.get('category')
#             print(category_id,"Categoryyyyyyyy")
#             if category_id and category_id.isnumeric():
#                 category_id = int(category_id)
#                 category = Category.objects.get(id=category_id)
#                 print(category,"Categoryyyyyyyy")

      
#                 Sub_category.objects.create(
#                     sub_category_name=sub_category_name,
#                     sub_category_title=sub_category_title,
#                     sub_category_description=sub_category_description,
#                     category_id=category
#                 )
#                 messages.success(request, 'Sub Category added successfully.')
                
#         elif 'edit_sub_category' in request.POST:
#             # Handle editing an existing category
#             sub_category_id = request.POST.get('edit_sub_category')
#             sub_category = get_object_or_404(Sub_category, id=sub_category_id)
#             sub_category.sub_category_name = request.POST.get('sub_category_name')
#             sub_category.sub_category_title = request.POST.get('sub_category_title')
#             sub_category.sub_category_description = request.POST.get('sub_category_description')
#             sub_category.category=request.POST.get('category')
#             sub_category.save()
#             print(sub_category,"SAVEDDDD")
#             messages.success(request, 'Sub Category has been sucessfully updated.')
#             d=Sub_category.objects.get(id=sub_category_id)
#             context = {"d":d}
#             return render(request,'adminpanel/sub_category.html',context)
            
#         elif 'delete_sub_category' in request.POST:
#             # Handle deleting a category
#             sub_category_id = request.POST.get('delete_sub_category')
#             sub_category = get_object_or_404(Sub_category, id=sub_category_id)
#             sub_category.delete()
#         return redirect('sub_category_view')

#     return render(request, 'adminpanel/sub_category.html', {'sub_categories': sub_categories, 'categories':categories})


# @never_cache
# @login_required(login_url='/signin')
# def brand_view(request):
#     brands = Brand.objects.all()

#     if request.method == 'POST':
#         if 'create_brand' in request.POST:
#             # Handle adding a new category
#             brand_name = request.POST.get('brand_name')
#             quantity = request.POST.get('quantity')
#             description = request.POST.get('description')
#             logo = request.FILES.get('brand_image')
#             Brand.objects.create(
#                 brand_name=brand_name,
#                 quantity=quantity,
#                 description=description,
#                 logo=logo
#             )
#             messages.success(request, 'Brand added successfully.')
            
#         elif 'edit_brand' in request.POST:
#             # Handle editing an existing brand
#             brand_id = request.POST.get('edit_brand')
#             brand = get_object_or_404(Brand, id=brand_id)
#             brand.brand_name = request.POST.get('brand_name')
#             brand.quantity = request.POST.get('quantity')
#             brand.description = request.POST.get('description')
#             brand.logo = request.FILES.get('logo')
#             brand.save()
#             print(brand,"SAVEDDDD")
#             messages.success(request, 'Brand has been sucessfully updated.')
#             d=Brand.objects.get(id=brand_id)
#             context = {"d":d}
#             return render(request,'adminpanel/brand_view.html',context)
            
#         elif 'delete_brand' in request.POST:
#             # Handle deleting a brand
#             brand_id = request.POST.get('delete_brand')
#             brand = get_object_or_404(Brand, id=brand_id)
#             brand.delete()
#         return redirect('brand_view')

#     return render(request, 'adminpanel/brand_view.html', {'brands': brands})

