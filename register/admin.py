from django.contrib import admin
from .models import *


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass

@admin.register(SimOrder)
class SimOrderAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'sim_type']
    pass

@admin.register(SimCardOption)
class SimCardOptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    pass
