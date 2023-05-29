from django.contrib import admin

from .models import Order, Service, Feedback

admin.site.register(Order)
admin.site.register(Service)
admin.site.register(Feedback)
