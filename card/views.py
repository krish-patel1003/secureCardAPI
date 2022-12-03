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
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        consumer = ConsumerProfile.objects.get(user=self.request.user)
        encrypted_pan = encrypt(serializer.validated_data['fullPAN'])
        serializer.save(consumer=consumer, fullPAN=encrypted_pan)
        return Response({"data": serializer.data, "mssg":"card successfully enrolled"}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        consumer = ConsumerProfile.objects.get(user=self.request.user)
        return self.queryset.filter(consumer=consumer)


class RetrieveDeleteCardAPIView(RetrieveDestroyAPIView):
    serializer_class = CardSerializer
    queryset = Card.objects.all()
    permission_classes = (IsAuthenticated, IsOwner,) 
    lookup_field = "cardId" 

    def get_queryset(self):
        consumer = ConsumerProfile.objects.get(user=self.request.user)
        return self.queryset.filter(consumer=consumer)