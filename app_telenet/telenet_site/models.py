import datetime
from datetime import timedelta

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.


class Service(models.Model):
    name = models.CharField(max_length=255, null=False, default="")
    description = models.TextField(null=True)
    price = models.FloatField(null=False, default=0)
    image = models.ImageField(upload_to='service_images/' + str(datetime.datetime.now()), null=True, blank=True)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    text = models.TextField(null=False, default="")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, default='Undefined')
    score = models.PositiveIntegerField(null=False, validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    create_datetime = models.DateTimeField(auto_now_add=True)
    edit_datetime = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='feedback_images/' + str(datetime.datetime.now()))

    def __str__(self):
        return f'{self.service.name}: {str(self.text)[:10]}'


class Order(models.Model):
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, null=False, blank=True, default="")
    register_date = models.DateTimeField(auto_now_add=True)
    order_end_date = models.DateField(auto_now_add=True)

    def save(self):
        from datetime import timedelta
        d = timedelta(days=30)

        if not self.id:
            super(Order, self).save()
            self.mydate += d
            super(Order, self).save()

