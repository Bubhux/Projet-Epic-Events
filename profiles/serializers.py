from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.utils.translation import gettext_lazy as _

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

        # Générer les jetons à l'aide de Django REST framework simplejwt
        tokens = RefreshToken.for_user(user)
        data = {
            "refresh": str(tokens),  # Convertir le jeton d'actualisation en chaîne
            "access": str(tokens.access_token)  # Convertir le jeton d'accès en chaîne
        }
        # Retourner le dictionnaire contenant les jetons
        return data

    def create(self, validated_data):
        """Méthode pour créer un nouvel utilisateur dans la base de données"""

        # Récupérer le mot de passe à partir des données validées
        password = validated_data.get('password')

        # Créer un nouvel utilisateur avec les données validées
        user = User.objects.create_user(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            password=password,  # Utiliser le mot de passe récupéré
        )

        # Définir le mot de passe haché à partir des données validées
        user.set_password(password)
        user.save()
        return user


class ClientListSerializer(serializers.ModelSerializer):
    """Sérialiseur pour afficher une liste d'objets Client.

    Ce sérialiseur est utilisé pour représenter une liste d'objets Client
    lorsqu'ils sont récupérés via une requête GET sur l'endpoint 'crm/clients/'.
    Il inclut uniquement les champs 'full_name', 'id', 'email', 'phone_number', 'company_name' dans la réponse.
    """
    class Meta:
        model = Client
        fields = ['full_name', 'id', 'email', 'phone_number', 'company_name']


class ClientDetailSerializer(serializers.ModelSerializer):
    """Sérialiseur pour afficher les détails d'un objet Client.

    Ce sérialiseur est utilisé pour représenter les détails d'un objet Client
    lorsqu'il est récupéré via une requête GET sur l'endpoint 'crm/clients/<pk>/'.
    Il inclut les champs 'full_name', 'id', 'email', 'phone_number', 'company_name', 'creation_date',
    'update_date', 'last_contact', 'sales_contact', 'email_contact_id' dans la réponse.
    """
    class Meta:
        model = Client
        fields = ['full_name', 'id', 'email', 'phone_number', 'company_name', 'creation_date',
                  'update_date', 'last_contact', 'sales_contact', 'email_contact_id']


class UserListSerializer(serializers.ModelSerializer):
    clients = ClientListSerializer(many=True)

    class Meta:
        model = User
        fields = ['full_name', 'id', 'email']


class UserDetailSerializer(serializers.ModelSerializer):
    clients = ClientDetailSerializer(many=True)

    class Meta:
        model = User
        fields = ['full_name', 'id', 'email', 'user_contact', 'role', 'is_staff', 'clients']
