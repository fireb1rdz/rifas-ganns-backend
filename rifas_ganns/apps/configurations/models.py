from django.db import models
from apps.users.models import User
from django.utils.translation import gettext_lazy as _
from apps.raffles.models import Raffle

class UserConfiguration(models.Model):
    class ThemeChoices(models.TextChoices):
        LIGHT = "LG", _("LIGHT")
        DARK = "DK", _("DARK")
    user = models.OneToOneField(User, related_name="configuration", on_delete=models.PROTECT)
    theme = models.CharField(max_length=2, choices=ThemeChoices, default=ThemeChoices.LIGHT)
    class Meta:
        verbose_name = 'Configuração do usuário'
        verbose_name_plural = 'Configurações dos usuários'
class RaffleConfiguration(models.Model):
    raffle = models.OneToOneField(Raffle, related_name="configuration", on_delete=models.CASCADE)
    notify_winner_by_email = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'Configuração da rifa'
        verbose_name_plural = 'Configurações das rifas'

class GatewayConfiguration(models.Model):
    class GATEWAY_CHOICES(models.TextChoices):
        STRIPE = "ST", _("STRIPE")
        PAGARME = "PG", _("PAGARME")
    name = models.CharField(max_length=255, choices=GATEWAY_CHOICES.choices)
    active = models.BooleanField(default=False)
    test_api_key = models.CharField(max_length=255, null=True, blank=True)
    production_api_key = models.CharField(max_length=255, null=True, blank=True)
    customer_endpoint = models.URLField()
    payment_endpoint = models.URLField()