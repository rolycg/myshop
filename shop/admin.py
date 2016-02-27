from django.contrib import admin
from .models import Category, Product, Discount
from parler.admin import TranslatableAdmin
from django.utils.translation import gettext_lazy as _


class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'category', 'real_price', 'sell_price', 'get_discount', 'stock', 'available']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['real_price', 'stock', 'available']

    # filter_horizontal = ['discount']

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

    def sell_price(self, obj):
        return obj.price()

    sell_price.short_description = _('Sell Price')

    def get_discount(self, obj):
        return str(obj.get_discount_percent()) + '%'

    get_discount.short_description = _('Discount')


class DiscountAdmin(admin.ModelAdmin):
    filter_horizontal = ['products']
    list_display = ['valid_from', 'valid_to', 'discount']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Discount, DiscountAdmin)
