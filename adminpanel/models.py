from django.db import models

# Create your models here.
class Brand(models.Model):
    brand_name = models.CharField(max_length=200,null=False,unique=True)
    quantity = models.PositiveIntegerField()
    logo= models.ImageField(upload_to='photo/brand',blank=True, null=True)
    description=models.CharField(max_length=250,null=True)

    def __str__(self):
        return self.brand_name

class Category(models.Model):
    category_name=models.CharField(max_length=100,null=False)
    category_title=models.CharField(max_length=250)
    description=models.CharField(max_length=250)

    def __str__(self):
        return self.category_name
    
class Sub_category(models.Model):
    sub_category_name=models.CharField(max_length=100,null=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=False)
    sub_category_title=models.CharField(max_length=250)
    sub_category_description=models.CharField(max_length=250)

    def __str__(self):
        return self.sub_category_name

    
class Size(models.Model):
    regular_size=models.CharField(max_length=5,null=False,blank=False)
    size_chart=models.TextField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.regular_size
    
class Colour(models.Model):
    colour = models.CharField(max_length=50,null = False, blank = False)

    def __str__(self):
        return self.colour

class Product(models.Model):
    product_title = models.CharField(max_length=200)
    product_description = models.TextField(max_length=300)
    regular_price = models.IntegerField()
    quantity = models.IntegerField()
    size = models.ForeignKey(Size,on_delete=models.CASCADE)
    brand_name = models.ForeignKey(Brand,on_delete=models.CASCADE,blank=True,null=True)
    width = models.IntegerField(null=True,blank=True)
    height = models.IntegerField(null=True,blank=True)
    weight = models.IntegerField(null=True,blank=True)
    product_image=models.ImageField(upload_to='photo/product',blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    sub_category = models.ForeignKey(Sub_category,on_delete=models.CASCADE,blank=True,null=True)
    colour =models.ForeignKey(Colour,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self) -> str:
        return self.product_title

    

