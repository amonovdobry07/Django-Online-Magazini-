# Register your models here.
from django.contrib import admin

from .models import Product, Category, Order, Customer, Cart, CartItem, SubCategory, Order




class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}
    
class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}
    


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(SubCategory, SubCategoryAdmin)

