from django.contrib import admin

# Register your models here.
from main.models import Category, Image

admin.site.register(Category)


@admin.register(Image)
class ImagesAdmin(admin.ModelAdmin):
    pass
