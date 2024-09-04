import datetime
from django.utils import timezone
from rest_framework import serializers

from .models import Category, MyTaskList

read_only_fields = ('created_date','modified_date','created_by','modified_by','is_active')
class TaskSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField()
    class Meta:
        model = MyTaskList
        fields = '__all__'
        read_only_fields = read_only_fields
        

    def validate(self, attrs):
        self.__validate_due_date(attrs)
        self.__validate_reminder_time(attrs)
        return super(TaskSerializer, self).validate(attrs)
    
    @staticmethod
    def __validate_due_date(attrs):
        if attrs['due_date'] < datetime.date.today():
            raise serializers.ValidationError("Due date cannot be in the past!")
    
    @staticmethod
    def __validate_reminder_time(attrs):
        if attrs.get('reminder_time') and attrs['reminder_time'] < timezone.now():
            raise serializers.ValidationError("Reminder time should between today and due date!")
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = read_only_fields
