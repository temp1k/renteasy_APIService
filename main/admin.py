from django.contrib import admin

# Register your models here.
from main.models import Category, Image, Housing, HousingImages, Tag, Chat, Message, Feedback, \
    PublishedHousing, Currency, City, Metro, District, PublicationStatus, MessagesRequest, BuyRequest

admin.site.register(Category)


@admin.register(Image)
class ImagesAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
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


@admin.register(Metro)
class TypesAdmin(admin.ModelAdmin):
    pass


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessagesAdmin(admin.ModelAdmin):
    pass


@admin.register(PublicationStatus)
class PublicationStatusAdmin(admin.ModelAdmin):
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


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(MessagesRequest)
class MessagesRequestAdmin(admin.ModelAdmin):
    pass


@admin.register(BuyRequest)
class BuyRequestAdmin(admin.ModelAdmin):
    pass
