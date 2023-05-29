from rest_framework import serializers
from .models import Service, Order, Feedback


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('name', 'price')