from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import User, Client


class MultipleSerializerMixin:
    """Mixin pour utiliser plusieurs classes de sérialiseur dans une vue."""

    # Par défaut, la variable detail_serializer_class est définie sur None.
    # Ce qui signifie qu'il n'y a pas de sérialiseur spécifique défini pour les actions de type
    # "retrieve", "create", "update" et "destroy".
    detail_serializer_class = None

    def get_serializer_class(self):
        if (self.action == 'retrieve' or
                self.action == 'create' or
                self.action == 'update' or
                self.action == 'destroy') and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class UserLoginSerializer(serializers.ModelSerializer):
    """Champ personnalisé pour stocker les jetons d'authentification"""

    # Champ 'tokens' pour stocker les jetons d'authentification
    tokens = SerializerMethodField()

    class Meta:
        model = User
        # Champs du modèle User à inclure dans la sérialisation
        fields = ['id', 'full_name', 'email', 'password', 'tokens']

    def get_tokens(self, user):
        """Méthode pour obtenir les jetons (tokens) d'authentification pour l'utilisateur"""

        # Génére les jetons à l'aide de Django REST framework simplejwt
        tokens = RefreshToken.for_user(user)
        data = {
            "refresh": str(tokens),  # Convertie le jeton d'actualisation en chaîne
            "access": str(tokens.access_token)  # Convertie le jeton d'accès en chaîne
        }
        # Retourne le dictionnaire contenant les jetons
        return data

    def create(self, validated_data):
        """Méthode pour créer un nouvel utilisateur dans la base de données"""

        # Récupére le mot de passe à partir des données validées
        password = validated_data.get('password')

        # Créer un nouvel utilisateur avec les données validées
        user = User.objects.create_user(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            password=password,  # Utiliser le mot de passe récupéré
        )

        # Définie le mot de passe haché à partir des données validées
        user.set_password(password)
        user.save()
        return user


class ClientListSerializer(serializers.ModelSerializer):
    """
        Serializer pour la liste des clients.
        Ce serializer est utilisé pour représenter les données de la liste des clients dans le CRM.

        Champ 'full_name': Nom complet du client.
        Champ 'id': Identifiant unique du client.
        Champ 'email': Adresse e-mail du client.
        Champ 'phone_number': Numéro de téléphone du client.
        Champ 'company_name': Nom de l'entreprise du client.
    """
    class Meta:
        model = Client
        fields = ['full_name', 'id', 'email', 'phone_number', 'company_name']


class ClientDetailSerializer(serializers.ModelSerializer):
    """
        Serializer pour les détails d'un client.
        Ce serializer est utilisé pour représenter les détails d'un client spécifique dans le CRM.

        Champ 'full_name': Nom complet du client.
        Champ 'id': Identifiant unique du client.
        Champ 'email': Adresse e-mail du client.
        Champ 'phone_number': Numéro de téléphone du client.
        Champ 'company_name': Nom de l'entreprise du client.
        Champ 'creation_date': Date de création du client.
        Champ 'update_date': Date de mise à jour du client.
        Champ 'last_contact': Dernier contact du client.
        Champ 'sales_contact': Gestionnaire des ventes en charge du client.
        Champ 'email_contact_id': Identifiant de contact par e-mail.
    """
    class Meta:
        model = Client
        fields = ['full_name', 'id', 'email', 'phone_number', 'company_name', 'creation_date',
                  'update_date', 'last_contact', 'sales_contact', 'email_contact_id']


class UserListSerializer(serializers.ModelSerializer):
    """
        Serializer pour la liste des utilisateurs.
        Ce serializer est utilisé pour représenter les données de la liste des utilisateurs dans le CRM.

        Champ 'full_name': Nom complet de l'utilisateur.
        Champ 'id': Identifiant unique de l'utilisateur.
        Champ 'email': Adresse e-mail de l'utilisateur.
        """
    class Meta:
        model = User
        fields = ['full_name', 'id', 'email']


class UserDetailSerializer(serializers.ModelSerializer):
    """
        Serializer pour les détails d'un utilisateur.
        Ce serializer est utilisé pour représenter les détails d'un utilisateur spécifique dans le CRM.

        Champ 'full_name': Nom complet de l'utilisateur.
        Champ 'id': Identifiant unique de l'utilisateur.
        Champ 'email': Adresse e-mail de l'utilisateur.
        Champ 'role': Rôle de l'utilisateur dans le système.
        Champ 'is_staff': Indique si l'utilisateur a des privilèges d'administration.
    """
    class Meta:
        model = User
        fields = ['full_name', 'id', 'email', 'role', 'is_staff']
