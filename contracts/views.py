from django.http import HttpResponseForbidden
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from .models import Contract
from .permissions import ContractPermissions
from .serializers import MultipleSerializerMixin, ContractListSerializer, ContractDetailSerializer, ContractCreateUpdateSerializer


class AdminContractViewSet(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer

    def get_queryset(self):
        return Contract.objects.all()


class ContractViewSet(MultipleSerializerMixin, ModelViewSet):
    """ViewSet pour gérer les opérations CRUD sur les objets Contract (CRM)."""

    def __init__(self, *args, **kwargs):
        """
            Initialise une nouvelle instance de ContractViewSet.

            Args:
                *args: Arguments positionnels.
                **kwargs: Arguments nommés.

            Cette méthode appelle d'abord le constructeur de la classe parente (super) 
            avec les arguments reçus, puis initialise les permissions du contrat.
        """
        super().__init__(*args, **kwargs)
        self.initialize_contract_permissions()

    queryset = Contract.objects.all()
    serializer_class = ContractListSerializer
    permission_classes = [IsAuthenticated, ContractPermissions]

    serializers = {
        'list': ContractListSerializer,
        'retrieve': ContractDetailSerializer,
        'create': ContractCreateUpdateSerializer,
        'update': ContractCreateUpdateSerializer
    }

    contract_permissions = None

    def initialize_contract_permissions(self):
        """Initialise l'objet ContractPermissions."""
        if self.contract_permissions is None:
            self.contract_permissions = ContractPermissions()

    @action(detail=False, methods=['GET'])
    def contracts_list(self, request):
        """Renvoie tous les contrats."""
        contracts = Contract.objects.filter(sales_contact=request.user)
        serializer = ContractDetailSerializer(contracts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def contract_details(self, request, pk=None):
        """Renvoie les détails d'un contrat spécifique associé à l'utilisateur."""
        contract = self.get_object()

        # Vérifie si le contrat appartient à l'utilisateur actuellement authentifié
        if contract.sales_contact != request.user:
            return HttpResponseForbidden("You do not have permission to access this contract.")

        serializer = ContractDetailSerializer(contract)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def all_contracts_details(self, request):
        """Renvoie les détails de tous les contrats."""
        contracts = Contract.objects.all()
        serializer = ContractDetailSerializer(contracts, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Crée un nouveau contrat."""
        if not self.contract_permissions.has_create_permission(request):
            return HttpResponseForbidden("You do not have permission to create a contract.")

        serializer = self.serializers['create'](data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        success_message = "Contract successfully created."
        return Response({"message": success_message, "data": serializer.data}, status=201, headers=headers)

    def update(self, request, *args, **kwargs):
        """Met à jour un contrat existant."""
        instance = self.get_object()
        if not self.contract_permissions.has_update_permission(request, instance.sales_contact):
            return HttpResponseForbidden("You do not have permission to update this contract.")

        serializer = self.serializers['update'](instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        success_message = "Contract successfully updated."
        return Response({"message": success_message, "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        """Supprime un contrat existant."""
        instance = self.get_object()
        if not self.contract_permissions.has_delete_permission(request, instance.sales_contact):
            return HttpResponseForbidden("You do not have permission to delete this contract.")

        self.perform_destroy(instance)
        success_message = "Contract successfully deleted."
        return Response({"message": success_message}, status=204)
