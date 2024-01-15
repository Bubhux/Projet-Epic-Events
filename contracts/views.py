from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import action


from .models import Contract
from profiles.serializers import MultipleSerializerMixin


class ContractClientViewSet(MultipleSerializerMixin, ModelViewSet):
    """ViewSet d'API pour gérer les contrats d'un objet Client spécifique."""

    # serializer_class = ContractListSerializer
    # detail_serializer_class = ContractDetailSerializer
    # permission_classes = [IsAuthenticated, ContractPermissions]

    def get_contract(self, contract_pk):
        """Récupère l'objet Contract spécifié par la clé primaire passée dans l'URL."""
        return get_object_or_404(Contract, id=contract_pk)

    def get_queryset(self):
        """Renvoie les contrats associées à l'objet Client spécifié dans l'URL."""
        contract_pk = self.kwargs.get('contract_pk')
        coontract = self.get_project(conrtract_pk)
        return Contract.objects.filter(client=client)

    def perform_create(self, serializer):
        """Sauvegarde un nouvel objet Contract associé à l'objet Client spécifié et à l'auteur actuellement connecté."""
        contract_pk = self.kwargs.get('contract_pk')
        contract = self.get_contract(contract_pk)
        assignee_id = self.request.data.get('assignee')
        print(f"Assignee ID from request data: {assignee_id}")
        if assignee_id:
            try:
                assignee = get_user_model().objects.get(id=assignee_id)
                serializer.save(client=client, author=self.request.user, assignee=assignee)
                print(f"Assignee found: {assignee}")
            except get_user_model().DoesNotExist:
                print("Assignee not found")
                try:
                    assignee = get_user_model().objects.get(id=assignee_id)
                except get_user_model().DoesNotExist:
                    raise serializers.ValidationError("Invalid assignee ID")
        else:
            serializer.save(project=project, author=self.request.user)

    def update(self, request, client_pk, pk):
        """Met à jour l'objet Contract spécifié associé à l'objet Client spécifié."""
        contract = self.get_object()
        serializer = self.serializer_class(contract, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def create(self, request, client_pk):
        """Crée un nouvel objet Contract associé à l'objet Client spécifié."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, client_pk, pk):
        """Supprime l'objet Contract spécifié associé à l'objet Client spécifié."""
        contract = self.get_object()
        contract.delete()
        return Response('Contract successfully deleted.', status=status.HTTP_204_NO_CONTENT)
