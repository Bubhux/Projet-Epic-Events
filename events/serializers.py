from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer

from .models import Event
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


class EventListSerializer(serializers.ModelSerializer):
    """
        Serializer pour la liste des événements.
        Ce serializer est utilisé pour représenter les données de la liste des événements dans le CRM.

        Champs :
        - 'id': Identifiant unique du événement.
        - 'client': Nom complet du client.
        - 'support_contact': Nom complet du menbre de l'équipe support.
    """
    client = serializers.ReadOnlyField(source='client.full_name')
    support_contact = serializers.ReadOnlyField(source='support_contact.full_name')

    class Meta:
        model = Event
        fields = ['id', 'client', 'support_contact']


class EventDetailSerializer(serializers.ModelSerializer):
    """
        Serializer pour les détails d'un événement.
        Ce serializer est utilisé pour représenter les détails d'un événement spécifique dans le CRM.

        Champs :
        - 'id': Identifiant unique du événement.
        - 'event_name': Nom de l'événement.
        - 'client': Nom complet du client associé à l'événement.
        - 'contract': ID du contrat associé à l'événement.
        - 'event_date_start': Date de début de l'événement.
        - 'event_date_end': Date de fin de l'événement.
        - 'support_contact': Nom complet du membre de l'équipe support associé à l'événement.
        - 'location': Lieu de l'événement.
        - 'attendees': Nombre d'invités prévu.
        - 'notes': Notes ou détails supplémentaires sur l'événement.
    """
    # Champs utilisant SlugRelatedField pour la lecture et l'écriture
    client = serializers.SlugRelatedField(slug_field='full_name', queryset=Client.objects.all())
    support_contact = serializers.SlugRelatedField(
        slug_field='full_name', queryset=User.objects.filter(role=User.ROLE_SUPPORT)
    )

    class Meta:
        model = Event
        fields = ['id', 'event_name', 'client', 'client_contact', 'contract', 'event_date_start',
                  'event_date_end', 'support_contact', 'location', 'attendees', 'notes']
