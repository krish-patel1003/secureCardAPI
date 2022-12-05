from rest_framework import serializers
from card.models import Card
from django.shortcuts import redirect 
from django.utils.http import urlencode
from django.core.validators import MinLengthValidator

class CardSerializer(serializers.ModelSerializer):

    fullPAN = serializers.CharField(max_length=16, validators=[MinLengthValidator(16)])

    class Meta:
        model = Card
        fields = ['consumer', 'cardId', 'fullPAN', 'expDate', 'is_issuer_authorized', 'is_tokenized']

    # def create(self, validated_data):
    #     print(validated_data)
    #     print("Authorize for card tokenization requested...")
    #     # base_url = '/card/authorize-card-tokenization/'
    #     # query_string = urlencode({"cardId":validated_data["cardId"]})
    #     # url = f'{base_url}?{query_string}'
    #     # response = redirect(url)
    #     # print(response)

    #     return super().create(validated_data)


class AuthorizeCardSerializer(serializers.Serializer):
    cardId = serializers.UUIDField()

    class Meta:
        model = Card
        fields = ['cardId']