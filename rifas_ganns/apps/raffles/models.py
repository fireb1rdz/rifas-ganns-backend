from django.db import models
from apps.users.models import User

class Raffle(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    draw_date = models.DateTimeField(null=True, blank=True)
    prize_value = models.DecimalField(max_digits=10, decimal_places=2)
    quota_value = models.DecimalField(max_digits=10, decimal_places=2)
    quota_count = models.IntegerField()
    winner = models.ForeignKey(User, related_name='prizes', on_delete=models.SET_NULL, null=True, blank=True)
    awarded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    @property
    def available_quotas(self):
        return self.quota_count - self.quotas.count()
    
    class Meta:
        verbose_name = 'Raffle'
        verbose_name_plural = 'Raffles'
        ordering = ['-draw_date']

class Quota(models.Model):
    id = models.BigAutoField(primary_key=True)
    raffle = models.ForeignKey(Raffle, related_name='quotas', on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    owner = models.ForeignKey(User, related_name='quotas', on_delete=models.CASCADE)
    bought_at = models.DateTimeField(auto_now_add=True)
    is_winner = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('raffle', 'number')
        verbose_name = 'Quota'
        verbose_name_plural = 'Quotas'

    def __str__(self):
        return f'Cota {self.number} do {self.raffle.title}'
        
class RafflePicture(models.Model):
    raffle = models.ForeignKey(Raffle, related_name='pictures', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='raffle_pictures/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    main = models.BooleanField(default=False)

    def __str__(self):
        return f'Picture for {self.raffle.title}'
    
    class Meta:
        verbose_name = 'Raffle Picture'
        verbose_name_plural = 'Raffle Pictures'
