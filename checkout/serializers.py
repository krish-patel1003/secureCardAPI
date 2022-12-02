from rest_framework import serializers
from checkout.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['transactionId', 'consumer', 'merchant', 'transaction_amount', 'token', 'is_authorized']
    
    