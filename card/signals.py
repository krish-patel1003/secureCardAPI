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
        instance.issuerId = instance.get_issuer_id()
        bank_card = BankCard.objects.filter(
            email=user_email, fullPAN=fullPan, expDate=instance.expDate, issuerId=instance.issuerId)
        if bank_card:
            instance.is_issuer_authorized = True
            create_token(Card, instance, True)
        else:
            Card.objects.get(cardId=instance.cardId).delete()
            raise exceptions.ValidationError({"Error":"Card details r not issuer authorized"})


def create_token(sender, instance, created, **kwargs):
    if created:
        print("storing Token...")
        print(dir(instance))
        t = instance.get_token()
        print(t)
        token = Token.objects.create(cardId=instance, token=t)
        token.save()
        instance.is_tokenized = True
        instance.save()
        print(token)
        return {"msg": "Token created", "token": token}

