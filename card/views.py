from django.shortcuts import render
from card.models import Card
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.views import APIView
from card.serializers import CardSerializer, AuthorizeCardSerializer
from rest_framework.permissions import IsAuthenticated
from users.models import *
from card.utils import encrypt, decrypt
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from card.permissions import IsIssuerBank, IsOwner
# Create your views here.


class CardListCreateAPIView(ListCreateAPIView):
    serializer_class = CardSerializer
    queryset = Card.objects.all()

    def perform_create(self, serializer):
        consumer = ConsumerProfile.objects.get(user=self.request.user)
        encrypted_pan = encrypt(serializer.validated_data['fullPAN'])
        serializer.save(consumer=consumer, fullPAN=encrypted_pan)
        return Response({"data": serializer.data, "mssg":"card successfully enrolled"}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        consumer = ConsumerProfile.objects.get(user=self.request.user)
        return self.queryset.filter(consumer=consumer)


class CardEnrollmentAPIView(GenericAPIView):
    serializer_class = CardSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()


        return Response({"data":serializer.data, "mssg":"Card Enrollment successful"}, status=status.HTTP_201_CREATED)

class AuthorizeTokenization(APIView):
    serializer_class = AuthorizeCardSerializer
    permission_classes = (IsAuthenticated, IsIssuerBank, )

    def get(self, request):
        cardId = request.GET.get('cardId')
        card = Card.objects.get(cardId=cardId)

        if not card.is_issuer_authorized:
            card.is_issuer_authorized = True
            card.save()
        
        return Response({"success":"Issuer Bank Authorized card for tokenization"})


class RetrieveDeleteCardAPIView(RetrieveDestroyAPIView):
    serializer_class = CardSerializer
    queryset = Card.objects.all()
    permission_classes = (IsAuthenticated, IsOwner,) 
    lookup_field = "cardId" 

    def get_queryset(self):
        consumer = ConsumerProfile.objects.get(user=self.request.user)
        return self.queryset.filter(consumer=consumer)