from django.apps import AppConfig


class AdminpanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adminpanel'


class CategoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'category'

class BrandConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'brand' 

class ColourConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Colour'      
