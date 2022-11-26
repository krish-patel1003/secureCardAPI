from django.db.models.signals import post_save
from django.dispatch import receiver
from card.models import Card, Token
from django.shortcuts import redirect, resolve_url
from django.urls import reverse
from django.utils.http import urlencode

# @receiver(post_save, sender=Card)
# def authorize_card(sender, instance, created, **kwargs):
#     if created:
#         print("...")
#         try:
#             res = redirect('http://127.0.0.1:8000/api/card/authorize-card-tokenization', kwargs={"cardId":instance.cardId})
#             print(res)
#             return res
#         except Exception as e:
#             print(e)
#             return redirect("/")

@receiver(post_save, sender=Card)
def create_token(sender, instance, created, **kwargs):
    if created:
        print("storing Token...")
        try:
            print(dir(instance))
            card = Card.objects.get(cardId=instance.cardId)
            t = card.get_token()
            print(t)
            token = Token.objects.create(cardId=instance, token=t)
            token.save()
            print(token)
            return {"msg":"Token created", "token":token}
        except Exception as e:
            print(e)
            return {"error":"something went wrong whilt token storing."}

# @receiver(post_save, sender=Card)
# def save_token(sender, instance, **kwargs):
#     return instance.token.save()
