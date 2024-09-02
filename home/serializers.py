from rest_framework import serializers

from .models import MyTaskList


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyTaskList
        fields = '__all__'
