from django.db import models
from users.models import *
from card.models import *
# Create your models here.

class Transaction(models.Model):
    transactionId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    consumer = models.ForeignKey(ConsumerProfile, on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=00.00)
    token = models.ForeignKey(Token, null=True, on_delete=models.SET_NULL)
    is_authorized = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.consumer.get_full_name} {self.transactionId}'
    
    def generate_encrypted_payload(self):
        print(dir(self))
        return f'testing gep {self.full_clean}'


    
    
    
    