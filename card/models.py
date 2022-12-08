from django.db import models
from users.models import ConsumerProfile
import uuid
from card.utils import encrypt, decrypt, tokenizeCard
from django.core.validators import MinLengthValidator
# from jwt.api_jws

# Create your models here.


class Card(models.Model):
    consumer = models.ForeignKey(ConsumerProfile, null=True, on_delete=models.CASCADE)
    cardId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullPAN = models.CharField(max_length=255)
    expDate = models.DateField()
    issuerId = models.CharField(max_length=3, validators=[MinLengthValidator(3)], default="000")
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

    def get_issuer_id(self):
        ep = self.fullPAN
        p = decrypt(ep)
        return p[:3]
    
    def get_card_reference_id(self):
        return f'{self.issuerId}-{self.consumer.id}-{hex(int(self.cardId.time_low))[2:]}'
    

class TokenManager(models.Manager):
    pass

class Token(models.Model):
    cardId = models.ForeignKey(Card, on_delete=models.CASCADE)
    token = models.TextField()

    def __str__(self):
        return str(self.cardId)


class BankCard(models.Model):
    consumerId = models.ForeignKey(ConsumerProfile, on_delete=models.CASCADE)
    issuerId = models.CharField(max_length=3, validators=[MinLengthValidator(3)], default="123")
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)    
    phone = models.CharField(max_length=10)
    email = models.EmailField(default="a@b.com")
    fullPAN = models.CharField(max_length=255)
    expDate = models.DateField()

    def __str__(self):
        return f"{self.fname} {self.lname} - {self.expDate}"



