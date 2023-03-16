from .models import Wallet, WalletTransaction, Milestone, Payment
from rest_framework import serializers
from django.db.models import Sum
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.conf import settings
import requests

# get the user model set in the settings
User = get_user_model()

class WalletSerializer(serializers.ModelSerializer):
    """
    Serializer to validate the user's wallet 
    """
    balance = serializers.SerializerMethodField()

    def get_balance(self, obj):
        # calculate and return the balance of the wallet
        bal = WalletTransaction.objects.filter(
            wallet=obj, status="success").aggregate(Sum('amount'))['amount__sum']
        return bal

    class Meta:
        model = Wallet
        fields = ['id', 'currency', 'balance']


def is_amount(value):
    # custom validator to check if the amount is valid
    if value <= 0:
        raise serializers.ValidationError({"detail": "Invalid Amount"})
    return value


class DepositSerializer(serializers.Serializer):
    """
    Serializer to validate the deposit transaction
    """
    amount = serializers.IntegerField(validators=[is_amount])
    email = serializers.EmailField()

    def validate_email(self, value):
        # check if the user with the given email exists
        if User.objects.filter(email=value).exists():
            return value
        raise serializers.ValidationError({"detail": "Email not found"})

    def save(self):
        # get the user from the request and their wallet
        user = self.context['request'].user
        wallet = Wallet.objects.get(user=user)
        data = self.validated_data
        # create the paystack transaction request
        url = 'https://api.paystack.co/transaction/initialize'
        headers = {
            "authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
        }
        r = requests.post(url, headers=headers, data=data)
        response = r.json()
        # create a wallet transaction object for the deposit
        WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type="deposit",
            amount=data["amount"],
            paystack_payment_reference=response['data']['reference'],
            status="pending",
        )
        # return the paystack response
        return response


class MilestoneSerializer(serializers.ModelSerializer):
    """
    Serializer to validate the milestone
    """
    class Meta:
        model = Milestone
        fields = ['id', 'name', 'description', 'amount', 'influencer', 'created_at']


class WalletTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer to validate the wallet transaction
    """
    milestone = MilestoneSerializer(required=False)

    class Meta:
        model = WalletTransaction
        fields = ['id', 'wallet', 'transaction_type', 'amount', 'timestamp',
                  'status', 'paystack_payment_reference', 'milestone']

    def create(self, validated_data):
        # create a new wallet transaction object with its related milestone if provided
        milestone_data = validated_data.pop('milestone', None)
        wallet_transaction = WalletTransaction.objects.create(**validated_data)

        if milestone_data:
            Milestone.objects.create(
                wallet_transaction=wallet_transaction, **milestone_data)

        return wallet_transaction

    def update(self, instance, validated_data):
        # update the wallet transaction object and its related milestone if provided
        milestone_data = validated_data.pop('milestone', None)

        instance.transaction_type = validated_data.get(
            'transaction_type', instance.transaction_type)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.timestamp = validated_data.get(
            'timestamp', instance.timestamp)
        instance.status = validated_data.get('status', instance.status)
        instance.paystack_payment_reference = validated_data.get(
            'paystack_payment_reference', instance.paystack_payment_reference)

        instance.save()

        if milestone_data:
            milestone = instance.milestone
            if milestone:
                milestone.title = milestone_data.get(
                    'title', milestone.title)
                milestone.description = milestone_data.get(
                    'description', milestone.description)
                milestone.due_date = milestone_data.get(
                    'due_date', milestone.due_date)
                milestone.save()
            else:
                Milestone.objects.create(
                    wallet_transaction=instance, **milestone_data)

        return instance


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer to validate the payment
    """
    class Meta:
        model = Payment
        fields = ('id', 'milestone', 'brand', 'amount', 'status', 'created_at')