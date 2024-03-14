from django.contrib import admin

# Register your models here.
from main.models import Category, Image, Country, Housing, HousingImages, Tag, TypeHousing, Chat, Message, Feedback, PublishedHousing

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


@admin.register(HousingImages)
class HousingImagesAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    pass


@admin.register(TypeHousing)
class TypesAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessagesAdmin(admin.ModelAdmin):
    pass


@admin.register(Feedback)
class FeedbacksAdmin(admin.ModelAdmin):
    pass


@admin.register(Chat)
class ChatsAdmin(admin.ModelAdmin):
    pass


@admin.register(PublishedHousing)
class PublishedHousingsAdmin(admin.ModelAdmin):
    pass

