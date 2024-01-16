from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from .models import User, Client
from .permissions import ClientPermissions, UserPermissions
from .serializers import MultipleSerializerMixin, UserLoginSerializer, ClientListSerializer, ClientDetailSerializer, UserListSerializer, UserDetailSerializer


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
    """ViewSet pour gérer les opérations CRUD sur les objets Client (CRM)."""

    queryset = Client.objects.all()
    serializer_class = ClientListSerializer
    permission_classes = [IsAuthenticated, ClientPermissions]

    serializers = {
        'list': ClientListSerializer,
        'retrieve': ClientDetailSerializer,
    }

    @action(detail=False, methods=['GET'])
    def client_list(self, request):
        """Renvoie tous les clients."""
        clients = Client.objects.filter(user_contact=request.user)
        serializer = ClientDetailSerializer(clients, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def client_details(self, request, pk=None):
        """Renvoie les détails d'un client spécifique."""
        client = self.get_object()
        serializer = ClientDetailSerializer(client)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def all_clients_details(self, request):
        """Renvoie les détails de tous les clients."""
        clients = Client.objects.all()
        serializer = ClientDetailSerializer(clients, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Crée un nouveau client."""
        if not self.request.user.has_create_permission(request):
            return HttpResponseForbidden("You do not have permission to create a client.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        success_message = "Client successfully created."
        return Response({"message": success_message, "data": serializer.data}, status=201, headers=headers)

    def update(self, request, *args, **kwargs):
        """Met à jour un client existant."""
        instance = self.get_object()
        if not self.request.user.has_update_permission(request, instance.user_contact):
            return HttpResponseForbidden("You do not have permission to update this client.")

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        success_message = "Client successfully updated."
        return Response({"message": success_message, "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        """Supprime un client existant."""
        instance = self.get_object()
        if not self.request.user.has_delete_permission(request, instance.user_contact):
            return HttpResponseForbidden("You do not have permission to delete this client.")

        self.perform_destroy(instance)
        success_message = "Client successfully deleted."
        return Response({"message": success_message}, status=204)


class UserViewSet(MultipleSerializerMixin, ModelViewSet):
    """ViewSet pour gérer les opérations CRUD sur les objets Utilisateur (CRM)."""

    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated, UserPermissions]

    serializers = {
        'list': UserListSerializer,
        'retrieve': UserDetailSerializer,
    }

    @action(detail=False, methods=['GET'])
    def user_list(self, request):
        """Renvoie tous les utilisateurs."""
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def user_details(self, request, pk=None):
        """Renvoie les détails d'un utilisateur spécifique."""
        user = self.get_object()
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def all_users_details(self, request):
        """Renvoie les détails de tous les utilisateurs."""
        users = User.objects.all()
        serializer = UserDetailSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Crée un nouvel utilisateur."""
        if not self.request.user.has_create_permission(request):
            return HttpResponseForbidden("You do not have permission to create a user.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        success_message = "User successfully created."
        return Response({"message": success_message, "data": serializer.data}, status=201, headers=headers)

    def update(self, request, *args, **kwargs):
        """Met à jour un utilisateur existant."""
        instance = self.get_object()
        if not self.request.user.has_update_permission(request, instance):
            return HttpResponseForbidden("You do not have permission to update this user.")

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        success_message = "User successfully updated."
        return Response({"message": success_message, "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        """Supprime un utilisateur existant."""
        instance = self.get_object()
        if not self.request.user.has_delete_permission(request, instance):
            return HttpResponseForbidden("You do not have permission to delete this user.")

        self.perform_destroy(instance)
        success_message = "User successfully deleted."
        return Response({"message": success_message}, status=204)
