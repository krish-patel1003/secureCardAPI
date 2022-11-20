from django.urls import path
from card.views import CardListCreateAPIView, AuthorizeTokenization, CardEnrollmentAPIView


urlpatterns = [
    path('', CardListCreateAPIView.as_view(), name='card'),
    path('authorize-card-tokenization',
         AuthorizeTokenization.as_view(), name='authorize-card-tokenization')
]