from django.urls import path

from backupDb.views import CreateBackup, Restore

urlpatterns = [
    path('', CreateBackup.as_view(), name='backup'),
    path('restore/', Restore.as_view(), name='restore'),
]
