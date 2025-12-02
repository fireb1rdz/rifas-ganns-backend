from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    SCOPE_CHOICES = [
        ('client', 'Cliente'),
        ('admin', 'Admin'),
        ('seller', 'Vendedor'),
    ]
    cpf = models.CharField(max_length=11, unique=True, blank=True, null=True, verbose_name="CPF")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Data de nascimento")
    lucky_number = models.PositiveIntegerField(blank=True, null=True, verbose_name="Número da sorte")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name="Foto de perfil")
    bio = models.TextField(blank=True, null=True, verbose_name="Biografia")
    is_verified = models.BooleanField(default=False, verbose_name="Verificado")
    scope = models.CharField(max_length=10, choices=SCOPE_CHOICES, default='client', verbose_name="Escopo")
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name="Slug")

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.username.lower().replace(' ', '-')
        super().save(*args, **kwargs)
    
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
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE, verbose_name="Usuário")
    street = models.CharField(max_length=255, verbose_name="Rua")
    city = models.CharField(max_length=100, verbose_name="Cidade")
    state = models.CharField(max_length=100, choices=STATE_CHOICES, verbose_name="Estado")
    zip_code = models.CharField(max_length=20, verbose_name="CEP")
    country = models.CharField(max_length=100, verbose_name="País")

    def __str__(self):
        return f'{self.street}, {self.city}, {self.state}, {self.country}'
    
    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
        
class Phone(models.Model):
    user = models.ForeignKey(User, related_name='phones', on_delete=models.CASCADE, verbose_name="Usuario")
    number = models.CharField(max_length=15, verbose_name="Número")
    description = models.CharField(max_length=100, blank=True, null=True, verbose_name="Descrição")

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Telefone'
        verbose_name_plural = 'Telefones'
        unique_together = ('user', 'number')

class Email(models.Model):
    user = models.ForeignKey(User, related_name='emails', on_delete=models.CASCADE, verbose_name="Usuário")
    address = models.EmailField(unique=True, verbose_name="Endereço")
    description = models.CharField(max_length=100, blank=True, null=True, verbose_name="Descrição")

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'
        unique_together = ('user', 'address')
        
class SocialMedia(models.Model):
    user = models.OneToOneField(User, related_name='social_medias', on_delete=models.CASCADE, unique=True, verbose_name="Usuário")
    facebook = models.CharField(max_length=100, blank=True, null=True, verbose_name="Facebook")
    twitter = models.CharField(max_length=100, blank=True, null=True, verbose_name="X")
    instagram = models.CharField(max_length=100, blank=True, null=True, verbose_name="Instagram")

    def __str__(self):
        return f'{self.user}: {self.facebook}, {self.twitter}, {self.instagram}'

    class Meta:
        verbose_name = 'Mídia social'
        verbose_name_plural = 'Mídias sociais'
        
        