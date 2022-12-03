from django.db.models.signals import post_save
from django.dispatch import receiver
from card.models import Card, Token, BankCard
from users.models import ConsumerProfile
from card.utils import decrypt
from rest_framework import exceptions


@receiver(post_save, sender=Card)
def authorize_card(sender, instance, created, **kwargs):
    if created:
        print("...")
        conumser = instance.consumer
        user = ConsumerProfile.objects.get(id=conumser.id).user
        user_email = user.email
        fullPan = decrypt(instance.fullPAN)
        bank_card = BankCard.objects.filter(
            email=user_email, fullPAN=fullPan, expDate=instance.expDate)
        if bank_card:
            instance.is_issuer_authorized = True
        return 


@receiver(post_save, sender=Card)
def create_token(sender, instance, created, **kwargs):
    if created:
        print("storing Token...")
        print(dir(instance))
        if not instance.is_issuer_authorized:
            Card.objects.get(cardId=instance.cardId).delete()
            raise exceptions.PermissionDenied({"error":"the card is not issuer authorized"})
        t = instance.get_token()
        print(t)
        token = Token.objects.create(cardId=instance, token=t)
        token.save()
        instance.is_tokenized = True
        instance.save()
        print(token)
        return {"msg": "Token created", "token": token}

