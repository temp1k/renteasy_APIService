from django.contrib import admin

from users.models import CustomUser, CustomGroup


@admin.register(CustomUser)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'get_groups']
    readonly_fields = ['password', 'last_login', 'date_joined']

    def has_add_permission(self, request):
        return False

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])


@admin.register(CustomGroup)
class GroupsAdmin(admin.ModelAdmin):
    list_display = ['name']
