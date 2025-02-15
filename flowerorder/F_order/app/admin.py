from django.contrib import admin

# Register your models here.
from .models  import MainSubProduct, Product,MainProduct,LastProduct,SubProduct,SubLastProduct,Order
admin.site.register(LastProduct)
admin.site.register(MainProduct)
admin.site.register(Product)
admin.site.register(SubProduct)
admin.site.register(MainSubProduct)
admin.site.register(SubLastProduct)
admin.site.register(Order)