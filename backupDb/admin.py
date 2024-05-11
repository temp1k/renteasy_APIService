from io import StringIO

from django.contrib import admin

# Register your models here.
from django.core.management import call_command
from backupDb.models import Backup


class BackupRestoreActionsMixin:
    actions = ['backup_database', 'restore_database']

    def restore_database(self, request, queryset):
        out = StringIO()
        call_command('dbrestore', stdout=out, noinput=True, interactive=False)
        self.message_user(request, "Database restored")

    restore_database.short_description = "Восстановить базу данных"


class BackupAdmin(BackupRestoreActionsMixin, admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


admin.site.register(Backup, BackupAdmin)



