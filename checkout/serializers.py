from rest_framework import serializers
from checkout.models import Transaction
from card.utils import deTokenizeCard, decrypt
from card.models import Card, Token, BankCard
from users.utils import Util
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site



class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['transactionId', 'consumer', 'merchant',
            'transaction_amount', 'cardId', 'is_authorized']

    def validate(self, attrs):
        cardId = attrs.get("cardId", "")
        token_obj = Token.objects.get(cardId=cardId)
        request = self.context['request']
        
        if not token_obj:
            raise serializers.ValidationError({"Error": "Transaction Failed request failed, no such card"})

        else:
            c = Card.objects.get(cardId=cardId)
            bc = BankCard.objects.get(consumerId=c.consumer, expDate=c.expDate, fullPAN=decrypt(c.fullPAN))
            data = Util.prepare_payment_verify_email({"email":request.user.email, "cardId":cardId}, request)
            Util.send_email(data)

        return attrs


class PaymentVerifySerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)

    class Meta:
        model = Transaction
        fields = ['token']
