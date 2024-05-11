from io import StringIO

from django.core.management import call_command
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from backupDb.serializers import BackupSerializer


class CreateBackup(APIView):
    def post(self, request):
        serializer = BackupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                call_command('dbbackup')
                return Response(status=200)
            except Exception as ex:
                return Response(ex, status=500)
        else:
            return Response(serializer.errors, status=400)


class Restore(APIView):
    def post(self, request):
        try:
            out = StringIO()
            call_command('dbrestore', stdout=out, noinput=True, interactive=False)
            return Response(status=200)
        except Exception as ex:
            return Response(ex, status=500)

