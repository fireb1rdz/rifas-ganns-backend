from django.contrib import admin
from .models import Raffle, Quota, RafflePicture

@admin.register(Raffle)
class RaffleAdmin(admin.ModelAdmin):
    list_display = ('title', 'draw_date', 'prize_value', 'quota_value', 'winner', 'awarded_at')
    list_filter = ('draw_date', 'awarded_at')
    search_fields = ('title',)
    readonly_fields = ('created_at',)
    ordering = ('-draw_date',)

@admin.register(Quota)
class QuotaAdmin(admin.ModelAdmin):
    list_display = ('raffle', 'number', 'owner', 'bought_at', 'is_winner')
    list_filter = ('raffle', 'is_winner')
    search_fields = ('raffle__title', 'owner__username')
    readonly_fields = ('bought_at',)
    ordering = ('raffle', 'number')

@admin.register(RafflePicture)
class RafflePictureAdmin(admin.ModelAdmin):
    list_display = ('raffle', 'main', 'uploaded_at')
    list_filter = ('main', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    ordering = ('-uploaded_at',)
