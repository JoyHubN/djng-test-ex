from django.contrib import admin
from tovar.models import Product, KorzinaItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'count', 'total_stock')
    search_fields = ('name',)

@admin.register(KorzinaItem)
class KorzinaItemAdmin(admin.ModelAdmin):
    list_display = ('us', 'product', 'quantity')
    list_filter = ('us', 'product')
    search_fields = ('us__username', 'us__first_name', 'us__last_name', 'product__name')

