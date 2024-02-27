from django.contrib import admin

# Register your models here.
from main.models import Category, Image, Country, Housing

admin.site.register(Category)


@admin.register(Image)
class ImagesAdmin(admin.ModelAdmin):
    pass


@admin.register(Country)
class CountriesAdmin(admin.ModelAdmin):
    pass


@admin.register(Housing)
class HousingsAdmin(admin.ModelAdmin):
    pass
