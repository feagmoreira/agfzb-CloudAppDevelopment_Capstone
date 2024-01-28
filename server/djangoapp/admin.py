from django.contrib import admin
from .models import CarMake, CarModel

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel 
    extra = 5

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['Name', 'Type', 'Year', 'Dealer_Id']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields = ['Name', 'Description']
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarMake,CarMakeAdmin)
admin.site.register(CarModel,CarModelAdmin)
