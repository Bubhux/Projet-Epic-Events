from django.http import HttpResponseForbidden
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from .models import Event
from .permissions import EventPermissions
from .serializers import MultipleSerializerMixin, EventListSerializer, EventDetailSerializer
from contracts.models import Contract


class AdminEventiewSet(MultipleSerializerMixin, ModelViewSet):

    serializer_class = EventListSerializer
    detail_serializer_class = EventDetailSerializer

    def get_queryset(self):
        return Event.objects.all()

@method_decorator(csrf_protect, name='dispatch')
class EventViewSet(MultipleSerializerMixin, ModelViewSet):
    """ViewSet pour gérer les opérations CRUD sur les objets Event (CRM)."""

    def __init__(self, *args, **kwargs):
        """
            Initialise une nouvelle instance de EventViewSet.

            Args:
                *args: Arguments positionnels.
                **kwargs: Arguments nommés.

            Cette méthode appelle d'abord le constructeur de la classe parente (super) 
            avec les arguments reçus, puis initialise les permissions de l'événement.
        """
        super().__init__(*args, **kwargs)
        self.initialize_event_permissions()

    queryset = Event.objects.all()
    serializer_class = EventListSerializer
    permission_classes = [IsAuthenticated, EventPermissions]

    serializers = {
        'list': EventListSerializer,
        'retrieve': EventDetailSerializer,
        'create': EventDetailSerializer,
        'update': EventDetailSerializer
    }

    event_permissions = None

    def initialize_event_permissions(self):
        """Initialise l'objet EventPermissions."""
        if self.event_permissions is None:
            self.event_permissions = EventPermissions()

    @action(detail=False, methods=['GET'])
    def events_list(self, request):
        """Renvoie tous les événements associé à l'utilisateur connecté."""
        events = Event.objects.filter(support_contact=request.user)
        serializer = EventDetailSerializer(events, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def event_details(self, request, pk=None):
        """Renvoie les détails d'un événement spécifique associé à l'utilisateur."""
        event = self.get_object()

        # Vérifie si l'événement appartient à l'utilisateur actuellement authentifié
        if event.support_contact != request.user:
            return HttpResponseForbidden("You do not have permission to access this event.")

        serializer = EventDetailSerializer(event)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def all_events_details(self, request):
        """Renvoie les détails de tous les événements."""
        events = Event.objects.all()
        serializer = EventDetailSerializer(events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def events_without_support(self, request):
        """Renvoie tous les événements qui n'ont pas de support associé."""
        events_without_support = Event.objects.filter(support_contact=None)
        serializer = EventDetailSerializer(events_without_support, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Crée un nouvel événement."""
        if not self.event_permissions.has_create_permission(request):
            return HttpResponseForbidden("You do not have permission to create an event.")

        # Récupérer les données de la requête
        data = request.data

        # Vérifier si le contrat associé est signé
        contract_id = data.get('contract')
        contract = get_object_or_404(Contract, id=contract_id)
        if not contract.status_contract:
            return HttpResponseForbidden("The associated contract is not signed. Cannot create the event.")

        # Vérifier si un événement existe déjà pour ce contrat
        existing_event = Event.objects.filter(contract=contract).first()
        if existing_event:
            return HttpResponseForbidden("An event already exists for this contract. Cannot create another event.")

        # Créer l'événement uniquement si le contrat est signé
        serializer = self.serializers['create'](data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        success_message = "Event successfully created."
        return Response({"message": success_message, "data": serializer.data}, status=201, headers=headers)

    def update(self, request, *args, **kwargs):
        """Met à jour un événement existant."""
        instance = self.get_object()
        if not self.event_permissions.has_update_permission(request, instance.support_contact):
            return HttpResponseForbidden("You do not have permission to update this event.")

        serializer = self.serializers['update'](instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        success_message = "Event successfully updated."
        return Response({"message": success_message, "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        """Supprime un événement existant."""
        instance = self.get_object()
        if not self.event_permissions.has_delete_permission(request, instance.support_contact):
            return HttpResponseForbidden("You do not have permission to delete this event.")

        self.perform_destroy(instance)
        success_message = "Event successfully deleted."
        return Response({"message": success_message}, status=204)
