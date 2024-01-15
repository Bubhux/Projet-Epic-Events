from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import UserSignupSerializer
from .models import User


class SignupView(generics.CreateAPIView):
    """
    Vue pour l'inscription des utilisateurs.

    Cette vue permet à un utilisateur de s'inscrire en fournissant un nom d'utilisateur,
    une adresse e-mail, un mot de passe.
    L'utilisateur sera créé dans la base de données avec les informations fournies.
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSignupSerializer