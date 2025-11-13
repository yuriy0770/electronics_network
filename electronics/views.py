from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch

from .models import NetworkNode
from .serializers import (
    NetworkNodeSerializer,
    NetworkNodeCreateUpdateSerializer
)
from .filters import NetworkNodeFilter
from .permissions import IsActiveEmployee


class NetworkNodeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend]
    filterset_class = NetworkNodeFilter

    def get_queryset(self):
        queryset = NetworkNode.objects.all().select_related(
            'contact', 'supplier'
        ).prefetch_related(
            Prefetch('products')
        )
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return NetworkNodeCreateUpdateSerializer
        return NetworkNodeSerializer

    def perform_update(self, serializer):
        if 'debt_to_supplier' in serializer.validated_data:
            raise serializers.ValidationError({
                'debt_to_supplier': 'Обновление этого поля через API запрещено'
            })
        serializer.save()

    @action(detail=False, methods=['get'])
    def stats(self, request):
        stats = {
            'total_nodes': NetworkNode.objects.count(),
            'factories': NetworkNode.objects.filter(node_type='factory').count(),
            'retail_chains': NetworkNode.objects.filter(node_type='retail').count(),
            'entrepreneurs': NetworkNode.objects.filter(node_type='entrepreneur').count(),
        }
        return Response(stats)
