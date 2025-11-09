from django.contrib import admin
from .models import Brand, CarModel, Car

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand')
    list_filter = ('brand',)
    search_fields = ('name', 'brand__name')

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'engine_type', 'transmission', 'price')
    list_filter = ('brand', 'engine_type', 'transmission', 'year')
    search_fields = ('brand__name', 'model__name')
