from django.urls import path
from card.views import CardListCreateAPIView, RetrieveDeleteCardAPIView

app_name = 'card'
urlpatterns = [
    path('', CardListCreateAPIView.as_view(), name='card'),
    path('<uuid:cardId>', RetrieveDeleteCardAPIView.as_view(), name="card-detail"),
]
