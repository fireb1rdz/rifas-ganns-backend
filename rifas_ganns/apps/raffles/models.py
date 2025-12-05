from django.db import models
from apps.users.models import User

class Prize(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_selling_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Prêmio'
        verbose_name_plural = 'Prêmios'
class PrizePicture(models.Model):
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='raffle_pictures/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    main = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Foto do prêmio'
        verbose_name_plural = 'Fotos do prêmio'
class Raffle(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    draw_date = models.DateTimeField(null=True, blank=True)
    quota_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor da cota")
    quota_count = models.IntegerField(verbose_name="Quantidade de cotas total")
    amount_to_sell = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor de venda total")
    winner = models.ForeignKey(User, related_name='prizes', on_delete=models.SET_NULL, null=True, blank=True)
    awarded_at = models.DateTimeField(null=True, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, verbose_name="Porcentagem de cotas vendidas") 
    created_by = models.ForeignKey(User, related_name='created_raffles', on_delete=models.PROTECT, verbose_name="Usuário")
    prizes = models.ManyToManyField(Prize, through="RafflePrize", through_fields=["raffle", "prize"])

    def __str__(self):
        return self.title
    
    def update_percentage(self):
        """Atualiza a porcentagem de cotas vendidas com base no número de cotas vendidas e no total de cotas disponíveis.
        """
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
        verbose_name = 'Rifa'
        verbose_name_plural = 'Rifas'
        ordering = ['-draw_date']

class RafflePrize(models.Model):
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE, related_name="raffles")
    main = models.BooleanField(default=True)
    roulette = models.BooleanField(default=False)
    awarded_quota = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Prêmio x rifa'
        verbose_name_plural = 'Prêmios x rifas'
    
class RafflePicture(models.Model):
    raffle = models.ForeignKey(Raffle, related_name='pictures', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='raffle_pictures/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    main = models.BooleanField(default=False)

    def __str__(self):
        return f'Picture for {self.raffle.title}'
    
    class Meta:
        verbose_name = 'Foto da rifa'
        verbose_name_plural = 'Fotos da rifa'

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
        verbose_name = 'Cota'
        verbose_name_plural = 'Cotas'

    def __str__(self):
        return f'Cota {self.number} do {self.raffle.title}'
        
class PreAwardedQuota(models.Model):
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE, verbose_name="Rifa")
    quota_number = models.IntegerField(verbose_name="Número da cota")
    block_number = models.BooleanField(default=True, verbose_name="Bloqueia o número impossibilitando de comprar")
    class Meta:
        verbose_name = 'Cota pré-selecionada'
        verbose_name_plural = 'Cotas pré-selecionadas'