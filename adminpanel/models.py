from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class Brand(models.Model):
    brand_name = models.CharField(max_length=200,null=False,unique=True)
    is_active = models.BooleanField(default=True)
#     quantity = models.PositiveIntegerField()
#     logo= models.ImageField(upload_to='photo/brand',blank=True, null=True)
#     description=models.CharField(max_length=250,null=True)

    def __str__(self):
        return self.brand_name

class Category(models.Model):
    category_name=models.CharField(max_length=100,null=False,unique = True)
    is_available =models.BooleanField(default=True)
    category_image=models.ImageField(upload_to='photo/category',blank=True,null=True)
    description=models.CharField(max_length=250)

    def __str__(self):
        return reverse('products_by_category', args=[self.pk]) 

    def __str__(self):
        return self.category_name
    
# class Sub_category(models.Model):
#     sub_category_name=models.CharField(max_length=100,null=False)
#     category = models.ForeignKey(Category,on_delete=models.CASCADE)
#     sub_category_title=models.CharField(max_length=250)
#     sub_category_description=models.CharField(max_length=250)

#     def __str__(self):
#         return self.sub_category_name

    
# class Size(models.Model):
#     regular_size=models.CharField(max_length=5,null=False,blank=False)
#     size_chart=models.TextField(max_length=100,null=True,blank=True)
  

#     def __str__(self):
#         return self.regular_size
    
# class ProductImage(models.Model):
#     product = models.ForeignKey('Product', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='photo/product' ,blank =True, null = True)

#     def __str__(self):
#         return f"Image {self.id}"
    

class Product(models.Model):
    product_name = models.CharField(max_length=200)
#     product_code = models.CharField(max_length=20,unique=True)
    product_description = models.TextField(max_length=500, blank=True)
    images = models.ImageField(upload_to='photo/products', null=True, blank=True)
    product_price = models.PositiveIntegerField(null=True, blank=True)
#     # quantity = models.IntegerField()
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,blank=True,null=True)
#     width = models.IntegerField(null=True,blank=True)
#     height = models.IntegerField(null=True,blank=True)
#     weight = models.IntegerField(null=True,blank=True)
#     product_images=models.ManyToManyField(ProductImage,blank=True,related_name='product_images')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
#     sub_category = models.ForeignKey(Sub_category,on_delete=models.CASCADE,blank=True,null=True)
#     available_sizes = models.ManyToManyField(Size, through = 'ProductSize', blank = True, related_name='product_sizes')
#     available_colours = models.ManyToManyField('Colour',through= 'ProductColour', blank = True, related_name='product_colours' )
    is_available = models.BooleanField(default=True)
    new_arrival = models.BooleanField(default=False)
    created_date = models.DateField(default = None)
    modified_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.created_date is None:
            self.created_date = timezone.now().date()  # Import timezone if not already imported
        super().save(*args, **kwargs)


    def get_url(self):
        return reverse('product_details', args=[self.category.pk, self.pk])


    def __str__(self) -> str:
        return self.product_name




class Colour(models.Model):
    product = models.ForeignKey('Product',on_delete=models.CASCADE,default=1)
    product_colour = models.CharField(max_length=50,null = False, blank = False)
    colour_stock = models.PositiveIntegerField(default=0)
    # sizes_available = models.ManyToManyField(Size,through='ColourSize')
    is_available = models.BooleanField(default=True)
    variant_image = models.ImageField(upload_to='photo/product',blank=True, null =True)
    
    def __str__(self):
        return self.product_colour
    
# class ColourSize(models.Model):
#     colour = models.ForeignKey('Colour',on_delete=models.CASCADE)
#     size = models.ForeignKey('Size',on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(null=True,blank=True)

# class ProductSize(models.Model):
#     product = models.ForeignKey(Product,on_delete = models.CASCADE)
#     size = models.ForeignKey(Size,on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(null=True, blank=True)

#     def __str__(self):
#         return f"Size {self.size} for {self.product.product_title}"
    
# class ProductColour(models.Model):
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     colour = models.ForeignKey('Colour',on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(null=True, blank=True)

#     def __str__(self):
#         return f"Colour {self.colour.product_colour} for {self.product.product_title}"

    

