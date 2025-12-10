from django.db import models
from rifas_ganns.apps.users.models import User

class UserBalance(models.Model):
    user = models.OneToOneField(User, related_name="balance", on_delete=models.PROTECT, verbose_name="Usuário")
    balance = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    
    class Meta:
        verbose_name = "Saldo do usuário"
        verbose_name_plural = "Saldo dos usuários"
        