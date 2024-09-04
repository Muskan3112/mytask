from django.db import models
from django.utils import timezone
from django_currentuser.middleware import get_current_user

class BaseModel(models.Model):
    created_date = models.DateTimeField(default= timezone.now, editable=False)
    modified_date = models.DateTimeField(default= timezone.now)
    created_by = models.CharField(max_length=50, blank=True, null=True, default='')
    modified_by = models.CharField(max_length=50, blank=True, null=True, default='')
    is_active = models.BooleanField(default=True)
    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        self.modified_date = timezone.now()
        self.modified_by = get_current_user()
        self.created_by = self.created_by if self.created_by else get_current_user()
        super(BaseModel, self).save(*args, **kwargs)

class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class MyTaskList(BaseModel):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, db_index=True)
    due_date=models.DateField(default=timezone.now, db_index=True)
    category = models.ForeignKey(Category, null=True, default=None, on_delete=models.CASCADE, related_name='category')
    reminder_time = models.DateTimeField(null=True, blank=True, default=None)
    class Meta:
        unique_together = ('user', 'title')
        ordering = ('due_date',)

    @property
    def category_name(self):
        return self.category.name