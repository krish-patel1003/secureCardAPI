from django.urls import path
from checkout.views import TransactionListCreateAPIView

urlpatterns = [
    path('', TransactionListCreateAPIView.as_view(), name='transaction'),
]