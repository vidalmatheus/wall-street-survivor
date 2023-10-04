from django.db import models
from django_cryptography.fields import encrypt


class WssLogin(models.Model):
    BASE_URL = "https://app.wallstreetsurvivor.com"

    username = models.CharField(max_length=100, unique=True, db_index=True)
    password = encrypt(models.CharField(max_length=100))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    wss_login = models.ForeignKey(WssLogin, on_delete=models.CASCADE)
    actions = models.CharField(max_length=100, null=True, blank=True)
    transaction_type = models.CharField(max_length=100, null=True, blank=True)
    symbol = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    price_status = models.CharField(max_length=100, null=True, blank=True)
    fee = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=4)
    date_time = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
