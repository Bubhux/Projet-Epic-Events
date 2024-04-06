from rest_framework import permissions
from django.http import Http404

from profiles.models import User, Client


class EventPermissions(permissions.BasePermission):
    """
        Classe de permission personnalisée pour la vue du CRM gérant les opérations CRUD sur les objets Event.
        Cette classe contrôle l'accès aux opérations CRUD
        sur les objets Event en fonction du rôle de l'utilisateur connecté.

        - 'ROLE_MANAGEMENT': Rôle pour les menbres de l'équipe gestion.
        - 'ROLE_SALES': Rôle pour les membres de l'équipe commerciale.
        - 'ROLE_SUPPORT' Rôle pour les menbres de l'équipe support.

        Méthode has_create_permission:
            Autorise la création d'un nouvel événement uniquement
            pour les membres de l'équipe commerciale associés au client concerné.

        Méthode has_update_permission:
            Autorise les menbres de l'équipe gestion pour la mise à jour d'un événement spécifique.
            Autorise les menbres de l'équipe support
            pour la mise à jour d'un événement spécifique dont ils sont responsables.

        Méthode has_delete_permission:
            Autorise les menbres de l'équipe gestion pour la suppression d'un contrat spécifique.
            Autorise les menbres de l'équipe support
            pour la suppression d'un événement spécifique dont ils sont responsables.

        Méthode has_permission:
            - Récupère l'événement spécifié par la clé primaire 'event_pk' dans l'URL.
            - Si 'event_pk' n'est pas spécifié dans l'URL, l'accès est autorisé sans restriction de permission.
            - Pour les méthodes sécurisées (GET, HEAD, OPTIONS),
              autorise l'accès uniquement aux membres de l'équipe de gestion.
            - Pour les autres méthodes (POST, PUT, DELETE),
              vérifie si l'utilisateur connecté est menbre de l'équipe gestion
              ou menbre de l'équipe commerciale ou membre de l'équipe support.
            - Pour la création (POST), autorise uniquement les membres de l'équipe de commerciale.

        Notez que le rôle de l'utilisateur est utilisé pour déterminer les permissions,
        avec des autorisations spécifiques pour l'équipe de gestion, l'équipe commerciale et l'équipe support.
    """
    def has_create_permission(self, request):
        # Vérifie si l'utilisateur connecté a la permission de créer un nouvel événement.
        # Autorise uniquement si le membres de l'équipe commerciale est associés au client concerné.
        if request.user.role == User.ROLE_SALES:
            client_name = request.data.get('client')
            if client_name:
                client = Client.objects.filter(full_name=client_name).first()
                if client and client.sales_contact == request.user:
                    return True
        return False

    def has_update_permission(self, request, user):
        # Vérifie si l'utilisateur connecté a la permission de mettre à jour un événement spécifique.
        # Autorise les membres de l'équipe gestion et les membres de l'équipe support associés aux événements.
        return (
            request.user.role == User.ROLE_MANAGEMENT or (
                request.user.role == User.ROLE_SUPPORT and (
                    request.user == user or (
                        hasattr(user, 'client') and request.user in user.event.support_contact.all()
                    )
                )
            )
        )

    def has_delete_permission(self, request, user):
        # Vérifie si l'utilisateur connecté a la permission de supprimer un événement spécifique.
        # Autorise les membres de l'équipe gestion et les membres de l'équipe support associés aux événements.
        return (
            request.user.role == User.ROLE_MANAGEMENT or (
                request.user.role == User.ROLE_SUPPORT and (
                    request.user == user or (
                        hasattr(user, 'client') and request.user in user.event.support_contact.all()
                    )
                )
            )
        )

    def has_permission(self, request, view):
        try:
            event_pk = view.kwargs.get('event_pk')

            # Si 'event_pk' n'est pas spécifié dans l'URL, l'accès est autorisé sans restriction de permission
            if not event_pk:
                return True

            # Méthodes sécurisées : GET, HEAD, OPTIONS
            if request.method in permissions.SAFE_METHODS:
                # Autorise l'accès uniquement aux membres de l'équipe gestion et de l'équipe support
                return request.user.role in [User.ROLE_MANAGEMENT, User.ROLE_SUPPORT]

            # Méthodes non sécurisées : POST, PUT, DELETE
            # Vérifie si l'utilisateur connecté est membre de l'équipe gestion ou de léquipe support
            return request.user.role in [User.ROLE_MANAGEMENT, User.ROLE_SUPPORT]

        except Http404:
            # Si l'objet event_pk n'est pas trouvé, l'accès est refusé
            return False
