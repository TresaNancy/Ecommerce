from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .models import Product,Category,Brand,Sub_category,Size,Colour
from django.contrib import messages

# Create your views here.
@never_cache
@login_required(login_url='/signin')
def dashboard(request):
    return render(request,'adminpanel/dashboard.html')




@never_cache
@login_required(login_url='/signin')
def add_product(request):
    if request.method == 'POST':
        product_title = request.POST.get('product_title')
        product_description = request.POST.get('product_description')
        regular_price = request.POST.get('regular_price')
        quantity = request.POST.get('quantity')
        regular_size = request.POST.get('regular_size')
        brand_id = request.POST.get('brand')
        width = request.POST.get('width')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        product_image = request.FILES.get('product_image')
        category_name = request.POST.get('category')
        sub_category_name = request.POST.get('sub_category')
        colour = request. POST.get('colour')

        # Check for required fields
        if not (product_title and regular_price and quantity and product_image and category_name and sub_category_name):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('adminpanel/add_product')  # Redirect to the same page to correct errors.

        try:
            regular_size, _ = Size.objects.get_or_create(regular_size=regular_size)
            brand_name, _ = Brand.objects.get_or_create(id=brand_id)

            category, _ = Category.objects.get_or_create(category_name=category_name)
            sub_category, _ = Sub_category.objects.get_or_create(sub_category_name=sub_category_name, category=category)
            colour,_ = Colour.objects.get_or_create(colour=colour)

            product = Product(
                product_title=product_title,
                product_description=product_description,
                regular_price=regular_price,
                quantity=quantity,
                size=regular_size,
                brand_name=brand_name,
                width=width,
                height=height,
                weight=weight,
                product_image=product_image,
                category=category,
                sub_category=sub_category,
                colour = colour
            )
            product.save()
            messages.success(request, 'Product added successfully!')

            return redirect('shop')  # Redirect to the home page after a successful addition.

        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('add_product')  # Redirect back to the form with an error message.

    # If it's not a POST request, render the form.
    categories = Category.objects.all()
    sub_categories = Sub_category.objects.all()
    brands = Brand.objects.all()
    sizes = Size.objects.all()
    colours = Colour.objects.all()
    return render(request, 'adminpanel/add_product.html', {
        'categories': categories,
        'sub_categories': sub_categories,
        'brands': brands,
        'sizes': sizes,
        'colours' : colours,
    })

def product_filter(request):
    # Fetch all available filter options from your database
    sizes = Size.objects.all()
    colours = Colour.objects.all()
    categories = Category.objects.all()
    subcategories = Sub_category.objects.all()
    brands = Brand.objects.all()

    # Initialize a queryset with all products
    filtered_products = Product.objects.all()

    # Filter based on selected options

    # Size filter
    selected_size = request.GET.get('size')
    if selected_size:
        filtered_products = filtered_products.filter(size__regular_size=selected_size)

    # Color filter
    selected_colour = request.GET.get('colour')
    if selected_colour:
        filtered_products = filtered_products.filter(colour__colour=selected_colour)

    # Category filter
    selected_category = request.GET.get('category')
    if selected_category:
        filtered_products = filtered_products.filter(category__id=selected_category)

    # Subcategory filter
    selected_subcategory = request.GET.get('subcategory')
    if selected_subcategory:
        filtered_products = filtered_products.filter(sub_category__id=selected_subcategory)

    # Brand filter
    selected_brand = request.GET.get('brand')
    if selected_brand:
        filtered_products = filtered_products.filter(brand_name__id=selected_brand)

    # Pass the filtered products and filter options to your template
    context = {
        'filtered_products': filtered_products,
        'sizes': sizes,
        'colours': colours,
        'categories': categories,
        'subcategories': subcategories,
        'brands': brands,
    }

    return render(request, 'adminpanel/shop.html', context)


def account_register(request):
    return render(request,'adminpanel/account_register.html')

def brands(request):
    return render(request,'adminpanel/brands.html')

def categories(request):
    return render(request,'adminpanel/categories.html')

def error_404(request):
    return render(request,'adminpanel/error_404.html')


def form_product_2(request):
    return render(request,'adminpanel/form_product_2.html')

def form_product_3(request):
    return render(request,'adminpanel/form_product_3.html')

def form_product_4(request):
    return render(request,'adminpanel/form_product_4.html')

def orders_1(request):
    return render(request,'adminpanel/orders_1.html')

def orders_2(request):
    return render(request,'adminpanel/orders_2.html')

def products_grid(request):
    return render(request,'adminpanel/products_grid.html')

def products_grid_2(request):
    return render(request,'adminpanel/products_grid_2.html')

def products_list(request):
    return render(request,'adminpanel/products_list.html')

def reviews(request):
    return render(request,'adminpanel/reviews.html')

def seller_detail(request):
    return render(request,'adminpanel/seller_detail.html')

def settings_1(request):
    return render(request,'adminpanel/settings_1.html')

def settings_2(request):
    return render(request,'adminpanel/settings_2.html')

def transactions_1(request):
    return render(request,'adminpanel/transactions_1.html')

def transactions_2(request):
    return render(request,'adminpanel/transactions_2.html')

def sellers_cards(request):
    return render(request,'adminpanel/sellers_cards.html')

def sellers_list(request):
    return render(request,'adminpanel/sellers_list.html')

def orders_detail(request):
    return render(request,'adminpanel/orders_detail.html')