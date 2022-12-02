from django.urls import path
from users.views import (
    RegisterAPIView,
    VerifyEmailAPIView,
    LoginAPIView,
    PrepareConsumerProfile,
    BankDetailAPIView
)

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('email-verfiy', VerifyEmailAPIView.as_view(), name='email-verify'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('consumer/<int:id>', PrepareConsumerProfile.as_view(), name='prepare-consumer-profile'),
    path('bank/<int:id>', BankDetailAPIView.as_view(), name='bank-detail'),

]
