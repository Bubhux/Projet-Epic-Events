from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from django.http import Http404

from .models import User, Client


class ClientPermissions(permissions.BasePermission):
    """
    Classe de permission personnalisée pour la vue de l'API gérant les opérations CRUD sur les objets Client.
    Cette classe contrôle l'accès aux opérations CRUD sur les objets Client en fonction du rôle de l'utilisateur connecté.

    Méthode has_permission:
        - Récupère le client spécifié par la clé primaire 'client_pk' dans l'URL.
        - Si 'client_pk' n'est pas spécifié dans l'URL, l'accès est autorisé sans restriction de permission.
        - Pour les méthodes sécurisées (GET, HEAD, OPTIONS), autorise l'accès aux gestionnaires de clients et aux membres de l'équipe de support.
        - Pour les autres méthodes (POST, PUT, DELETE), vérifie si l'utilisateur connecté est le gestionnaire du client ou membre de l'équipe de gestion.
        - Pour la création (POST), autorise uniquement les membres de l'équipe de gestion et l'équipe support.

    Notez que le rôle de l'utilisateur est utilisé pour déterminer les permissions, avec des autorisations spécifiques pour l'équipe de gestion et l'équipe de support.
    """
    def has_create_permission(self, request):
        # Vérifier si l'utilisateur connecté a la permission de créer un nouveau client
        return request.user.role in [User.ROLE_MANAGEMENT, User.ROLE_SUPPORT]

    def has_update_permission(self, request, user):
        # Vérifier si l'utilisateur connecté a la permission de mettre à jour un client spécifique
        return request.user.role == User.ROLE_MANAGEMENT or request.user == user

    def has_delete_permission(self, request, user):
        # Vérifier si l'utilisateur connecté a la permission de supprimer un client spécifique
        return request.user.role == User.ROLE_MANAGEMENT or request.user == user

    def has_permission(self, request, view):
        try:
            client_pk = view.kwargs.get('client_pk')

            # Si 'client_pk' n'est pas spécifié dans l'URL, l'accès est autorisé sans restriction de permission
            if not client_pk:
                return True

            client = get_object_or_404(Client, id=client_pk)
            # Méthodes sécurisées : GET, HEAD, OPTIONS
            if request.method in permissions.SAFE_METHODS:
                # Autorise l'accès aux gestionnaires de clients et aux membres de l'équipe de support
                if request.user.role == User.ROLE_MANAGEMENT or request.user.role == User.ROLE_SUPPORT:
                    return True
                # Vérifie si l'utilisateur connecté est le gestionnaire du client pour les méthodes sécurisées
                return client.user_contact == request.user

            # Méthodes non sécurisées : POST, PUT, DELETE
            # Vérifie si l'utilisateur connecté est le gestionnaire du client ou membre de l'équipe de gestion
            if request.user.role == User.ROLE_MANAGEMENT:
                return True
            return request.user == client.user_contact

        except Http404:
            # Si l'objet client_pk n'est pas trouvé, l'accès est refusé (aucune restriction de permission)
            return False


class UserPermissions(permissions.BasePermission):
    """
    Classe de permission personnalisée pour la vue de l'API gérant les opérations CRUD sur les objets User.
    Cette classe contrôle l'accès aux opérations CRUD sur les objets User en fonction du rôle de l'utilisateur connecté.

    Méthode has_permission:
        - Récupère l'utilisateur spécifié par la clé primaire 'user_pk' dans l'URL.
        - Si 'user_pk' n'est pas spécifié dans l'URL, l'accès est autorisé sans restriction de permission.
        - Pour les méthodes sécurisées (GET, HEAD, OPTIONS), autorise l'accès aux gestionnaires des utilisateurs s'ils sont membres de l'équipe gestion.
        - Pour les autres méthodes (POST, PUT, DELETE), vérifie si l'utilisateur connecté est le gestionnaire des utilisateurs s'il est membre de l'équipe de gestion.
        - Pour la création (POST), autorise uniquement les membres de l'équipe de gestion.

    Notez que le rôle de l'utilisateur est utilisé pour déterminer les permissions, avec des autorisations spécifiques pour l'équipe de gestion.
    """
    def has_create_permission(self, request):
        # Vérifier si l'utilisateur connecté a la permission de créer un nouvel utilisateur
        return request.user.role == User.ROLE_MANAGEMENT

    def has_update_permission(self, request, user):
        # Vérifier si l'utilisateur connecté a la permission de mettre à jour un utilisateur spécifique
        return request.user.role == User.ROLE_MANAGEMENT

    def has_delete_permission(self, request, user):
        # Vérifier si l'utilisateur connecté a la permission de supprimer un utilisateur spécifique
        return request.user.role == User.ROLE_MANAGEMENT

    def has_permission(self, request, view):
        try:
            user_pk = view.kwargs.get('user_pk')

            # Si 'user_pk' n'est pas spécifié dans l'URL, l'accès est autorisé sans restriction de permission
            if not user_pk:
                return True

            user = get_object_or_404(User, id=user_pk)
            # Méthodes sécurisées : GET, HEAD, OPTIONS
            if request.method in permissions.SAFE_METHODS:
                # Autoriser l'accès aux gestionnaires des utilisateurs s'ils sont membres de l'équipe de gestion
                return user.role == User.ROLE_MANAGEMENT

            # Vérifier les permissions pour les méthodes non sécurisées (POST, PUT, DELETE)
            else:
                # Vérifier si l'utilisateur connecté est le gestionnaire des utilisateurs s'il est membre de l'équipe de gestion
                if request.method == 'POST':
                    # Autoriser la création uniquement pour les membres de l'équipe de gestion
                    return user.role == User.ROLE_MANAGEMENT
                else:
                    return user.role == User.ROLE_MANAGEMENT

        except Http404:
            # Si l'objet user_pk n'est pas trouvé, l'accès est refusé (aucune restriction de permission)
            return False
