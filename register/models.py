from django.db import models
from django.db.models.base import ModelState
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class SimCardOption(models.Model):
    sim_option = models.CharField(max_length=50)

    class  Meta:  
        verbose_name_plural = "Sim karta turlari"
 
    def __str__(self):
        return self.sim_option


class Gift(models.Model):
    name = models.CharField(max_length=50)

    class  Meta:  
        verbose_name_plural = "Sovg'alar"

    def __str__(self):
        return self.name


class Client(models.Model):
    user_id = models.CharField(max_length=20)
    username = models.CharField(null=True, blank=True, max_length=128)
    first_name = models.CharField(max_length=64)
    cr_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    language = models.CharField(max_length=20, null=True, blank=True)
    step = models.IntegerField(default=0)

    class  Meta:  
        verbose_name_plural = "Mijozlar"

    def __str__(self):
        return self.first_name


class SimOrder(models.Model):
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)
    sim_type = models.ForeignKey(SimCardOption, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=128)
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    id_picture = models.ImageField(upload_to='images', default='default.jpg')
    id_picture2 = models.ImageField(upload_to='images', default='default.jpg')
    tel_number = models.CharField(max_length=100)
    step = models.IntegerField(default=0)
    active_sim = models.BooleanField(default=False)

    class  Meta:  
        verbose_name_plural = "Buyurtmalar"

    def __str__(self):
        return("Buyurtmalar")

    def get_absolute_url(self):
        return reverse('order_detail', args=[self.id])

