from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=255, null=False, default="")
    description = models.TextField(null=True)
    price = models.FloatField(null=False, default=0)


class Feedback(models.Model):
    text = models.TextField(null=False, default="")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, default='Undefined')
    score = models.PositiveIntegerField(null=False, validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
