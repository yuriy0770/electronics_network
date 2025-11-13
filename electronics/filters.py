import django_filters
from .models import NetworkNode


class NetworkNodeFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(
        field_name='contact__country',
        lookup_expr='icontains',
        label='Страна'
    )

    class Meta:
        model = NetworkNode
        fields = {
            'name': ['icontains'],
            'node_type': ['exact'],
            'level': ['exact'],
        }