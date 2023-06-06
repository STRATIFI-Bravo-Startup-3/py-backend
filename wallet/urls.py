from django.urls import path
from .views import (
    WalletInfo,
    DepositFunds,
    VerifyDeposit,
    CreateMilestone,
    ListMilestones,
    PayInfluencer,
    WithdrawView,
    #DepositView,
    BalanceCheck,
)

urlpatterns = [
    path('wallet/', WalletInfo.as_view(), name='wallet_info'),
    path('deposit/', DepositFunds.as_view(), name='deposit_funds'),
    path('verify-deposit/<str:reference>/', VerifyDeposit.as_view(), name='verify_deposit'),
    path('create-milestone/', CreateMilestone.as_view(), name='create_milestone'),
    path('list-milestones/', ListMilestones.as_view(), name='list_milestones'),
    path('pay-influencer/', PayInfluencer.as_view(), name='pay_influencer'),
    path('withdraw/', WithdrawView.as_view(), name='withdraw'),
   # path('deposit/', DepositView.as_view(), name='deposit'),
    path('balance-check/', BalanceCheck.as_view(), name='balance_check'),
]
