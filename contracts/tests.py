import pytest
from django.test import TestCase, Client
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Contract


@pytest.mark.django_db
class TestContractsApp(TestCase):
    """
        Classe de test pour le module Contracts de l'application Epic Events.

        Cette classe contient plusieurs méthodes de test pour vérifier le bon fonctionnement
        des fonctionnalités liées aux contrats dans l'application.
    """
    def create_contract(self):
        pass

    def setUp(self):
        pass

    def test_create_contract(self):
        pass


@pytest.mark.django_db
class TestContractViewSet(TestCase):
    """
        Classe de tests pour les vues (ContractViewSet).
    """
    def create_contract(self):
        pass

    def setUp(self):
        pass

    def test_contracts_list(self):
        pass

    def test_contract_details(self):
        pass

    def test_all_contracts_details(self):
        pass
