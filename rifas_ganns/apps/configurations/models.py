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
    
class RaffleConfiguration(models.Model):
    raffle = models.OneToOneField(Raffle, related_name="configuration", on_delete=models.CASCADE)
    notify_winner_by_email = models.BooleanField(default=True)
    use_manual_percentage = models.BooleanField(default=False)
    