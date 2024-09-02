import datetime
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class BaseModel(models.Model):
    created_date = models.DateTimeField(default= timezone.now, editable=False)
    modified_date = models.DateTimeField(default= timezone.now)
    created_by = models.CharField(max_length=50, blank=True, null=True, default='')
    modified_by = models.CharField(max_length=50, blank=True, null=True, default='')
    is_active = models.BooleanField(default=True)
    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class MyTaskList(BaseModel):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, db_index=True)
    due_date=models.DateField(default=datetime.date.today(), db_index=True)
    category = models.ForeignKey(Category, null=True, default=None, on_delete=models.CASCADE, related_name='category')
    reminder_time = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        unique_together = ('user', 'title')
        ordering = ('due_date',)

    def save(self, *args, **kwargs):
        if self.due_date < datetime.date.today():
            raise ValidationError("Due date cannot be in the past!")
        if self.reminder_time and self.due_date < self.reminder_time < timezone.now:
            raise ValidationError("Reminder time should between today and due date!")
        super(MyTaskList, self).save(*args, **kwargs)