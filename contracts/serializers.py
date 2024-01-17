from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer

from .models import Contract
from profiles.models import User, Client


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


class ContractCreateUpdateSerializer(serializers.ModelSerializer):
    """
        Sérialiseur pour la création et la mise à jour d'instances de Contrat.

        Ce sérialiseur est utilisé pour gérer la création et la mise à jour d'objets Contrat
        au sein du CRM. Il inclut des champs permettant de spécifier le client, le contact commercial,
        le statut, le montant total et le montant restant.

        Champs :
        - 'client': Un SlugRelatedField représentant le client associé au contrat.
                    Il permet de spécifier le client en utilisant son nom complet.
        - 'sales_contact': Un SlugRelatedField représentant le contact commercial associé au contrat.
                        Il permet de spécifier le contact commercial en utilisant son nom complet.
        - 'status_contract': Un champ booléen représentant le statut du contrat.
        - 'total_amount': Un champ double représentant le montant total du contrat.
        - 'remaining_amount': Un champ double représentant le montant restant à payer sur le contrat.
    """
    client = serializers.SlugRelatedField(slug_field='full_name', queryset=Client.objects.all())
    sales_contact = serializers.SlugRelatedField(slug_field='full_name', queryset=User.objects.filter(role=User.ROLE_SALES))

    class Meta:
        model = Contract
        fields = ['client', 'sales_contact', 'status_contract', 'total_amount', 'remaining_amount']


class ContractListSerializer(serializers.ModelSerializer):
    """
        Serializer pour la liste des contrats.
        Ce serializer est utilisé pour représenter les données de la liste des contrats dans le CRM.

        Champs :
        - 'id': Identifiant unique du contrat.
        - 'client': Nom complet du client.
        - 'sales_contact': Nom complet du contact commercial.
    """
    client = serializers.ReadOnlyField(source='client.full_name')
    sales_contact = serializers.ReadOnlyField(source='sales_contact.full_name')

    class Meta:
        model = Contract
        fields = ['id', 'client', 'sales_contact']


class ContractDetailSerializer(serializers.ModelSerializer):
    """
        Serializer pour les détails d'un contrat.
        Ce serializer est utilisé pour représenter les détails d'un contrat spécifique dans le CRM.

        Champs :
        - 'id': Identifiant unique du contrat.
        - 'client': Nom complet du client.
        - 'sales_contact': Nom complet du contact commercial.
        - 'status_contract': Status du contrat.
        - 'total_amount': Montant total du contrat.
        - 'remaining_amount': Montant restant à payer sur le contrat.
        - 'creation_date': Date de création du contrat.
        - 'update_date': Date de mise à jour du contrat.
    """
    client = serializers.ReadOnlyField(source='client.full_name')
    sales_contact = serializers.ReadOnlyField(source='sales_contact.full_name')

    class Meta:
        model = Contract
        fields = ['id', 'client', 'sales_contact', 'status_contract', 'total_amount',
                  'remaining_amount', 'creation_date', 'update_date']
