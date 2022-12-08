from django.urls import path
from checkout.views import TransactionListCreateAPIView, TransacionHistoryAPIView

urlpatterns = [
    path('', TransactionListCreateAPIView.as_view(), name='transaction'),
    path('transaction-history', TransacionHistoryAPIView.as_view(), name='transaction-history'),
] 