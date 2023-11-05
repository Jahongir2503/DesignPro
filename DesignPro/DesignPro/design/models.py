from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Request(models.Model):
    NEW = 'NEW'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'

    STATUS_CHOICES = [
        (NEW, 'Новая'),
        (IN_PROGRESS, 'Принято в работу'),
        (COMPLETED, 'Выполнено'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='image/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'bmp'])])

    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW)

    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='requests')

    def __str__(self):
        return self.title
