# transactions/models.py
from django.db import models

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Add other transaction attributes here
