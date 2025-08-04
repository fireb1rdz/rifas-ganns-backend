from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    lucky_number = models.PositiveIntegerField(blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
class Address(models.Model):
    STATE_CHOICES = [
        ('SP', 'São Paulo'),
        ('RJ', 'Rio de Janeiro'),
        ('MG', 'Minas Gerais'),
        ('RS', 'Rio Grande do Sul'),
        ('PR', 'Paraná'),
        ('BA', 'Bahia'),
        ('PE', 'Pernambuco'),
        ('CE', 'Ceará'),
        ('SC', 'Santa Catarina'),
        ('DF', 'Distrito Federal'),
        ('GO', 'Goiás'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('AM', 'Amazonas'),
        ('PA', 'Pará'),
        ('MA', 'Maranhão'),
        ('PI', 'Piauí'),
        ('AL', 'Alagoas'),
        ('SE', 'Sergipe'),
        ('RN', 'Rio Grande do Norte'),
        ('PB', 'Paraíba'),
        ('ES', 'Espírito Santo'),
        ('AC', 'Acre'),
        ('AP', 'Amapá'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
    ]
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, choices=STATE_CHOICES)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.street}, {self.city}, {self.state}, {self.country}'
    
    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        
class Phone(models.Model):
    user = models.ForeignKey(User, related_name='phones', on_delete=models.CASCADE)
    number = models.CharField(max_length=15)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Phone'
        verbose_name_plural = 'Phones'
        unique_together = ('user', 'number')

class Email(models.Model):
    user = models.ForeignKey(User, related_name='emails', on_delete=models.CASCADE)
    address = models.EmailField(unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'
        unique_together = ('user', 'address')
        
class SocialMedia(models.Model):
    user = models.ForeignKey(User, related_name='social_medias', on_delete=models.CASCADE, unique=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.user}: {self.facebook}, {self.twitter}, {self.instagram}'

    class Meta:
        verbose_name = 'Social Media'
        verbose_name_plural = 'Social Media'