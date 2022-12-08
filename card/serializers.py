from rest_framework import serializers
from card.models import Card
from users.models import Bank
from django.shortcuts import redirect 
from django.utils.http import urlencode
from django.core.validators import MinLengthValidator

class CardSerializer(serializers.ModelSerializer):

    fullPAN = serializers.CharField(max_length=16, validators=[MinLengthValidator(16)])
    referenceId = serializers.SerializerMethodField()
    bank = serializers.SerializerMethodField()

    def get_referenceId(self, obj):
        return obj.get_card_reference_id()
    
    def get_bank(self, obj):
        return Bank.objects.get(issuerId=obj.issuerId).name

    class Meta:
        model = Card
        fields = ['consumer', 'cardId', 'referenceId', 'bank','fullPAN', 'expDate', 'issuerId', 'is_issuer_authorized', 'is_tokenized']

    def save(self, **kwargs):
        print(dir(self))
        return super().save(**kwargs)

class AuthorizeCardSerializer(serializers.Serializer):
    cardId = serializers.UUIDField()

    class Meta:
        model = Card
        fields = ['cardId']