from django.contrib.auth import authenticate, login
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from .models import User, Client
from .permissions import ClientPermissions
from .serializers import MultipleSerializerMixin, UserLoginSerializer, ClientListSerializer, ClientDetailSerializer, UserDetailSerializer


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
    permission_classes = [IsAuthenticated, ClientPermissions]

    serializers = {
        'list': ClientListSerializer,
        'retrieve': ClientDetailSerializer,
    }

    @action(detail=False, methods=['GET'])
    def client_list(self, request):

        clients = Client.objects.filter(user_contact=request.user)
        serializer = ClientListSerializer(clients, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def client_details(self, request, pk=None):
        """Renvoie les détails d'un client spécifique."""
        client = self.get_object()
        serializer = ClientDetailSerializer(client)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def all_details(self, request):
        """Renvoie les détails de tous les clients."""
        clients = Client.objects.all()
        serializer = ClientDetailSerializer(clients, many=True)
        return Response(serializer.data)


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
