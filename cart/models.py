from django.db import models
from adminpanel .models import Product,Colour
from authentication .models import CustomUser
from django.utils import timezone

# # Create your models here.
# class Cart(models.Model):
#     user =models.ForeignKey(CustomUser,on_delete=models.CASCADE)
#     product_name = models.ForeignKey(Product,on_delete=models.CASCADE)
#     price = models.PositiveIntegerField(default=0)
#     quantity = models.PositiveIntegerField(null=False,blank=False)
#     total = models.PositiveIntegerField(default=0)
#     created_at = models.DateTimeField(default=timezone.now)
#     size = models.ForeignKey(Size, on_delete=models.CASCADE,default=0)
#     colour = models.ForeignKey(Colour, on_delete=models.CASCADE)

#     def sub_total(self):
#         return self.product.price * self.quantity
    
#     def get_total_quantity(self):
#         return sum(item.quantity for item in self.cart.all())

#     def __str__(self):
#         return f"Cart Item {self.id} - {self.product_name.brand_name}"


class Coupon(models.Model):
    code = models.CharField(max_length=50,unique = True)
    discount_price = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(default=True)
    end_date = models. DateField(default=0)
    min_price = models.IntegerField(default=0)
    max_price = models.IntegerField(default=0)

    def __str__(self)->str:
        return str(self.code)
    
class Cart(models.Model):
    cart_id =models.CharField(max_length=250,blank=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.cart_id
    
class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    colour = models.ForeignKey(Colour, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    cart_price = models.IntegerField(default=0)

    def sub_total(self):
        return self.product.price * self.quantity
    
    def get_total_quantity(self):
        return sum(item.quantity for item in self.cart.all())

    def __str__(self):
        return self.product
    

class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    colour = models.ForeignKey(Colour, on_delete=models.CASCADE,null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
