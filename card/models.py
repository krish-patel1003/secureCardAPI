from django.db import models
from users.models import ConsumerProfile
import uuid
from card.utils import encrypt, decrypt, tokenizeCard
# from jwt.api_jws

# Create your models here.


class Card(models.Model):
    consumer = models.ForeignKey(ConsumerProfile, on_delete=models.CASCADE)
    cardId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullPAN = models.CharField(max_length=255)
    expDate = models.DateField()
    is_issuer_authorized = models.BooleanField(default=False)
    is_tokenized = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.cardId} - {self.consumer.user.username}'
    
    def get_token(self):
        data = [{
            "consumer":self.consumer.user.id,
            "cardId":str(self.cardId),
            "fullPAN":self.fullPAN,
            "expDate":str(self.expDate)
        }]
        return tokenizeCard(data)
    

class TokenManager(models.Manager):
    pass

class Token(models.Model):
    cardId = models.ForeignKey(Card, on_delete=models.CASCADE)
    token = models.TextField()

    def __str__(self):
        return str(self.cardId)


class BankCard(models.Model):
    consumerId = models.ForeignKey(ConsumerProfile, on_delete=models.CASCADE)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)    
    phone = models.CharField(max_length=10)
    email = models.EmailField(default="a@b.com")
    fullPAN = models.CharField(max_length=255)
    expDate = models.DateField()

    def __str__(self):
        return f"{self.fname} {self.lname} - {self.expDate}"



