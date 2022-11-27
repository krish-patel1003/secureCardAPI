from django.urls import path
from card.views import CardListCreateAPIView, AuthorizeTokenization, RetrieveDeleteCardAPIView


urlpatterns = [
    path('', CardListCreateAPIView.as_view(), name='card'),
    path('<uuid:cardId>', RetrieveDeleteCardAPIView.as_view(), name="card-detail"),
    path('authorize-card-tokenization',
         AuthorizeTokenization.as_view(), name='authorize-card-tokenization')
]
