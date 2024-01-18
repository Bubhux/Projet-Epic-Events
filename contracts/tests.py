import pytest
import logging
from django.test import TestCase, Client
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Contract
from profiles.models import User, Client


@pytest.mark.django_db
class TestContractsApp(TestCase):
    """
        Classe de test pour le module Contracts de l'application Epic Events.

        Cette classe contient plusieurs méthodes de test pour vérifier le bon fonctionnement
        des fonctionnalités liées aux contrats dans l'application.
    """
    def create_user(self, email, role, full_name, phone_number, is_staff=True):
        """
            Crée et retourne un utilisateur avec les paramètres spécifiés.
        """
        return User.objects.create_user(
            email=email,
            password='Pingou123',
            role=role,
            full_name=full_name,
            phone_number=phone_number,
            is_staff=is_staff,
        )

    def create_client(self, email, full_name, phone_number, company_name):
        """
            Crée et retourne un client avec les paramètres spécifiés.
        """
        return Client.objects.create(
            email=email,
            full_name=full_name,
            phone_number=phone_number,
            company_name=company_name,
        )

    def create_contract(self, client, total_amount, remaining_amount, sales_contact=None, status_contract=False):
        """
            Crée et retourne un contrat avec les paramètres spécifiés.
        """
        return Contract.objects.create(
            client=client,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            status_contract=status_contract,
            sales_contact=sales_contact,
        )

    def setUp(self):
        """
            Met en place les données nécessaires pour les tests.
        """
        self.sales_user = self.create_user(
            email='Timothy@EpicEvents-Sales.com',
            role=User.ROLE_SALES,
            full_name='Timothy Lovejoy',
            phone_number='+345678912',
            is_staff=True
        )

        self.client_user = self.create_client(
            email='Ned@EpicEvents.com',
            full_name='Ned Flanders',
            phone_number='+987654321',
            company_name='Flanders & Co',
        )

        self.contract_user = self.create_contract(
            client=self.client_user,
            total_amount=1500.0,
            remaining_amount=1500.0,
            status_contract=True,
        )

    def test_contract_str_representation(self):
        """Teste la méthode __str__ du modèle Contract."""
        # Définis les valeurs initiales
        self.contract_user.status_contract = True
        self.contract_user.client = self.client_user
        
        # Chaîne attendue pour "Contrat signé" avec un client
        expected_str_signed = f"Contrat ID : {self.contract_user.id} Contract signed - {self.client_user.full_name}"
        self.assertEqual(str(self.contract_user), expected_str_signed)

        # Définies de nouvelles valeurs pour "Contrat non signé" et "Aucun client"
        self.contract_user.status_contract = False
        self.contract_user.client = None

        # Chaîne attendue pour "Contrat non signé" sans client associé
        expected_str_not_signed = f"Contrat ID : {self.contract_user.id} Contract not signed - No Client"
        self.assertEqual(str(self.contract_user), expected_str_not_signed)

    def test_contract_print_details(self, caplog):
        """Teste la méthode print_details du modèle Contract."""
        expected_output = "\nID du contrat : {}\n" \
                          "Nom du client : {}\n" \
                          "E-mail du client : {}\n" \
                          "Compagnie du client : {}\n\n".format(
                              self.contract_user.id,
                              self.client_user.full_name,
                              self.client_user.email,
                              self.client_user.company_name
                          )

        self.contract_user.print_details()
        self.assertEqual(caplog.text, expected_output)

    def test_save_method(self):
        """Teste la méthode save du modèle Contract."""
        client_with_sales_contact = self.create_client(
            email='Ned@EpicEvents.com',
            full_name='Ned Flanders',
            phone_number='+987654321',
            company_name='Flanders & Co',
            sales_contact=self.sales_user
        )

        contract_to_save = self.create_contract(
            client=client_with_sales_contact,
            total_amount=2000.0,
            remaining_amount=2000.0,
            sales_contact=self.sales_user,
            status_contract=False,
        )

        # Appel la méthode save
        contract_to_save.save()

        self.assertEqual(contract_to_save.sales_contact, self.sales_user)
        self.assertAlmostEqual(contract_to_save.update_date, contract_to_save.creation_date, delta=timezone.timedelta(seconds=1))


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
