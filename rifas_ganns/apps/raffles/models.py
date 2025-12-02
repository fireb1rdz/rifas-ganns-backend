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
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0) 
    created_by = models.ForeignKey(User, related_name='created_raffles', on_delete=models.PROTECT, verbose_name="Usuário")

    def __str__(self):
        return self.title
    
    def update_percentage(self, *args: float):
        """Atualiza a porcentagem de cotas vendidas com base no número de cotas vendidas e no total de cotas disponíveis.
        Se um valor específico for fornecido como argumento, ele será usado para atualizar a porcentagem diretamente.
        """
        if args:
            self.percentage = args[0]
            self.save()
            return
        self.percentage = self.current_quota_percentage
        self.save()
            
    def current_quota_percentage(self):
        """Calcula a porcentagem atual de cotas vendidas com base no número de cotas vendidas e no total de cotas disponíveis."""
        if self.quota_count > 0:
            return (self.quotas.count() / self.quota_count) * 100
        return 0.0
            
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
    seller = models.ForeignKey(User, related_name='sold_quotas', on_delete=models.SET_NULL, null=True, blank=True)
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

class RaffleSellerPaymentLink(models.Model):
    raffle = models.ForeignKey(Raffle, related_name='seller_payment_links', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='raffle_payment_links', on_delete=models.CASCADE)
    payment_link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment Link for {self.seller.username} in {self.raffle.title}'
    
    class Meta:
        verbose_name = 'Raffle Seller Payment Link'
        verbose_name_plural = 'Raffle Seller Payment Links'