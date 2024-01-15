from django.contrib.auth import authenticate, login
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from .models import User, Client
from .permissions import ClientPermissions
from .serializers import MultipleSerializerMixin, UserLoginSerializer, ClientListSerializer, ClientDetailSerializer


class LoginViewSet(generics.CreateAPIView):
    """
    Vue pour la connexion des utilisateurs.
    Cette vue permet à un utilisateur de se connecter en fournissant,
    une adresse e-mail, un mot de passe.
    l'utilisateur est authentifié pendant le processus de connexion.
    """
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        # Obtenir le sérialiseur avec les données de la requête
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Authentifier l'utilisateur avec le nom d'utilisateur (adresse e-mail) et le mot de passe
        user = authenticate(
            request,
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        # Vérifier si l'authentification a réussi et si l'utilisateur est actif
        if user and user.is_active:
            # Connecter l'utilisateur
            login(request, user)
            return Response({"detail": "Login successful"})
        else:
            # Retourner une réponse indiquant des identifiants invalides ou un compte inactif
            return Response({"detail": "Invalid credentials or account inactive"}, status=400)


class ClientViewSet(MultipleSerializerMixin, ModelViewSet):
    """ViewSet d'API pour gérer les opérations CRUD sur les objets Client."""

    queryset = Client.objects.all()
    serializer_class = ClientListSerializer
    detail_serializer_class = ClientDetailSerializer
    permission_classes = [IsAuthenticated, ClientPermissions]

    def perform_create(self, serializer):
        """Sauvegarde l'objet Client avec l'utilisateur actuellement connecté en tant que gestionnaire du client."""
        serializer.save(user_contact=self.request.user)

    @action(detail=False, methods=['GET'])
    def user_clients(self, request):
        """Renvoie tous les clients associés à l'utilsateur."""
        user = self.request.user
        clients = Client.objects.filter(user_contact=user)
        serializer = ClientListSerializer(clients, many=True)

        # Messages de débogage
        print(f"Utilisateur actuel : {user}")
        return Response(serializer.data)

    def put(self, request, pk=None):
        """Met à jour l'objet Client spécifié par la clé primaire passée dans l'URL."""
        client = self.get_object()
        data = request.data.copy()
        data['user_contact'] = client.user_contact.id
        serializer = ClientListSerializer(client, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, client_pk=None, pk=None):
        """Supprime l'objet Client spécifié par la clé primaire passée dans l'URL."""
        client = self.get_object()

        # Utilise la permission pour vérifier si l'utilisateur est l'auteur du projet
        if not self.request.user == client.user_contact:
            return Response("You don't have permission to delete this client.", status=status.HTTP_403_FORBIDDEN)

        client.delete()
        return Response('Client successfully deleted.', status=status.HTTP_204_NO_CONTENT)


class AllClientsDetailsViewSet(ModelViewSet):
    """ViewSet d'API pour afficher les détails de tous les clients."""

    queryset = Client.objects.all()
    serializer_class = ClientDetailSerializer
    permission_classes = [IsAuthenticated, ClientPermissions]

    @action(detail=False, methods=['GET'])
    def all_details(self, request):
        """Renvoie les détails de tous les clients."""
        clients = Client.objects.all()
        serializer = ClientDetailSerializer(clients, many=True)
        return Response(serializer.data)
