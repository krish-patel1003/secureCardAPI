from django.shortcuts import render
from rest_framework.response import Response
from checkout.models import Transaction
from card.models import *
from users.models import *
from rest_framework.generics import ListCreateAPIView, ListAPIView, GenericAPIView
from rest_framework.views import APIView
import jwt
from checkout.serializers import TransactionSerializer, PaymentVerifySerializer
from rest_framework.permissions import IsAuthenticated
from checkout.permissions import IsMerchant
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
# Create your views here.


class TransactionListCreateAPIView(GenericAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Transaction.objects.all()

    def post(self, request):
        merchant = Merchant.objects.get(user=3)
        consumer = ConsumerProfile.objects.get(user=request.user)
        serializer = self.serializer_class(data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save(merchant=merchant, consumer=consumer)
        return Response({'data':serializer.data, 'msg':'New Transaction added'}, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        consumer = ConsumerProfile.objects.get(user=request.user)
        print(consumer)
        return self.queryset.filter(consumer=consumer).last()


class TransacionHistoryAPIView(ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Transaction.objects.all()

    def get_queryset(self):
        consumer = ConsumerProfile.objects.get(user=self.request.user)
        return self.queryset.filter(consumer=consumer)

class VerifyPayment(APIView):
    serializer_class = PaymentVerifySerializer

    def get(self, request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            c =ConsumerProfile.objects.get(user=user)
            t = Transaction.objects.filter(consumer=c).latest('created_at')
            print(t.transaction_amount)
            if not t.is_authorized:
                print("authorized")
                t.is_authorized = True
                t.save()

            return Response({"Success": "Payment verified"}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({"error": "verification link expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({"error": "Token is invalid, couldn't decode"}, status=status.HTTP_400_BAD_REQUEST)
