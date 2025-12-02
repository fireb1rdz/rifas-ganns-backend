from django_filters import rest_framework as filters
from .models import Raffle

class RaffleFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")
    description = filters.CharFilter(lookup_expr="icontains")
    created_by = filters.CharFilter(field_name="created_by__username", lookup_expr="icontains")
    created_at = filters.DateFromToRangeFilter()
    draw_date = filters.DateFromToRangeFilter()
    prize_value = filters.RangeFilter()
    quota_value = filters.RangeFilter()
    
    class Meta:
        model = Raffle
        fields = ["title", "description", "created_at",
                  "draw_date", "prize_value", "quota_value", "created_by"]