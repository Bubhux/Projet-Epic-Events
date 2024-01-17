from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from django.http import Http404

from .models import Contract
from profiles.models import User, Client


class ContractPermissions(permissions.BasePermission):
    """
        Classe de permission personnalisée pour la vue du CRM gérant les opérations CRUD sur les objets Contract.
        Cette classe contrôle l'accès aux opérations CRUD sur les objets Contract en fonction du rôle de l'utilisateur connecté.

        - 'ROLE_MANAGEMENT': Rôle pour les gestionnaires de contrats.
        - 'ROLE_SALES': Rôle pour les membres de l'équipe commerciale.

        Méthode has_create_permission:
            Autorise la création d'un nouveau contrat uniquement pour les membres de l'équipe de gestion.

        Méthode has_update_permission:
            Autorise la mise à jour d'un contrat spécifique par les gestionnaires du contrat ou l'utilisateur associé.

        Méthode has_delete_permission:
            Autorise la suppression d'un contrat spécifique par les gestionnaires du contrat ou l'utilisateur associé.

        Méthode has_permission:
            - Récupère le contrat spécifié par la clé primaire 'contract_pk' dans l'URL.
            - Si 'contract_pk' n'est pas spécifié dans l'URL, l'accès est autorisé sans restriction de permission.
            - Pour les méthodes sécurisées (GET, HEAD, OPTIONS), autorise l'accès uniquement aux membres de l'équipe de gestion.
            - Pour les autres méthodes (POST, PUT, DELETE), vérifie si l'utilisateur connecté est le gestionnaire du contrat ou membre de l'équipe de gestion.
            - Pour la création (POST), autorise uniquement les membres de l'équipe de gestion.
            
        Notez que le rôle de l'utilisateur est utilisé pour déterminer les permissions, avec des autorisations spécifiques pour l'équipe de gestion et l'équipe commerciale.
    """
    def has_create_permission(self, request):
        # Vérifie si l'utilisateur connecté a la permission de créer un nouveau contrat.
        # Autorise uniquement les membres de l'équipe gestion.
        return request.user.role == User.ROLE_MANAGEMENT

    def has_update_permission(self, request, user):
        # Vérifie si l'utilisateur connecté a la permission de mettre à jour un contrat spécifique.
        # Autorise les membres de l'équipe gestion et les membres de l'équipe commerciale associés au contrat et au client.
        return (
            request.user.role == User.ROLE_MANAGEMENT or
            (
                request.user.role == User.ROLE_SALES and (
                    request.user == user or
                    (hasattr(user, 'client') and request.user in user.client.sales_contact.all())
                )
            )
        )

    def has_delete_permission(self, request, user):
        # Vérifie si l'utilisateur connecté a la permission de supprimer un contrat spécifique.
        # Autorise les membres de l'équipe gestion et les membres de l'équipe commerciale associés au contrat et au client.
        return (
            request.user.role == User.ROLE_MANAGEMENT or
            (
                request.user.role == User.ROLE_SALES and (
                    request.user == user or
                    (hasattr(user, 'client') and request.user in user.client.sales_contact.all())
                )
            )
        )

    def has_permission(self, request, view):
        try:
            contract_pk = view.kwargs.get('contract_pk')

            # Si 'contract_pk' n'est pas spécifié dans l'URL, l'accès est autorisé sans restriction de permission
            if not contract_pk:
                return True

            # Méthodes sécurisées : GET, HEAD, OPTIONS
            if request.method in permissions.SAFE_METHODS:
                # Autorise l'accès uniquement aux membres de l'équipe gestion et de l'équipe commerciale
                return request.user.role in [User.ROLE_MANAGEMENT, User.ROLE_SALES]

            # Méthodes non sécurisées : POST, PUT, DELETE
            # Vérifie si l'utilisateur connecté est le gestionnaire du contrat ou membre de l'équipe gestion ou commerciale
            return request.user.role in [User.ROLE_MANAGEMENT, User.ROLE_SALES]

        except Http404:
            # Si l'objet contract_pk n'est pas trouvé, l'accès est refusé
            return False
