from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wallet, WalletTransaction, Milestone, Payment
from .serializers import WalletSerializer, WalletTransactionSerializer, MilestoneSerializer, PaymentSerializer

# This view returns the wallet information of the user
class WalletInfo(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    
    def get_object(self):
        # Retrieve the authenticated user
        user = self.request.user
        # Get or create a wallet instance for the user
        wallet, created = Wallet.objects.get_or_create(user=user)
        return wallet

# This view allows a user to deposit funds into their wallet
class DepositView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        # Retrieve the authenticated user
        user = request.user
        # Retrieve the amount to be deposited
        amount = request.data.get('amount')

        try:
            # Get the user's wallet instance
            wallet = Wallet.objects.get(user=user)
        except Wallet.DoesNotExist:
            # If the user does not have a wallet instance, create one
            wallet = Wallet.objects.create(user=user)

        # Update the wallet balance and create a transaction instance
        wallet.balance += amount
        wallet_transaction = WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type='deposit',
            amount=amount,
            status='successful',
        )
        wallet_transaction.save()
        wallet.save()

        return Response({'success': 'Deposit successful.'}, status=status.HTTP_200_OK)

# This view allows a user to withdraw funds from their wallet
class WithdrawView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        # Retrieve the authenticated user
        user = request.user
        # Retrieve the amount to be withdrawn
        amount = request.data.get('amount')

        try:
            # Get the user's wallet instance
            wallet = Wallet.objects.get(user=user)
        except Wallet.DoesNotExist:
            # If the user does not have a wallet instance, return an error response
            return Response({'error': 'Wallet does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if wallet.balance < amount:
            # If the user does not have enough funds in their wallet, return an error response
            return Response({'error': 'Insufficient balance.'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the wallet balance and create a transaction instance
        wallet.balance -= amount
        wallet_transaction = WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type='withdraw',
            amount=amount,
            status='successful',
        )
        wallet_transaction.save()
        wallet.save()

        return Response({'success': 'Withdrawal successful.'}, status=status.HTTP_200_OK)

# This view returns the wallet balance of the authenticated user
class BalanceCheck(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    
    def get(self, request):
        # Retrieve the authenticated user
        user = request.user
        # Get the user's wallet instance
        wallet = Wallet.objects.get(user=user)
        balance = wallet.balance
        serializer = WalletSerializer(wallet)
        # Return the wallet information and balance
        return Response({"wallet": serializer.data, "balance": balance}, status=status.HTTP_200_OK)

# This view allows a user to deposit funds into their wallet via paystack payment gateway
class DepositFunds(APIView):
    serializer_class = WalletTransactionSerializer

    def post(self, request, format=None):
        """
        API endpoint for depositing funds into the user's wallet.

        Args:
            request: The HTTP request object.
            format: The format of the request.

        Returns:
            A HTTP response with a success or error message.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            amount = serializer.data.get('amount')
            user = request.user
            wallet, created = Wallet.objects.get_or_create(user=user)
            WalletTransaction.objects.create(wallet=wallet, transaction_type='deposit', amount=amount)
            wallet.balance += amount
            wallet.save()
            return Response({'message': 'Deposit successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyDeposit(APIView):
    def get(self, request, reference):
        transaction = WalletTransaction.objects.filter(paystack_payment_reference=reference).first()
        if transaction:
            transaction.status = 'completed'
            transaction.save()
            wallet = transaction.wallet
            wallet.balance += transaction.amount
            wallet.save()
            return Response({'message': 'Deposit successful'}, status=status.HTTP_200_OK)
        return Response({'message': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)


class CreateMilestone(APIView):
    serializer_class = MilestoneSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(influencer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListMilestones(generics.ListAPIView):
    serializer_class = MilestoneSerializer

    def get_queryset(self):
        influencer = self.request.user
        return Milestone.objects.filter(influencer=influencer)


class PayInfluencer(APIView):
    serializer_class = PaymentSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            influencer = serializer.data.get('influencer')
            amount = serializer.data.get('amount')
            milestone = serializer.data.get('milestone')
            brand = request.user
            Payment.objects.create(milestone=milestone, brand=brand, amount=amount)
            return Response({'message': 'Payment successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        amount = request.data.get('amount')

        try:
            wallet = Wallet.objects.get(user=user)
        except Wallet.DoesNotExist:
            return Response({'error': 'Wallet does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if wallet.balance < amount:
            return Response({'error': 'Insufficient balance.'}, status=status.HTTP_400_BAD_REQUEST)

        wallet.balance -= amount
        wallet_transaction = WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type='withdraw',
            amount=amount,
            status='successful',
        )
        wallet_transaction.save()
        wallet.save()

        return Response({'success': 'Withdrawal successful.'}, status=status.HTTP_200_OK)


        