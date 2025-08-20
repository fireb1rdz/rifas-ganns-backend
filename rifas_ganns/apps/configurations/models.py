from django.db import models
from apps.users.models import User
from django.utils.translation import gettext_lazy as _

class UserConfiguration(models.Model):
    class ThemeChoices(models.TextChoices):
        LIGHT = "LG", _("LIGHT")
        DARK = "DK", _("DARK")
    user = models.OneToOneField(User, related_name="configuration", on_delete=models.PROTECT)
    theme = models.CharField(max_length=2, choices=ThemeChoices, default=ThemeChoices.LIGHT)
    
    