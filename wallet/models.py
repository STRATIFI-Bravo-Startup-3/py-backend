from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
# some google commit
User = get_user_model()


class Wallet(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    currency = models.CharField(max_length=50, default='NGN')
    balance = models.DecimalField(max_digits=100, null=True, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.user.__str__()


class WalletTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'deposit'),
        ('transfer', 'transfer'),
        ('withdraw', 'withdraw'),
    )
    wallet = models.ForeignKey(Wallet, null=True, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=200, null=True,  choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=100, null=True, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now, null=True)
    status = models.CharField(max_length=100, default="pending")
    paystack_payment_reference = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return self.wallet.user.__str__()


class Milestone(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    amount = models.DecimalField(max_digits=100, null=True, decimal_places=2)
    influencer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    milestone = models.ForeignKey(Milestone, null=True, on_delete=models.CASCADE)
    brand = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, null=True, decimal_places=2)
    status = models.CharField(max_length=100, default="pending")
    created_at = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.milestone.name