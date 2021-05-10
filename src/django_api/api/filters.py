import django_filters
from .models import ElectricityConsumption


class DateTimeFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    until_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    from_time = django_filters.TimeFilter(field_name='time', lookup_expr='gte')
    until_time = django_filters.TimeFilter(field_name='time', lookup_expr='lte')

    class Meta:
        model = ElectricityConsumption
        fields = ['from_date', 'until_date', 'from_time', 'until_time']
