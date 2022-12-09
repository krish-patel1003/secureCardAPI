from django.urls import path
from checkout.views import TransactionListCreateAPIView, TransacionHistoryAPIView, VerifyPayment

urlpatterns = [
    path('', TransactionListCreateAPIView.as_view(), name='transaction'),
    path('transaction-history', TransacionHistoryAPIView.as_view(), name='transaction-history'),
    path('verifyPayment', VerifyPayment.as_view(), name="verify-payment"),
] 