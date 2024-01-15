from rest_framework import permissions
from rest_framework.generics import get_object_or_404

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

    Notez que le rôle de l'utilisateur est utilisé pour déterminer les permissions, avec des autorisations spécifiques pour l'équipe de gestion et l'équipe de support.
    """
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
                return client in Client.objects.filter(user_contact=request.user)

            # Méthodes non sécurisées : POST, PUT, DELETE
            # Vérifie si l'utilisateur connecté est le gestionnaire du client ou membre de l'équipe de gestion
            if request.user.role == User.ROLE_MANAGEMENT:
                return True
            return request.user == client.user_contact

        except KeyError:
            # Si 'client_pk' n'est pas spécifié dans l'URL, l'accès est autorisé (aucune restriction de permission)
            return True
