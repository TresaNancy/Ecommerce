from django.db import models
from authentication.models import CustomUser

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField()
    pincode = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    set_default = models.BooleanField(default = False)
    
    def __str__ (self):
        return self.full_name
    

