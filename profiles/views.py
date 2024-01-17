from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from .models import User, Client
from .permissions import ClientPermissions, UserPermissions
from .serializers import MultipleSerializerMixin, UserLoginSerializer, ClientListSerializer, ClientDetailSerializer, UserListSerializer, UserDetailSerializer


class AdminUserLoginViewSet(MultipleSerializerMixin, ModelViewSet):

    serializer_class = UserLoginSerializer

    def get_queryset(self):
        return User.objects.all()


class AdminUserViewSet(MultipleSerializerMixin, ModelViewSet):

    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer

    def get_queryset(self):
        return User.objects.all()


class AdminUserClientViewSet(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ClientListSerializer
    detail_serializer_class = ClientDetailSerializer

    def get_queryset(self):
        return Client.objects.all()


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

    def __init__(self, *args, **kwargs):
        """
            Initialise une nouvelle instance de ClientViewSet.

            Args:
                *args: Arguments positionnels.
                **kwargs: Arguments nommés.

            Cette méthode appelle d'abord le constructeur de la classe parente (super) 
            avec les arguments reçus, puis initialise les permissions du contrat.
        """
        super().__init__(*args, **kwargs)
        self.initialize_client_permissions()

    queryset = Client.objects.all()
    serializer_class = ClientListSerializer
    permission_classes = [IsAuthenticated, ClientPermissions]

    serializers = {
        'list': ClientListSerializer,
        'retrieve': ClientDetailSerializer,
        'create' : ClientDetailSerializer,
        'update' : ClientDetailSerializer
    }

    client_permissions = None

    def initialize_client_permissions(self):
        """Initialise l'objet ClientPermissions."""
        if self.client_permissions is None:
            self.client_permissions = ClientPermissions()

    @action(detail=False, methods=['GET'])
    def clients_list(self, request):
        """Renvoie tous les clients."""
        clients = Client.objects.filter(user_contact=request.user)
        serializer = ClientDetailSerializer(clients, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def client_details(self, request, pk=None):
        """Renvoie les détails d'un client spécifique associé à l'utilisateur."""
        client = self.get_object()

        # Vérifie si le client appartient à l'utilisateur actuellement authentifié
        if client.user_contact != request.user:
            return HttpResponseForbidden("You do not have permission to access this client.")

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
        if not self.client_permissions.has_create_permission(request):
            return HttpResponseForbidden("You do not have permission to create a client.")

        serializer = self.serializers['create'](data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        success_message = "Client successfully created."
        return Response({"message": success_message, "data": serializer.data}, status=201, headers=headers)

    def update(self, request, *args, **kwargs):
        """Met à jour un client existant."""
        instance = self.get_object()
        if not self.client_permissions.has_update_permission(request, instance.user_contact):
            return HttpResponseForbidden("You do not have permission to update this client.")

        serializer = self.serializers['update'](instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        success_message = "Client successfully updated."
        return Response({"message": success_message, "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        """Supprime un client existant."""
        instance = self.get_object()
        if not self.client_permissions.has_delete_permission(request, instance.user_contact):
            return HttpResponseForbidden("You do not have permission to delete this client.")

        self.perform_destroy(instance)
        success_message = "Client successfully deleted."
        return Response({"message": success_message}, status=204)


class UserViewSet(MultipleSerializerMixin, ModelViewSet):
    """ViewSet pour gérer les opérations CRUD sur les objets Utilisateur (CRM)."""

    def __init__(self, *args, **kwargs):
        """
            Initialise une nouvelle instance de UserViewSet.

            Args:
                *args: Arguments positionnels.
                **kwargs: Arguments nommés.

            Cette méthode appelle d'abord le constructeur de la classe parente (super) 
            avec les arguments reçus, puis initialise les permissions du contrat.
        """
        super().__init__(*args, **kwargs)
        self.initialize_user_permissions()

    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated, UserPermissions]

    serializers = {
        'list': UserListSerializer,
        'retrieve': UserDetailSerializer,
        'create': UserDetailSerializer,
        'update': UserDetailSerializer,
    }

    user_permissions = None

    def initialize_user_permissions(self):
        """Initialise l'objet UserPermissions."""
        if self.user_permissions is None:
            self.user_permissions = UserPermissions()

    @action(detail=False, methods=['GET'])
    def users_list(self, request):
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
        if not self.user_permissions.has_create_permission(request.user):
            return HttpResponseForbidden("You do not have permission to create a user.")

        serializer = self.serializers['create'](data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        success_message = "User successfully created."
        return Response({"message": success_message, "data": serializer.data}, status=201, headers=headers)

    def update(self, request, *args, **kwargs):
        """Met à jour un utilisateur existant."""
        instance = self.get_object()
        if not self.user_permissions.has_update_permission(self.request.user, instance):
            return HttpResponseForbidden("You do not have permission to update this user.")

        serializer = self.serializers['update'](instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        success_message = "User successfully updated."
        return Response({"message": success_message, "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        """Supprime un utilisateur existant."""
        instance = self.get_object()
        if not self.user_permissions.has_delete_permission(self.request.user, instance):
            return HttpResponseForbidden("You do not have permission to delete this user.")

        self.perform_destroy(instance)
        success_message = "User successfully deleted."
        return Response({"message": success_message}, status=204)
