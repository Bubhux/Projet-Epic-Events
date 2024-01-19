from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer

from .models import Contract
from profiles.models import User, Client


class MultipleSerializerMixin:
    """
        Mixin pour utiliser plusieurs classes de sérialiseur dans une vue.

        Par défaut, la variable detail_serializer_class est définie sur None.
        Ce qui signifie qu'il n'y a pas de sérialiseur spécifique défini pour les actions de type
        "retrieve", "create", "update" et "destroy".
    """
    detail_serializer_class = None

    def get_serializer_class(self):
        """
            Retourne la classe du sérialiseur en fonction de l'action de la vue.

            Si l'action est 'retrieve', 'create', 'update' ou 'destroy' et qu'un sérialiseur détaillé
            est spécifié, retourne le sérialiseur détaillé. Sinon, retourne le sérialiseur par défaut.
        """
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
            - 'client': Nom complet du client associé au contrat.
            - 'sales_contact': Nom complet du contact commercial associé au contrat.
            - 'status_contract': Statut du contrat (signé ou non signé).
            - 'total_amount': Montant total du contrat.
            - 'remaining_amount': Montant restant à payer sur le contrat.
            - 'creation_date': Date de création du contrat.
            - 'update_date': Date de mise à jour du contrat.
            - 'client': Un SlugRelatedField représentant le client associé au contrat.
                        Il permet de spécifier le client en utilisant son nom complet.
            - 'sales_contact': Un SlugRelatedField représentant le contact commercial associé au contrat.
                        Il permet de spécifier le contact commercial en utilisant son nom complet.
    """
    # Champs utilisant SlugRelatedField pour la lecture et l'écriture
    client = serializers.SlugRelatedField(slug_field='full_name', queryset=Client.objects.all())
    sales_contact = serializers.SlugRelatedField(
        slug_field='full_name', queryset=User.objects.filter(role=User.ROLE_SALES)
    )

    class Meta:
        model = Contract
        fields = ['id', 'client', 'sales_contact', 'status_contract', 'total_amount',
                  'remaining_amount', 'creation_date', 'update_date']
