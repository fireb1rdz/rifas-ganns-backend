from django.contrib import admin
from .models import RaffleConfiguration
# Register your models here.
@admin.register(RaffleConfiguration)
class RaffleConfigurationAdmin(admin.ModelAdmin):
    list_display = ('raffle', 'notify_winner_by_email',)
    list_filter = ('notify_winner_by_email',)
    search_fields = ('raffle__title',)
    ordering = ('raffle',)