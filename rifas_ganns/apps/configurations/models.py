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
        STRIPE = "stripe", _("STRIPE")
        PAGARME = "pagarme", _("PAGARME")
    name = models.CharField(max_length=255, choices=GATEWAY_CHOICES.choices)
    active = models.BooleanField(default=False)
    customer_endpoint = models.URLField()
    payment_endpoint = models.URLField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Configuração do gateway"
        verbose_name_plural = "Configuração dos gateways"

class GatewayRequiredCustomerFields(models.Model):
    gateway = models.ForeignKey(GatewayConfiguration, on_delete=models.CASCADE)
    required_field_name = models.CharField(max_length=255)
    class Meta:
        verbose_name = "Campo obrigatório p/ cadastrar customer"
        verbose_name_plural = "Campos obrigatórios p/ cadastrar customer"