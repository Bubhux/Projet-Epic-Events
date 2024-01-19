import pytest
import json
import sys
from io import StringIO
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
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

    def tearDown(self):
        """
            Méthode appelée après l'exécution de chaque test.
            Réinitialise l'état de la base de données.
        """
        # Supprime toutes les instances des modèles après chaque test
        User.objects.all().delete()
        Client.objects.all().delete()
        Contract.objects.all().delete()

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

    def test_contract_print_details(self):
        """Teste la méthode print_details du modèle Contract."""
        expected_output = (
            f"\nID du contrat : {self.contract_user.id}\n"
            f"Nom du client : {self.client_user.full_name}\n"
            f"E-mail du client : {self.client_user.email}\n"
            f"Compagnie du client : {self.client_user.company_name}\n\n"
        )

        # Capture la sortie standard dans une chaîne
        captured_output = StringIO()
        sys.stdout = captured_output

        # Utilise la méthode print_details
        self.contract_user.print_details()

        # Restaure la sortie standard
        sys.stdout = sys.__stdout__

        # Obtient la valeur capturée
        result = captured_output.getvalue()

        # Compare la sortie de la méthode avec la valeur attendue
        self.assertEqual(result, expected_output)

        # Compare les attributs du contrat avec les valeurs attendues
        self.assertEqual(self.contract_user.id, 1)
        self.assertEqual(self.client_user.full_name, 'Ned Flanders')
        self.assertEqual(self.client_user.email, 'Ned@EpicEvents.com')
        self.assertEqual(self.client_user.company_name, 'Flanders & Co')

    def test_save_method(self):
        """Teste la méthode save du modèle Contract."""
        # Crée le client avec sales_contact égal à self.sales_user
        client_with_sales_contact = self.create_client(
            email='Lisa@EpicEvents.com',
            full_name='Lisa Simpson',
            phone_number='+765432198',
            company_name='Simpson & Co',
        )

        client_with_sales_contact.sales_contact = self.sales_user
        client_with_sales_contact.save()

        # Crée le contrat en référençant le client créé
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
        self.assertAlmostEqual(
            contract_to_save.update_date, contract_to_save.creation_date, delta=timezone.timedelta(seconds=1)
        )


@pytest.mark.django_db
class TestContractViewSet(TestCase):
    """
        Classe de tests pour les vues (ContractViewSet).
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

    def create_client(self, email, full_name, phone_number, company_name, sales_contact=None):
        """
        Crée et retourne un client avec les paramètres spécifiés.
        """
        return Client.objects.create(
            email=email,
            full_name=full_name,
            phone_number=phone_number,
            company_name=company_name,
            sales_contact=sales_contact,
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
        self.sales_user1 = self.create_user(
            email='Timothy@EpicEvents-Sales.com',
            role=User.ROLE_SALES,
            full_name='Timothy Lovejoy',
            phone_number='+345678912',
            is_staff=True
        )

        self.sales_user2 = self.create_user(
            email='Marge@EpicEvents-Sales.com',
            role=User.ROLE_SALES,
            full_name='Marge Simpson',
            phone_number='+123456789',
            is_staff=True
        )

        self.management_user = self.create_user(
            email='Milhouse@EpicEvents-Management.com',
            role=User.ROLE_MANAGEMENT,
            full_name='Milhouse Van Houten',
            phone_number='+567891234',
            is_staff=True
        )

        self.client_user = self.create_client(
            email='Ned@EpicEvents.com',
            full_name='Ned Flanders',
            phone_number='+987654321',
            company_name='Flanders & Co',
            sales_contact=self.sales_user1,
        )

        self.contract_user1 = self.create_contract(
            client=self.client_user,
            total_amount=1500.0,
            remaining_amount=500.0,
            status_contract=True,
            sales_contact=self.sales_user1
        )

        self.contract_user2 = self.create_contract(
            client=self.client_user,
            total_amount=2000.0,
            remaining_amount=2000.0,
            status_contract=False,
            sales_contact=self.sales_user1
        )

        self.contract_user3 = self.create_contract(
            client=self.client_user,
            total_amount=2000.0,
            remaining_amount=0.0,
            status_contract=True,
            sales_contact=self.sales_user1
        )

        # Créer un jeton d'accès pour sales_user1
        refresh_sales_user1 = RefreshToken.for_user(self.sales_user1)
        self.access_token_sales_user1 = str(refresh_sales_user1.access_token)

        # Créer un jeton d'accès pour sales_user2
        refresh_sales_user2 = RefreshToken.for_user(self.sales_user2)
        self.access_token_sales_user2 = str(refresh_sales_user2.access_token)

        # Créer un jeton d'accès pour management_user
        refresh_management_user = RefreshToken.for_user(self.management_user)
        self.access_token_management_user = str(refresh_management_user.access_token)

    def tearDown(self):
        """
            Méthode appelée après l'exécution de chaque test.
            Réinitialise l'état de la base de données.
        """
        # Supprime toutes les instances des modèles après chaque test
        User.objects.all().delete()
        Client.objects.all().delete()
        Contract.objects.all().delete()

    def test_contracts_list(self):
        # Test de la vue contract_list
        url = '/crm/contracts/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token_sales_user1}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

        # Affiche la totalité de la réponse JSON dans la console
        print("Response Data:", response.data)
        # print(json.dumps(response.data, indent=2))

    def test_contract_details(self):
        # Assure que le contrat_user1 est associé à sales_user1
        self.assertEqual(self.contract_user1.sales_contact, self.sales_user1)

        # Crée un jeton d'accès pour sales_user1
        refresh_sales_user1 = RefreshToken.for_user(self.sales_user1)
        access_token_sales_user1 = str(refresh_sales_user1.access_token)

        # Test de la vue contract_details pour le client associé à sales_user1
        url = f'/crm/contracts/{self.contract_user1.pk}/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token_sales_user1}')

        # Affiche la totalité de la réponse JSON dans la console
        print("Response Data:", response.data)
        # print(json.dumps(response.data, indent=2))

        # Vérifie que la réponse a le statut HTTP 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vérifie que les données de la réponse correspondent aux détails du contrat
        self.assertEqual(response.data['id'], self.contract_user1.pk)
        self.assertEqual(str(response.data['client']), str(self.contract_user1.client.full_name))

        # Vérifie que l'accès a bien été autorisé
        self.assertIn('id', response.data)
        self.assertIn('client', response.data)

    def test_contract_details_unauthorized_user(self):
        # Assure que le contract_user1 est associé à sales_user1
        self.assertEqual(self.contract_user1.sales_contact, self.sales_user1)

        # Crée un jeton d'accès pour sales_user2
        refresh_sales_user2 = RefreshToken.for_user(self.sales_user2)
        access_token_sales_user2 = str(refresh_sales_user2.access_token)

        # Test de la vue contract_details pour le contrat_user1
        # associé à sales_user1 avec le jeton d'accès de sales_user2
        url = f'/crm/contracts/{self.contract_user1.pk}/contract_details/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token_sales_user2}')

        # Vérifie que la réponse a le statut HTTP 403 (Forbidden) car l'utilisateur n'est pas autorisé
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.content.decode())

        # Vérifie que le texte spécifié est présent dans la réponse
        self.assertIn("You do not have permission to access this contract.", response.content.decode())

    def test_all_contracts_details(self):
        # Test la vue all_contracts_details
        url = '/crm/contracts/all_contracts_details/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token_sales_user2}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_filtered_contracts(self):
        # Créer un jeton d'accès pour sales_user1
        refresh_sales_user1 = RefreshToken.for_user(self.sales_user1)
        access_token_sales_user1 = str(refresh_sales_user1.access_token)

        # Effectue une requête GET vers la vue filtered_contracts avec le token d'accès de sales_user1
        url = '/crm/contracts/filtered_contracts/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token_sales_user1}')

        # Vérifie que la réponse a le statut HTTP 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vérifie que les données renvoyées correspondent aux contrats filtrés
        # Vérifie que le nombre de contrats renvoyés est égal à 2
        self.assertEqual(len(response.data), 2)

        # Vérifie que les contrats renvoyés sont les contrats associés à sales_user1
        self.assertIn(self.contract_user1.id, [contract['id'] for contract in response.data])
        self.assertIn(self.contract_user2.id, [contract['id'] for contract in response.data])

        # Vérifie que les contrats renvoyés sont les contrats non signés et non entièrement payés
        for contract in response.data:
            print(f"ID du contrat : {contract['id']}")
            print(f"Nom du client : {contract['client']}")
            print(f"Status du contrat : {contract['status_contract']}")
            print()

            # Si le contrat est signé (status_contract=True), vérifie que remaining_amount est supérieur à 0
            if contract['status_contract']:
                self.assertGreater(contract['remaining_amount'], 0.0)
            # Sinon (le contrat n'est pas signé), vérifie que status_contract est False
            else:
                self.assertFalse(contract['status_contract'])

    def test_create_contract(self):
        # Créer un jeton d'accès pour management_user
        refresh_management_user = RefreshToken.for_user(self.management_user)
        access_token_management_user = str(refresh_management_user.access_token)

        # Données du nouveau contrat à créer
        new_contract_data = {
            'client': 'Ned Flanders',
            'total_amount': '1500.0',
            'remaining_amount': '1500.0',
            'status_contract': 'True',
            'sales_contact': self.sales_user1.full_name
        }

        # Test de la vue create pour créer un nouveau contrat
        url = '/crm/contracts/'
        response = self.client.post(
            url, data=new_contract_data, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token_management_user}'
        )

        # Vérifie que la réponse a le statut HTTP 201 (Created) car le contrat a été créé avec succès
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Affiche la réponse pour vérifier le message de succès
        print(response.data)

        # Vérifie que le message de succès est présent dans la réponse
        self.assertIn("Contract successfully created.", response.data.get("message"))

        # Vérifie que les données du contrat créé sont présentes dans la réponse
        self.assertIn("data", response.data)
        self.assertEqual(response.data["data"]["client"], new_contract_data["client"])
        self.assertEqual(str(response.data["data"]["total_amount"]), new_contract_data["total_amount"])
        self.assertEqual(str(response.data["data"]["remaining_amount"]), new_contract_data["remaining_amount"])
        self.assertEqual(response.data["data"]["sales_contact"], new_contract_data["sales_contact"])

    def test_create_contract_unauthorized_user(self):
        # Créer un jeton d'accès pour sales_user2
        refresh_sales_user2 = RefreshToken.for_user(self.sales_user2)
        access_token_sales_user2 = str(refresh_sales_user2.access_token)

        # Données du nouveau contrat à créer
        new_contract_data = {
            'client': 'Ned Flanders',
            'total_amount': '1500.0',
            'remaining_amount': '1500.0',
            'status_contract': 'True',
            'sales_contact': self.sales_user1.full_name
        }

        # Test de la vue create pour créer un nouveau contrat avec le jeton d'accès de support_user2
        url = '/crm/contracts/'
        response = self.client.post(
            url, data=new_contract_data, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token_sales_user2}'
        )

        # Vérifie que la réponse a le statut HTTP 403 (Forbidden) car l'utilisateur n'est pas autorisé
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.content.decode())

        # Vérifie que le texte spécifié est présent dans la réponse
        self.assertIn("You do not have permission to create a contract.", response.content.decode())

    def test_update_contract(self):
        # Assure que le contract_user1 est associé à sales_user1
        self.assertEqual(self.contract_user1.sales_contact, self.sales_user1)

        # Créer un jeton d'accès pour sales_user1
        refresh_sales_user1 = RefreshToken.for_user(self.sales_user1)
        access_token_sales_user1 = str(refresh_sales_user1.access_token)

        # Données du client mis à jour
        update_contract_data = {
            'client': 'Ned Flanders',
            'total_amount': '2000.0',
            'remaining_amount': '1500.99',
            'status_contract': 'True',
            'sales_contact': self.sales_user1.full_name
        }

        # Test de la vue update pour mettre à jour contract_user1
        url = f'/crm/contracts/{self.contract_user1.pk}/'
        response = self.client.put(
            url,
            data=json.dumps(update_contract_data),
            content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {access_token_sales_user1}'
        )

        # Vérifie que la réponse a le statut HTTP 200 (OK) car le contrat a été mis à jour avec succès
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Affiche la réponse pour vérifier le message de succès
        print(response.data)

        # Vérifie que le message de succès est présent dans la réponse
        self.assertIn("Contract successfully updated.", response.data.get("message"))

        # Vérifie que les données mises à jour du client créé sont présentes dans la réponse
        self.assertIn("data", response.data)
        self.assertEqual(response.data["data"]["client"], update_contract_data["client"])
        self.assertEqual(str(response.data["data"]["total_amount"]), update_contract_data["total_amount"])
        self.assertEqual(str(response.data["data"]["remaining_amount"]), update_contract_data["remaining_amount"])

    def test_update_contract_unauthorized_user(self):
        # Assure que le contract_user1 est associé à sales_user1
        self.assertEqual(self.contract_user1.sales_contact, self.sales_user1)

        # Créer un jeton d'accès pour sales_user1
        refresh_sales_user2 = RefreshToken.for_user(self.sales_user2)
        access_token_sales_user2 = str(refresh_sales_user2.access_token)

        # Données du contrat mis à jour
        update_contract_data = {
            'client': 'Ned Flanders',
            'total_amount': '2000.0',
            'remaining_amount': '1000.0',
            'status_contract': 'True',
            'sales_contact': self.sales_user2.full_name
        }

        # Test de la vue update pour mettre à jour contract_user1 avec le jeton d'accès de sales_user2
        url = f'/crm/contracts/{self.contract_user1.pk}/'
        response = self.client.put(
            url,
            data=json.dumps(update_contract_data),
            content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {access_token_sales_user2}'
        )

        # Vérifie que la réponse a le statut HTTP 403 (Forbidden) car l'utilisateur n'est pas autorisé
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.content.decode())

        # Vérifie que le texte spécifié est présent dans la réponse
        self.assertIn("You do not have permission to update this contract.", response.content.decode())

    def test_destroy_contract(self):
        # Assure que le contract_user1 est associé à sales_user1
        self.assertEqual(self.contract_user1.sales_contact, self.sales_user1)

        # Créer un jeton d'accès pour sales_user1
        refresh_sales_user1 = RefreshToken.for_user(self.sales_user1)
        access_token_sales_user1 = str(refresh_sales_user1.access_token)

        # Données du contrat à supprimer
        destroy_contract_data = {
            'client': 'Ned Flanders',
            'total_amount': '1500.0',
            'remaining_amount': '1500.0',
            'status_contract': 'True',
            'sales_contact': self.sales_user1.full_name
        }

        # Test de la vue destroy pour supprimer contract_user1
        url = f'/crm/contracts/{self.contract_user1.pk}/'
        response = self.client.delete(
            url,
            data=destroy_contract_data,
            format='json', HTTP_AUTHORIZATION=f'Bearer {access_token_sales_user1}'
        )

        # Vérifie que la réponse a le statut HTTP 204 (No Content) car le contrat a été supprimé avec succès
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.data)

        # Vérifie que le message de succès est présent dans la réponse
        self.assertIn("Contract successfully deleted.", response.data.get("message"))

    def test_destroy_contract_unauthorized_user(self):
        # Assure que le contract_user1 est associé à sales_user1
        self.assertEqual(self.contract_user1.sales_contact, self.sales_user1)

        # Créer un jeton d'accès pour sales_user2
        refresh_sales_user2 = RefreshToken.for_user(self.sales_user2)
        access_token_sales_user2 = str(refresh_sales_user2.access_token)

        # Données du contrat à supprimer
        destroy_contract_data = {
            'client': 'Ned Flanders',
            'total_amount': '1500.0',
            'remaining_amount': '1500.0',
            'status_contract': 'True',
            'sales_contact': self.sales_user1.full_name
        }

        # Test de la vue destroy pour supprimer le contract_user1 avec le jeton d'accès de sales_user2
        url = f'/crm/contracts/{self.contract_user1.pk}/'
        response = self.client.delete(
            url,
            data=destroy_contract_data,
            format='json', HTTP_AUTHORIZATION=f'Bearer {access_token_sales_user2}'
        )

        # Vérifie que la réponse a le statut HTTP 403 (Forbidden) car l'utilisateur n'est pas autorisé
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.content.decode())

        # Vérifie que le message de succès est présent dans la réponse
        self.assertIn("You do not have permission to delete this contract.", response.content.decode())
