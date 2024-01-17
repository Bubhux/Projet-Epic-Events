from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer

from .models import Contract


class MultipleSerializerMixin:
    """Mixin pour utiliser plusieurs classes de sérialiseur dans une vue."""

    # Par défaut, la variable detail_serializer_class est définie sur None.
    # Ce qui signifie qu'il n'y a pas de sérialiseur spécifique défini pour les actions de type
    # "retrieve", "create", "update" et "destroy".
    detail_serializer_class = None

    def get_serializer_class(self):
        if (self.action == 'retrieve' or
                self.action == 'create' or
                self.action == 'update' or
                self.action == 'destroy') and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ContractListSerializer(serializers.ModelSerializer):
    """
        Serializer pour la liste des contrats.
        Ce serializer est utilisé pour représenter les données de la liste des contrats dans le CRM.
    """
    class Meta:
        model = Contract
        fields = ['client', 'id', 'sales_contact']


class ContractDetailSerializer(serializers.ModelSerializer):
    """
        Serializer pour les détails d'un contrat.
        Ce serializer est utilisé pour représenter les détails d'un contrat spécifique dans le CRM.
    """
    class Meta:
        model = Contract
        fields = ['client', 'id', 'sales_contact', 'status_contract', 'total_amount',
                  'remaining_amount', 'creation_date', 'update_date']
