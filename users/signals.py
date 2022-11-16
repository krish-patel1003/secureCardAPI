from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from users.models import Bank, ConsumerProfile, Merchant, User


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print(dir(instance))
        if instance.role == 'CONSUMER':
            ConsumerProfile.objects.create(user=instance)
        elif instance.role == 'MERCHANT':
            Merchant.objects.create(user=instance)
        elif instance.role == 'BANK':
            Bank.objects.create(user=instance)
        else:
            pass


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    print(sender, instance, kwargs)
