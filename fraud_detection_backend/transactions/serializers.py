# serializers.py
from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class PredictionSerializer(serializers.Serializer):
    # Define fields for your predictions data
    rule = serializers.CharField()
    confidence = serializers.FloatField()
    # Add more fields as needed based on the structure of your predictions data

    # If predictions data has nested structure, define nested serializers here

