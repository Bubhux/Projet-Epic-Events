from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

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
        fields = ['id', 'full_name', 'email', 'role', 'is_staff', 'is_active', 'password', 'tokens']

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
            role=validated_data['role'],
            is_staff=True,
            is_active=True,
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

        Champs :
        - 'id': Identifiant unique du client.
        - 'full_name': Nom complet du client.
        - 'email': Adresse e-mail du client.
        - 'phone_number': Numéro de téléphone du client.
        - 'company_name': Nom de l'entreprise du client.
    """
    class Meta:
        model = Client
        fields = ['id', 'full_name', 'email', 'phone_number', 'company_name']


class ClientDetailSerializer(serializers.ModelSerializer):
    """
        Serializer pour les détails d'un client.
        Ce serializer est utilisé pour représenter les détails d'un client spécifique dans le CRM.

        Champs :
        - 'id': Identifiant unique du client.
        - 'full_name': Nom complet du client.
        - 'email': Adresse e-mail du client.
        - 'phone_number': Numéro de téléphone du client.
        - 'company_name': Nom de l'entreprise du client.
        - 'creation_date': Date de création du client.
        - 'update_date': Date de mise à jour du client.
        - 'last_contact': Dernier contact du client.
        - 'sales_contact': Gestionnaire des ventes en charge du client.
        - 'email_contact_id': Identifiant de contact par e-mail.
    """
    sales_contact = serializers.ReadOnlyField(source='sales_contact.full_name')

    class Meta:
        model = Client
        fields = ['id', 'full_name', 'email', 'phone_number', 'company_name', 'creation_date',
                  'update_date', 'last_contact', 'sales_contact', 'email_contact_id']


class UserListSerializer(serializers.ModelSerializer):
    """
        Serializer pour la liste des utilisateurs.
        Ce serializer est utilisé pour représenter les données de la liste des utilisateurs dans le CRM.

        Champs :
        - 'id': Identifiant unique de l'utilisateur.
        - 'full_name': Nom complet de l'utilisateur.
        - 'email': Adresse e-mail de l'utilisateur.
        """
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email']


class UserDetailSerializer(serializers.ModelSerializer):
    """
        Sérialiseur pour les détails d'un utilisateur.
        Ce sérialiseur est utilisé pour représenter les détails d'un utilisateur spécifique dans le CRM.

        Champs :
        - 'id': Identifiant unique de l'utilisateur.
        - 'full_name': Nom complet de l'utilisateur.
        - 'email': Adresse e-mail de l'utilisateur.
        - 'role': Rôle de l'utilisateur dans le système.
        - 'is_staff': Indique si l'utilisateur a des privilèges d'administration.
        - 'is_active': Indique si le compte de l'utilisateur est actif.
        - 'phone_number': Numéro de téléphone de l'utilisateur.
        - 'password': Mot de passe de l'utilisateur (en écriture seule).

        Méthodes :
        - 'validate_password': Méthode de validation personnalisée pour le champ 'password'.
        Assure que le mot de passe n'est pas vide et le hache avant de l'enregistrer.

        Remarque : Le champ 'password' est en écriture seule et n'est pas inclus lors de la récupération des détails de l'utilisateur.
    """
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'role', 'phone_number', 'is_staff', 'is_active', 'password']

    def validate_password(self, value):
        # Vérifier que le mot de passe n'est pas vide
        if value is not None:
            # Hacher le mot de passe avant de l'enregistrer
            return make_password(value)
        # Le mot de passe est vide, lever une erreur de validation
        raise ValidationError("Le mot de passe est vide")
