from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'get_groups']

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
