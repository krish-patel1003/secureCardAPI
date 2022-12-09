from django.db import models
from users.models import *
from card.models import *
from datetime import datetime

# Create your models here.

class Transaction(models.Model):
    transactionId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    consumer = models.ForeignKey(ConsumerProfile, on_delete=models.CASCADE, null=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, null=True)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=00.00)
    cardId = models.CharField(max_length=255, default="")
    is_authorized = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f'{self.consumer.get_full_name} {self.transactionId}'
    
    def generate_encrypted_payload(self):
        print(dir(self))
        return f'testing gep {self.full_clean}'


    
    
    
    