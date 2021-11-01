from django.contrib import admin
from .models import Product, Order, OrderItem

@admin.register(Product)
class RegisterProduct(admin.ModelAdmin):
    list_display = ['product_name','quantity','price','is_available','is_active']
    search_fields = ['product_name']
    list_filter = ['is_available']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ['name','surname','email','phone','address','post_code','city','paid']
    list_display = ['name','surname','email','phone','paid']
    search_fields = ['name','surname','email','phone']
    list_filter = ['paid','created']
    inlines = [OrderItemInline]



