from django.db.models.signals import post_save
from django.dispatch import receiver
from card.models import Card
from django.shortcuts import redirect, resolve_url
from django.urls import reverse
from django.utils.http import urlencode

@receiver(post_save, sender=Card)
def authorize_card(sender, instance, created, **kwargs):
    if created:
        print("...")
        try:
            res = redirect('http://127.0.0.1:8000/api/card/authorize-card-tokenization', kwargs={"cardId":instance.cardId})
            print(res)
            return res
        except Exception as e:
            print(e)
            return redirect("/")


