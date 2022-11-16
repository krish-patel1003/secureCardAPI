from django.contrib import admin
from users.models import *
# Register your models here.
admin.site.register(User)
admin.site.register(ConsumerProfile)
admin.site.register(Merchant)
admin.site.register(Bank)