from django.contrib import admin
from .models import Product, KorzinaItem, Category, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'customer_fullname', 'created_at', 'status', 'total_items_count')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
    inlines = [OrderItemInline]
    actions = ['confirm_orders', 'cancel_orders']

    def customer_fullname(self, obj):
        return f"{obj.user.last_name or ''} {obj.user.first_name or ''} {obj.user.patronymic or ''}".strip() or obj.user.username
    customer_fullname.short_description = 'ФИО заказчика'

    def total_items_count(self, obj):
        return sum(item.quantity for item in obj.items.all())
    total_items_count.short_description = 'Кол-во товаров'

    def confirm_orders(self, request, queryset):
        queryset.update(status='confirmed')
    confirm_orders.short_description = 'Подтвердить выбранные заказы'

    def cancel_orders(self, request, queryset):
        queryset.update(status='canceled')
    cancel_orders.short_description = 'Отменить выбранные заказы'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'count', 'total_stock', 'year', 'country')
    list_filter = ('category', 'country', 'year')
    search_fields = ('name', 'model_name')

@admin.register(KorzinaItem)
class KorzinaItemAdmin(admin.ModelAdmin):
    list_display = ('us', 'product', 'quantity')
    list_filter = ('us', 'product')
    search_fields = ('us__username', 'product__name')
