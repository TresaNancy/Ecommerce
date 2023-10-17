from django.shortcuts import render,get_object_or_404
from adminpanel.models import Product,Category,Brand
from django.views. decorators.cache import never_cache


# Create your views here.
@never_cache
def index(request):

    return render(request,'home/index.html')
    
    

def cart(request):
    print("tresaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    return render(request,'home/cart.html')


def checkout(request):
    return render(request,'home/checkout.html')


def contact(request):
    return render(request,'home/contact.html')


def detail(request,id):
    product= get_object_or_404(Product, id=id)

    context = {
        'product': product,
    
    }
    return render(request,'home/detail.html',context)


def shop(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request,'home/shop.html',context)

def singin(request):
    return render()