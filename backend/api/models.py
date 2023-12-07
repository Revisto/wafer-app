from django.db import models
from django.contrib.auth.models import User

class Crypto(models.Model):
    name = models.CharField(max_length=255, unique=True)
    symbol = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    cryptos = models.ManyToManyField(Crypto, through='CryptoBalance')

    def __str__(self):
        return self.user.username

class CryptoBalance(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.crypto.symbol}: {self.balance}"

class CryptoValue(models.Model):
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)    
    
class Transaction(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    crypto_value = models.ForeignKey(CryptoValue, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.crypto.symbol}: {self.amount} - {self.timestamp}"