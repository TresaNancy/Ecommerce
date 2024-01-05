from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.models import CustomUser
from django.views.decorators.cache import never_cache
from .models import Profile
from orders.models import *

# Create your views here.

@login_required(login_url='signin')
def my_profile(request):
    user=request.user
    context = {
        'user':user,
    }
    return render(request,'user/my_profile.html',context)

@login_required
def user_page(request):
    user=request.user
    context = {
        'user': user,
    }
    return render(request,'user/user_page.html',context)

@login_required
def update_profile(request):
    user = request.user
    print(user,"USR>>>>>>>>")

    if request.method == 'POST':
        new_username = request.POST.get('first_name')
        new_email = request.POST.get('email')
        new_phone = request.POST.get('phone')

        print(new_phone)
        print(new_username)

        try:
            # Retrieve the user's profile using the email
            current_user = CustomUser.objects.get(email=user.email)

            if new_username:
                current_user.first_name = new_username
            if new_email:
                current_user.email = new_email
            if new_phone:
                current_user.phone = new_phone

            current_user.save()

            messages.success(request, 'Profile updated successfully')
            return redirect('my_profile')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User profile not found')
        except Exception as e:
            messages.error(request, f'Profile update failed: {e}')

    return render(request, 'user/my_profile.html')


def address(request):
    bool = True
    addresses = Profile.objects.filter(user=request.user)
    context = {
        'show_footer': bool,
        'addresses':addresses
    }
    
    return render(request, 'user/address.html',context)
  

def add_address(request):
    if request.method == 'POST':
        name = request.POST.get('user_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        city = request.POST.get('city')
        user = CustomUser.objects.get(id = request.user.id)
        profile = Profile(
            full_name = name,
            phone = phone,
            email = email,
            address_line_1 = address,
            pincode = pincode,
            state = state,
            city = city,
            user = user,
        )
        check_address = Profile.objects.filter(user=request.user)
        if check_address:
            profile.save()
        else:
            profile.set_default = True
            profile.save()    
        messages.success(request,"Your address has been added successfully")
        return redirect('address')

    return render(request,'user/address.html')

 

@login_required(login_url='handlelogin')
def edit_address(request,id):
    address = get_object_or_404(Profile, id=id)
    
    if request.method == 'POST':
        address_name = request.POST.get('name')
        address_phone = request.POST.get('phone')
        address_email = request.POST.get('email')
        address_address = request.POST.get('address')
        address_pincode = request.POST.get('pincode')
        address_state = request.POST.get('state')
        address_city = request.POST.get('city')

        address.full_name = address_name
        address.phone = address_phone
        address.email = address_email
        address.address_line_1 = address_address
        address.country = address_pincode
        address.state = address_state
        address.city = address_city
        print(address_city)
        address.save()
        messages.success(request, "Your address has been successfully edited")
        return redirect('address')

    return render(request,'user/address.html')

def delete_address(request,id):
    if request.method =='POST':
        del_address = Profile.objects.get(id=id, user=request.user)
        if del_address.set_default==True:
            del_address.delete()
            set_another_default = Profile.objects.filter(user = request.user)
            if set_another_default:
                set_another_default[0].set_default = True
                set_another_default[0].save()
        else:
            del_address.delete()
        messages.info(request, "Your selected address has been successfully deleted.")
        return redirect('address')
    return redirect('address')
 
    

def set_default(request, id):
    if request.method == 'POST':
        address = Profile.objects.get(user=request.user,id=id)
        address.set_default = True
        address.save()
        
        try:
            defaults_to_reset = Profile.objects.filter(set_default=True).exclude(user=request.user, id=id)
            for default_address in defaults_to_reset:
                default_address.set_default = False
                default_address.save()
        except Profile.DoesNotExist:
            pass
        messages.success(request, "Your selected address has been set as the default for your future product purchases.")
        return redirect('address')
    return render(request,'user/address.html' )

# orders

def order_detail(request):
    bool = True
    orders = Order.objects.filter(user=request.user).order_by('-id')
    print(orders,"ooooooooooooooooo ")


    context = {
        'show_footer': bool,
        'orders':orders,

    }
    return render(request,"user/order_detail.html",context)

def order_detail_view(request,bulk_order_id, price=0):
    print(bulk_order_id,"bulk KKKKKKKKKK")
    bool = True
    orders = Order.objects.filter(bulk_order_id = bulk_order_id)
    order = Order.objects.filter(bulk_order_id=bulk_order_id).first()
    print(orders,"ordersssssssssssssss")
    
    for ord in orders:
        price += int(ord.unit_amount)
   
    context = {
        'show_footer': bool,
        'orders':orders,
        'order':order,
        'price':price,
       
    }
    return render(request,"user/order_detail_view.html",context )

def cancel_order(request,order_id):
    current_order = Order.objects.get(order_number=order_id)
    current_order.status = "Cancelled"  
    current_order.save() 
    cancel_order_price = int(current_order.unit_amount)
    print(cancel_order_price,"11111111111111")
    try:
        wallet = Wallet.objects.filter(user=request.user).first()
        print(wallet,"2222222222222")
    except:
        pass

    if wallet is None:
        wallet = Wallet.objects.create(user=request.user, wallet_amount = 0)
        print(wallet,"333333333333")


    wallet.wallet_amount += cancel_order_price 
    print(wallet.wallet_amount,"44444444444444")
    wallet.save()
    bulk_order_id = current_order.bulk_order_id
    print(current_order.status,"cancelledddddddddddddddd")
    return redirect(order_detail_view,bulk_order_id)


def user_coupon(request):

    coupons = Coupon.objects.all() 
    return render(request,'user/user_coupon.html',{'coupons': coupons})


