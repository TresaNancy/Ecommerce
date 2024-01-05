from django.contrib import admin
# from django import forms
from .models import *

# # Register your models here.
# # admin.site.register(Product),
# admin.site.register(Brand),
# admin.site.register(Category),
# admin.site.register(Sub_category),
# admin.site.register(Size),
# admin.site.register(Colour),
# admin.site.register(ProductImage)

# class ProductAdminForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = '__all__'


#     available_sizes = forms.ModelMultipleChoiceField(
#         queryset=Size.objects.all(),
#         required =False,
#         widget = admin.widgets.FilteredSelectMultiple('Available Sizes',False)
        
#     )

#     available_colours = forms.ModelMultipleChoiceField(
#         queryset=Colour.objects.all(),
#         required = False,
#         widget= admin.widgets.FilteredSelectMultiple('Available Colours',False)
    
#     )

# class ProductAdmin(admin.ModelAdmin):
#     form= ProductAdminForm

# admin.site.register(Product,ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display =('category_name',)

admin.site.register(Category,CategoryAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name',)

admin.site.register(Brand,BrandAdmin)

class ColourAdmin(admin.ModelAdmin):
    list_display = ('product_colour','colour_stock')

admin.site.register(Colour,ColourAdmin)