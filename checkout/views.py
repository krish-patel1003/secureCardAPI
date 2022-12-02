from django.shortcuts import render
from rest_framework.response import Response
from checkout.models import Transaction
from card.models import *
from users.models import *
from rest_framework.generics import ListCreateAPIView
from checkout.serializers import TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from checkout.permissions import IsMerchant
from rest_framework import status
# Create your views here.


class TransactionListCreateAPIView(ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated, IsMerchant, )
    queryset = Transaction.objects.all()

    def perform_create(self, serializer):
        merchant = Merchant.objects.get(user=self.request.user)
        serializer.save(merchant=merchant)
        return Response({'data':serializer.data, 'msg':'New Transaction added'}, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        merchant = Merchant.objects.get(user=self.request.user)
        return self.queryset.filter(merchant=merchant)

    