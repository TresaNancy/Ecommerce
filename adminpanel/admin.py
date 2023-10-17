from django.contrib import admin
from .models import Product,Brand,Category,Sub_category,Size,Colour

# Register your models here.
admin.site.register(Product),
admin.site.register(Brand),
admin.site.register(Category),
admin.site.register(Sub_category),
admin.site.register(Size),
admin.site.register(Colour)