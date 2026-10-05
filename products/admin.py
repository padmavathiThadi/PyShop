from django.contrib import admin
from .models import Product, Offer, Order, OrderItem


class OfferAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total', 'status', 'created_at')
    list_editable = ('status',)
    inlines = [OrderItemInline]


admin.site.register(Offer, OfferAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)


