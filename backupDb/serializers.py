from rest_framework import serializers
from datetime import datetime

from backupDb.models import Backup


class BackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backup
        fields = ['name']

    def create(self, validated_data):
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime('%d_%m_%Y_%H_%M_%S')

        # Добавляем дату и время к значению поля name
        validated_data['name'] = f"{validated_data['name']}_{formatted_datetime}"

        return super().create(validated_data)
