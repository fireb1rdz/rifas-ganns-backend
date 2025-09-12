from django.contrib import admin
from .models import RaffleConfiguration
# Register your models here.
@admin.register(RaffleConfiguration)
class RaffleConfigurationAdmin(admin.ModelAdmin):
    list_display = ('raffle', 'notify_winner_by_email', 'use_manual_percentage')
    list_filter = ('notify_winner_by_email', 'use_manual_percentage')
    search_fields = ('raffle__title',)
    ordering = ('raffle',)