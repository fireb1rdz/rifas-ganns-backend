from django.contrib import admin
from .models import RaffleConfiguration, GatewayConfiguration, GatewayRequiredCustomerFields
# Register your models here.
@admin.register(RaffleConfiguration)
class RaffleConfigurationAdmin(admin.ModelAdmin):
    list_display = ('raffle', 'notify_winner_by_email',)
    list_filter = ('notify_winner_by_email',)
    search_fields = ('raffle__title',)
    ordering = ('raffle',)

@admin.register(GatewayConfiguration)
class GatewayConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    list_max_show_all = 50

@admin.register(GatewayRequiredCustomerFields)
class GatewayRequiredCustomerFieldsAdmin(admin.ModelAdmin):
    list_display = ('gateway', 'required_field_name')
    list_max_show_all = 50