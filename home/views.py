from django.shortcuts import render,get_object_or_404
from adminpanel.models import *
from cart.models import *
from django.views. decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.mail import send_mail
from .forms import ContactForm


# Create your views here.
@never_cache
def index(request):
    categories = Category.objects.filter(is_available = True)[:8]
    products = Product.objects.filter(is_available = True).order_by('-modified_date')[:8]
    context = {
        'categories' : categories,
        'products': products
    }

    return render(request,'home/index.html',context)
    
    

@never_cache
@login_required(login_url='signin')
def checkout(request):
    return render(request,'home/checkout.html')

@never_cache
@login_required(login_url='signin')
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Sending email
            send_mail(
                subject,
                f"From: {name}\nEmail: {email}\n\n{message}",
                email,
                ['explorejunction091@gmail.com'],
                fail_silently=False,
            )
            # Redirect after successful form submission
            # You can redirect to a success page or home page
            return render(request, 'home/contact_success.html')
    else:
        form = ContactForm()

    return render(request, 'home/contact.html', {'form': form})
   


@never_cache
@login_required(login_url='signin')
def product_details(request,id):
    single_product = Product.objects.get(id=id)
    print(single_product,"single producttttttttttttttttttttttttttttttttttt")
    colour = Colour.objects.filter(product=id, is_available = True)
    print(colour,"sollllllllllrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")

    wishlist = Wishlist.objects.all()
    print(wishlist,"9999909990990990909")
    print(single_product.id,"0000000000000000000")
  # Create a list of variant IDs in the wishlist
    wishlist_colour_ids = [item.colour.id for item in wishlist]
    

    context = {
        'single_product': single_product,
        'colour': colour,
        'wishlist_colour_ids': wishlist_colour_ids,
    }
    return render(request, 'home/product_detail.html', context)


@never_cache
@login_required(login_url='signin')
def shop(request):
    products = Product.objects.filter(is_available=True)
    colours = Colour.objects.all()
    brands = Brand.objects.all()
    # categoreis = Category.objects.all()

    selected_colors = request.GET.getlist('color')
    selected_prices = request.GET.getlist('price')
    selected_brands = request.GET.getlist('brand')
    # selected_categories = request.GET.getlist('category')

    if selected_colors:
        products = products.filter(colour__product_colour__in=selected_colors)

    if selected_brands:
        products = products.filter(brand__in=selected_brands)

    # if selected_categories:
    #     products = products.filter(category__in=selected_categories)

    price_ranges = [
        (0, 500),
        (500, 1000),
        (1000, 2000),
        (2000, 3000),
        (3000, 4000),
        (4000, 5000),
        (5000, None),
    ]

    if selected_prices:
        price_filters = Q()
        for price_range in selected_prices:
            min_price, max_price = price_ranges[int(price_range) - 1]
            if max_price is not None:
                price_filters |= Q(product_price__gte=min_price, product_price__lt=max_price)
            else:
                price_filters |= Q(product_price__gte=min_price)
        products = products.filter(price_filters)

    distinct_colors = set(colours.values_list('product_colour', flat=True))
    distinct_brands = brands  # Pass the 'brands' queryset directly
    # distinct_categories = categoreis

    context = {
        'products': products,
        'colours': distinct_colors,
        'brands': distinct_brands,  # Pass 'distinct_brands' instead of 'set(brands.values_list('brand_name', flat=True))'
        # 'categories' : distinct_categories,
        # 'selected_categories' : selected_categories,
        'selected_colors': selected_colors,
        'selected_brands': selected_brands,
        'price_ranges': price_ranges,
        'selected_prices': selected_prices,
    }
    return render(request, 'home/shop.html', context)




# def shop(request):
#     products = Product.objects.filter(is_available=True)
#     colours = Colour.objects.all()
#     brands = Brand.objects.all()

#     selected_colors = request.GET.getlist('color')
#     selected_prices = request.GET.getlist('price')  # Retrieve selected price ranges
#     selected_brands = request.GET.getlist('brand')

#     if selected_colors:
#         products = products.filter(colour__product_colour__in=selected_colors)

#     if selected_brands:
#         products = products.filter(brand__in=selected_brands)

#     price_ranges = [
#         (0, 500),
#         (500, 1000),
#         (1000, 2000),
#         (2000, 3000),
#         (3000, 4000),
#         (4000, 5000),
#         (5000, None),  # Use None instead of infinity for the last range
#     ]

#     selected_prices = request.GET.getlist('price')

#     if selected_colors:
#         products = products.filter(colour__product_colour__in=selected_colors)

#     # Filter products based on selected price ranges
#     if selected_prices:
#         price_filters = Q()
#         for price_range in selected_prices:
#             min_price, max_price = price_ranges[int(price_range) - 1]  # Adjust index to match template numbering
#             if max_price is not None:
#                 price_filters |= Q(product_price__gte=min_price, product_price__lt=max_price)
#             else:
#                 price_filters |= Q(product_price__gte=min_price)
#         products = products.filter(price_filters)


#     distinct_colors = set(colours.values_list('product_colour', flat=True))
#     distinct_brands = set(brands.values_list('brand_name', flat=True))

#     context = {
#         'products': products,
#         'colours': distinct_colors,
#         'selected_colors': selected_colors,
#         'price_ranges': price_ranges,
#         'selected_brands': selected_brands,
#         'selected_prices': selected_prices,
#     }
#     return render(request, 'home/shop.html', context)
