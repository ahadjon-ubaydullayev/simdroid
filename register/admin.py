from django.contrib import admin
from .models import *


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'cr_on', 'username']


@admin.register(SimOrder)
class SimOrderAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'sim_type', 'gift', 'address', 'tel_number']
    

@admin.register(SimCardOption)
class SimCardOptionAdmin(admin.ModelAdmin):
    list_display = ['sim_option']


@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ['name']
