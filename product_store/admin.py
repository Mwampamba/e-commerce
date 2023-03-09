from django.contrib import admin
from .models import Product, Variation, Rating


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'original_price', 'selling_price', 'product_stock',
                    'product_category', 'product_brand', 'status')
    prepopulated_fields = {'product_slug': ('product_name',)}
    
    list_per_page = 10


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'status')
    list_editable = ('status',)
    list_filter = ('product',)
    
    list_per_page = 5


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(Rating)

