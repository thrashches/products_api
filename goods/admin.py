from django.contrib import admin
from .models import Shop, Category, Product, ProductInfo, ProductParameter, Parameter


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    pass


class ProductInline(admin.TabularInline):
    model = Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


class ParameterInline(admin.TabularInline):
    model = ProductParameter


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    inlines = [
        ParameterInline,
    ]


@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    pass


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    pass
