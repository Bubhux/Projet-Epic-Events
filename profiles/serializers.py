from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField
from django.utils.translation import gettext_lazy as _
from .models import User


class UserSignupSerializer(serializers.ModelSerializer):
    """Champ personnalisé pour stocker les jetons d'authentification"""

    tokens = SerializerMethodField()

    class Meta:
        model = User
        # Champs du modèle User à inclure dans la sérialisation
        fields = ['id', 'full_name', 'email', 'password', 'tokens']

    def validate_password(self, value):
        """Méthode de validation personnalisée pour le champ password"""
        # Vérifier que le mot de passe n'est pas vide
        if value is not None:
            # Hacher le mot de passe avant de le sauvegarder
            return make_password(value)
        # Le mot de passe est vide, lever une erreur de validation
        raise ValidationError("Password is empty")

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

        # Récupérer le nom d'utilisateur à partir des données validées
        # Récupérer l'email à partir des données validées
        user = User.objects.create_user(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            password=password,  # Utiliser le mot de passe récupéré
        )
        # Définir le mot de passe haché à partir des données validées
        user.set_password(password)
        user.save()
        return user