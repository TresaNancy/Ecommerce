from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from adminpanel.models import *
from .models import *
from django.contrib import messages
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from user.models import Profile
from decimal import Decimal
from django.db.models import Q
from orders.models import Order
from django.db.models import F
from django.views.decorators.cache import never_cache


# Create your views here.
@never_cache
@login_required(login_url='signin')
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart    


@never_cache
@login_required(login_url='signin')
def cart(request, total=0, quantity=0, cart_items=None):
    colours = Colour.objects.all()
    list = []
    for colour in colours:
        if colour.colour_stock < 1:     
            list.append(colour.id)
    print(list,"out of stock")
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:   
            cart = Cart.objects.get(cart_id=_cart_id(request))
            print(cart,'222222222222222222')                             
            cart_items = CartItem.objects.filter(cart=cart)
            # print(cart_items,"1111111111111111111")
        for cart_item in cart_items:
            total += (cart_item.product.product_price * cart_item.quantity)
            print(total,"TOTAL...")
            quantity += cart_item.quantity
            
            if cart_item.colour.colour_stock == 0:
                cart_item.is_active = False
                cart_item.save()
                total = total-(cart_item.product.product_price * cart_item.quantity)
        tax = (2*total)/100
        grand_total = total + tax    
    except ObjectDoesNotExist:
        pass # just ignore
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax':tax,
        'grand_total':grand_total,
        'list':list,
    }         
    return render(request, 'home/cart.html', context)

# views.py
@never_cache
@login_required(login_url='signin')
def wishlist_to_cart(request, product_id, colour_id):
    print(colour_id,"varianttttttttttttt in wishlis")
    # request.session['wishlist_variant_id'] = variant_id
    # return redirect('add_to_cart', product_id=product_id)
    colour = Colour.objects.get(id=colour_id)
    cart = CartItem.objects.create
    current_user = request.user
    product = Product.objects.get(id=product_id)


    try:
        get_product = CartItem.objects.get(product=product)
        cart_quantity = get_product.quantity
    except:
        cart_quantity = 0

    if current_user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id = current_user, user = current_user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = current_user, user = current_user)
        try:
            cart_item = CartItem.objects.get(product=product, user=current_user, colour=colour, cart = cart)
            cart_item.quantity += 1  
            cart_item.cart_price = product.product_price*cart_item.quantity  
            print(cart_item.cart_price,"9999999999999999")
            cart_item.save()
            messages.success(request,"The item is already in your cart, and the quantity of the cart item has been increased")

            if request.user.is_authenticated:
                wishlist_item = Wishlist.objects.get(colour = colour_id, user=request.user)
                wishlist_item.delete()


        except CartItem.DoesNotExist:
            cart_item =CartItem.objects.create(product =product,quantity =+ 1,user=current_user,colour=colour,cart=cart, cart_price=product.product_price)
            cart_item.save()

            if request.user.is_authenticated:
                wishlist_item = Wishlist.objects.get(colour = colour_id, user=request.user)
                wishlist_item.delete()


            messages.success(request,"The item has been successfully added to your cart")
        return redirect("wishlist") 
    
    return redirect("wishlist")
    
    

@never_cache 
@login_required(login_url='signin')
def add_to_cart(request,product_id,colour=0):
    print(product_id,"product_idddddddddddddd")
    colour_id_from_session = request.session.get('wishlist_colour_id')
    print(colour_id_from_session,"sessiion value color id")
    product = Product.objects.get(id=product_id)
    colour_id = request.POST.get('colour')  
    print(colour_id,"color iddddddd from variant html")
    # quantity = int(request.POST.get('quantity'))  
    action = request.POST.get('action')
    print(action,"actionnnnnnnnn")
    current_user = request.user
    if colour_id:
        try:
            colour = Colour.objects.get(id=colour_id)
        except Colour.DoesNotExist:
            pass
    elif colour_id_from_session:
        try:
            colour = Colour.objects.get(id=colour_id_from_session)
        except Colour.DoesNotExist:
            pass
    print(colour,"variant in cartttttttttttttttt")
    

    if action == 'Add to Cart' or action == None:
        print("add to carttttttttttt")
        if action == None:
            print(colour,colour_id,"OLOURRR")
            # wishlist = Wishlist.objects.get(colour=colour)
            # wishlist.delete()
        print("add_to_cart")
        try:
            get_product = CartItem.objects.get(product=product)
            cart_quantity = get_product.quantity
        except:
            cart_quantity = 0

        if current_user.is_authenticated:
            try:
                cart = Cart.objects.get(cart_id = current_user, user = current_user)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(cart_id = current_user, user = current_user)
            try:
                cart_item = CartItem.objects.get(product=product, user=current_user, colour=colour, cart = cart)
                # cart_item.quantity += 1  
                cart_item.quantity = F('quantity') + 1  # Increase the quantity by 1
                cart_item.cart_price = product.product_price*cart_item.quantity  
                print(cart_item.cart_price,"9999999999999999")
                cart_item.save()
                return redirect('cart')
                messages.success(request,"The item is already in your cart, and the quantity of the cart item has been increased")

            except CartItem.DoesNotExist:
                cart_item =CartItem.objects.create(product =product,quantity =+ 1,user=current_user,colour=colour,cart=cart, cart_price=product.product_price)
                cart_item.save()
                return redirect('cart')
                messages.success(request,"The item has been successfully added to your cart")
            return redirect("product_details", product_id) 
        else:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request)) 
            except Cart.DoesNotExist:
                cart = Cart.objects.create( cart_id = _cart_id(request))
            cart.save()
            try:
                cart_item = CartItem.objects.get(product=product, cart = cart, colour=colour)
                cart_item.quantity += 1 
                cart_item.cart_price = product.product_price*cart_item.quantity         
                cart_item.save()
                messages.success(request,"The item is already in your cart, and the quantity of the cart item has been increased")
            except CartItem.DoesNotExist:
                cart_item =CartItem.objects.create(product =product,quantity = cart_quantity+1,cart =cart ,colour=colour, cart_price=product.product_price)
                cart_item.save()
                return redirect('cart')
                messages.success(request,"The item has been successfully added to your cart")
        return redirect("product_details", product_id)
    elif action == 'Add to Wishlist':
        print("add to wishlist")
        return redirect('add_to_wishlist', colour_id=colour.id)
    else:
        return redirect('product_details', productid=product_id)
  
@never_cache
@login_required(login_url='signin')
def update_quantity(request, updated_price=0,new_updated_price=0):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        print(item_id,"itemmmmmmmmmmmmmm")
        change = int(request.POST.get('change'))
        print(change,"changeeeeeeeeeeeee")
        cart_item = CartItem.objects.get(id=item_id)
        product = cart_item.product
        colour = cart_item.colour
      

        if change == -1:
            if cart_item.quantity > 1:
                cart_item.quantity += change
                cart_item.cart_price -= product.product_price
            else:
                pass

            
        elif change == 1:
            if cart_item.colour.colour_stock > cart_item.quantity:
                cart_item.quantity += change
                cart_item.cart_price += product.product_price
            else:
                pass
        else:
            pass
        cart_item.save()

        new_price = CartItem.objects.get(id=item_id)
        new_updated_price = new_price.cart_price


        current_user = request.user
        if current_user.is_authenticated:
            cart = Cart.objects.get(cart_id = current_user, user = current_user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request)) 

        cart_items = CartItem.objects.filter(cart = cart)
        
        for cart in cart_items:
            updated_price += cart.cart_price

        # updated_price = cart_item.cart_price
        updated_quantity = cart_item.quantity

        tax = (2*updated_price)/100
        grand_total = updated_price + tax
        print(grand_total,"granddddddddddd")
        return JsonResponse({'updated_quantity': updated_quantity, 'updated_price': new_updated_price, 'tax':tax, 'grand_total':grand_total})
    else:
        return JsonResponse({'error': 'Invalid request method.'})
                
@never_cache
@login_required(login_url='signin')
def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)

    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

@never_cache
@login_required(login_url='signin')
def checkout(request,total=0, quantity=0, coupon_amount=0, coupon_id = 0, cart_item=None):
    address_count = Profile.objects.filter(user=request.user).count()
        
    if address_count<1:
        return redirect('change_address')
    else:
        try:
            tax = 0
            grand_total = 0
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            else:   
                cart = Cart.objects.get(cart_id=_cart_id(request))
                print(cart,'222222222222222222')
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)
                print(cart_items,"1111111111111111111")
            for cart_item in cart_items:
                total += (Decimal(cart_item.product.product_price) * cart_item.quantity)
                quantity += cart_item.quantity

                if cart_item.colour.colour_stock == 0:
                    total -= Decimal(cart_item.product.product_price)

            # tax = (2*total)/100
            tax = (Decimal('0.02') * total)
            grand_total = total + tax    
        except ObjectDoesNotExist:
            pass # just ignore
        try:
            address = Profile.objects.get(user=request.user, set_default=True)
        except:
            address = Profile.objects.get(user=request.user)
            address.set_default = True
            address.save()
        total_address = Profile.objects.filter(user=request.user).count()

        if request.method == 'POST':
            print("haiiiiiiiiiiiii")
            couponcode = request.POST.get('CouponCode')
            print(couponcode, "its coupon code")

            try:
                exist_coupon = Coupon.objects.get(code=couponcode)
                print(exist_coupon,"exitttttttttttt")
                
                # Check if the coupon is active
                if not exist_coupon.is_active:
                    messages.info(request, "This coupon is not currently active.")
                
                # Check if the coupon has expired
                current_date = datetime.now().date()
                if current_date < exist_coupon.start_date:
                    messages.info(request, "This coupon is not yet valid.")
                elif current_date > exist_coupon.end_date:
                    messages.info(request, "This coupon has expired.")
                
                if grand_total < exist_coupon.min_price:
                    messages.info(request,"Parchase more for applay this coupon.")
                elif grand_total > exist_coupon.max_price:
                    messages.info(request,"This coupon is not applaied for the price range")
                else:
                    grand_total = grand_total - exist_coupon.discount_price
                    coupon_amount = exist_coupon.discount_price
                    messages.success(request,"coupon applied successfulley")
                    print(coupon_amount,"settttttttttttttt")
                    coupon_id = exist_coupon.id
                    print(coupon_id,"carttttttttttcouponid")

            
            except Coupon.DoesNotExist:
                messages.info(request, "The entered coupon code is not valid")
        else:
            pass



        coupons = Coupon.objects.filter(
            Q(min_price__lt=grand_total) & Q(max_price__gt=grand_total)
        )

        orders = Order.objects.filter(user=request.user)
        unused_coupons = []

        for coupon in coupons:
            coupon_used = False
            for order in orders:
                if order.coupon == coupon:
                    coupon_used = True
                    break  # No need to check other orders if coupon is found in one
            if not coupon_used:
                unused_coupons.append(coupon)

        if total == 0:
            return redirect('shop')
        context = {
            'total' : total,
            'quantity' : quantity,
            'cart_items' : cart_items,
            'tax':tax,
            'grand_total':grand_total,
            'address':address,
            'total_address' : total_address,
            'coupon_amount' : coupon_amount,
            'coupon_id': coupon_id,
            'coupons' : unused_coupons,
        }
        # print(context,"''''''''''''''''''''")
    return render(request, 'home/checkout.html', context)

@never_cache
@login_required(login_url='signin')
def wishlist(request):
    wishlists = Wishlist.objects.all()
    bool = True
    context = {
        'wishlists': wishlists,
        'show_footer' : bool,
    }
    return render(request,'cart/wishlist.html', context)


@never_cache
@login_required(login_url='signin')
def add_to_wishlist(request, colour_id):
    colour = get_object_or_404(Colour, id=colour_id)
    product = colour.product
    wishlist_entry = Wishlist.objects.filter(user=request.user, colour=colour).first()
    if wishlist_entry:
        messages.info(request,"Product already in wishlist")
        # return JsonResponse({'message': 'Product already in wishlist'}, status=400)
        return redirect('shop')
        
    else:
        Wishlist.objects.create(
            product=product,
            colour=colour,
            user=request.user,
        )
        # return JsonResponse({'message': 'Product added to Wishlist'}, status=200)
        return redirect('wishlist')
    # return redirect('product_details',productid=product.id)



@never_cache
@login_required(login_url='signin')
def remove_wishlist_item(request, product_id, wishlist_id):
    # Retrieve the product object
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        try:
            # Attempt to get the wishlist item for the authenticated user
            wishlist_item = Wishlist.objects.get(product=product, user=request.user, id=wishlist_id)
            wishlist_item.delete()
            
            # Notify the user upon successful deletion
            messages.success(request, 'Item removed from wishlist successfully.')
        except Wishlist.DoesNotExist:
            # Handle the case when the Wishlist item does not exist
            messages.error(request, 'The selected item does not exist in the wishlist.')
        except Exception as e:
            # Handle any other unexpected exceptions gracefully
            messages.error(request, f'An error occurred: {str(e)}')
    else:
        # Redirect to login if the user is not authenticated
        messages.info(request, 'Please login to remove items from the wishlist.')
        return redirect('login')  # Update 'login' to your actual login URL

    return redirect('wishlist')



# # Create your views here.
# @never_cache
# @login_required(login_url='signin')
# def cart(request, total_price = 0):
#     cart_items = Cart.objects.filter(user = request.user).order_by('id')
#     for cart in cart_items:
#         total_price += cart.price*cart.quantity
    
#     context = {
#         'cart_items': cart_items,
#         'total_price':total_price
#     }
#     return render(request,'home/cart.html',context)


# @never_cache
# @login_required(login_url='signin')
# def add_to_cart(request,id):
#     if request.method == 'POST':
#         user = request.user
#         size_id = request.POST.get('size')
#         colour_id = request.POST.get('product_colour')
#         size = get_object_or_404(Size, id=size_id)
#         colour = get_object_or_404(Colour, id=colour_id)
#         quantity = request.POST.get('quantity')
      
#         print(quantity,"Quatityyyy")
#         if quantity is not None and quantity.isdigit():
#             quantity = int(quantity)


#         product = get_object_or_404(Product,id=id)

       
#         try:
#             existing_cart_item = Cart.objects.get(user=request.user,product_name_id = id)
#             existing_cart_item.quantity += 1
#             existing_cart_item.total = existing_cart_item.price * existing_cart_item.quantity
#             existing_cart_item.save()
#         except Cart.DoesNotExist:
#             total = product.regular_price * quantity
#             cart_item= Cart(
#                 user=user,
#                 product_name =product,
#                 price=product.regular_price,
#                 quantity=quantity,
#                 total=total,
#                 size = size,
#                 colour =colour,
#                 )
#             cart_item.save()
#         return redirect('cart')

#     return render(request,'home/cart.html')
#     # return redirect(reverse('signin'))



            
           

# def update_cart(request,cart_item_id):
#     cart_item = get_object_or_404(Cart,id=cart_item_id)
#     if request.method == 'POST':
#         action = request.POST.get('action')

#         if action == 'increase':
#             cart_item.quantity += 1
#             cart_item.total = cart_item.price * cart_item.quantity
#         elif action == 'decrease':
#             if cart_item.quantity > 1 :
#                 cart_item.quantity -= 1
#                 cart_item.total = cart_item.price * cart_item.quantity
#         else:
#             cart_item.delete()
#         cart_item.save()
#     return redirect('cart')




# def remove_from_cart(request, cart_item_id):
#     cart_item = get_object_or_404(Cart,id=cart_item_id)
#     cart_item.delete()
#     return redirect('cart')

   