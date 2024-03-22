import pytest
import json
import datetime
import pendulum
import sys
from io import StringIO
from django.test import TestCase
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Event
from contracts.models import Contract
from profiles.models import User, Client


@pytest.mark.django_db
class TestEventsApp(TestCase):
    """
        Classe de test pour le module Events de l'application Epic Events.
        Cette classe contient plusieurs méthodes de test pour vérifier le bon fonctionnement
        des fonctionnalités liées aux événements dans l'application.
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

    def create_event(
        self,
        event_name,
        contract,
        client,
        client_name,
        client_contact,
        event_date_start,
        event_date_end,
        support_contact,
        location,
        attendees,
        notes
    ):
        """
            Crée et retourne un événement avec les paramètres spécifiés.
        """
        return Event.objects.create(
            event_name=event_name,
            contract=contract,
            client_name=client_name,
            client_contact=client_contact,
            event_date_start=event_date_start,
            event_date_end=event_date_end,
            support_contact=support_contact,
            location=location,
            attendees=attendees,
            notes=notes,
        )

    def setUp(self):
        """
            Mets en place les données nécessaires pour les tests.
        """
        self.sales_user1 = self.create_user(
            email='Timothy@EpicEvents-Sales.com',
            role=User.ROLE_SALES,
            full_name='Timothy Lovejoy',
            phone_number='+345678912',
            is_staff=True
        )

        self.support_user1 = self.create_user(
            email='Homer@EpicEvents-Support.com',
            role=User.ROLE_SUPPORT,
            full_name='Homer Simpson',
            phone_number='+345678912',
            is_staff=True
        )

        self.management_user1 = self.create_user(
            email='Milhouse@EpicEvents-Management.com',
            role=User.ROLE_MANAGEMENT,
            full_name='Milhouse Van Houten',
            phone_number='+567891234',
            is_staff=True
        )

        self.client_user1 = self.create_client(
            email='Ned@EpicEvents.com',
            full_name='Ned Flanders',
            phone_number='+987654321',
            company_name='Flanders & Co',
            sales_contact=self.sales_user1,
        )

        self.contract_user1 = self.create_contract(
            client=self.client_user1,
            total_amount=1500.0,
            remaining_amount=0.0,
            status_contract=True,
            sales_contact=self.sales_user1
        )

        self.event_user1 = self.create_event(
            event_name="Event Flanders",
            contract=self.contract_user1,
            client=self.client_user1,
            client_name="Ned Flanders",
            client_contact="Ned@EpicEvents.com +987654321",
            event_date_start=make_aware(datetime.datetime(2025, 2, 14, 12, 45)),
            event_date_end=make_aware(datetime.datetime(2025, 11, 25, 12, 55)),
            support_contact=self.support_user1,
            location="Rome",
            attendees=1,
            notes="Event notes"
        )

        # Mets à jour les attributs du client dans l'événement
        self.event_user1.client = self.client_user1
        self.event_user1.save()

    def tearDown(self):
        """
            Méthode appelée après l'exécution de chaque test.
            Réinitialise l'état de la base de données.
        """
        # Supprime toutes les instances des modèles après chaque test
        User.objects.all().delete()
        Client.objects.all().delete()
        Contract.objects.all().delete()
        Event.objects.all().delete()

    def test_event_str_representation(self):
        """Teste la méthode __str__ du modèle Event."""
        # Définit les valeurs initiales
        self.event_user1.contract = self.contract_user1
        self.event_user1.support_contact = self.support_user1
        self.event_user1.client = self.client_user1

        # Sauvegarde l'événement après avoir lié le client
        self.event_user1.save()

        # Chaîne attendue pour l'événement créé avec un client
        expected_str_event_created = (
            f"Evénement ID: {self.event_user1.id} "
            f"{self.event_user1.event_name} - {self.event_user1.client_name}"
        )

        self.assertEqual(str(self.event_user1), expected_str_event_created)

    def test_event_print_details(self):
        """Teste la méthode print_details du modèle Event."""
        # Définit les valeurs initiales
        self.event_user1.contract = self.contract_user1
        self.event_user1.support_contact = self.support_user1
        self.event_user1.client = self.client_user1

        # Capture la sortie de print_details
        captured_output = StringIO()
        sys.stdout = captured_output
        self.event_user1.print_details()
        sys.stdout = sys.__stdout__

        # Récupère la sortie imprimée
        printed_output = captured_output.getvalue()

        # Chaîne attendue pour les détails de l'événement
        expected_output = (
            f"\nID de l'événement : {self.event_user1.id}\n"
            f"Nom de l'événement : {self.event_user1.event_name}\n"
            f"ID du contrat associé : {self.event_user1.contract.id}\n"
            f"Nom du client : {self.client_user1.full_name}\n"
            f"E-mail du client : {self.client_user1.email}\n"
            f"Compagnie du client : {self.client_user1.company_name}\n"
            f"Contact du client : {self.event_user1.client_contact}\n"
            f"Date de début de l'événement : {self.event_user1.event_date_start}\n"
            f"Date de fin de l'événement : {self.event_user1.event_date_end}\n"
            f"Contact de support : User ID : {self.support_user1.id} "
            f"Équipe Support - {self.support_user1.full_name} ({self.support_user1.email})\n"
            f"Lieu : {self.event_user1.location}\n"
            f"Nombre d'invités : {self.event_user1.attendees}\n"
            f"Notes : {self.event_user1.notes}\n\n"
        )

        # Compare la sortie avec les valeurs attendues
        self.assertEqual(printed_output.strip(), expected_output.strip())

        # Compare les attributs de l'événement avec les valeurs attendues
        self.assertEqual(self.event_user1.id, 1)
        self.assertEqual(self.event_user1.event_name, 'Event Flanders')
        self.assertEqual(self.client_user1.full_name, 'Ned Flanders')
        self.assertEqual(self.client_user1.email, 'Ned@EpicEvents.com')
        self.assertEqual(self.client_user1.company_name, 'Flanders & Co')
        self.assertEqual(self.event_user1.client_contact, 'Ned@EpicEvents.com +987654321')
        self.assertEqual(self.event_user1.event_date_start, make_aware(datetime.datetime(2025, 2, 14, 12, 45)))
        self.assertEqual(self.event_user1.event_date_end, make_aware(datetime.datetime(2025, 11, 25, 12, 55)))
        self.assertEqual(self.event_user1.support_contact, self.support_user1)
        self.assertEqual(self.event_user1.location, 'Rome')
        self.assertEqual(self.event_user1.attendees, 1)
        self.assertEqual(self.event_user1.notes, 'Event notes')

    def test_save_method(self):
        # Crée un nouvel événement
        new_event = self.create_event(
            event_name="Event Flanders",
            contract=self.contract_user1,
            client=self.client_user1,
            client_name="Ned Flanders",
            client_contact="Ned@EpicEvents.com +987654321",
            event_date_start=make_aware(datetime.datetime(2025, 2, 14, 12, 45)),
            event_date_end=make_aware(datetime.datetime(2025, 11, 25, 12, 55)),
            support_contact=self.support_user1,
            location="Rome",
            attendees=1,
            notes="Event notes"
        )

        # Associe le contrat et le client à l'événement
        new_event.contract = self.contract_user1
        new_event.client = self.client_user1

        # Appelle la méthode save
        new_event.save()

        # Récupère l'événement après la sauvegarde
        saved_event = Event.objects.get(id=new_event.id)
        print(saved_event)

        # Vérifie que les attributs ont été mis à jour correctement
        self.assertEqual(saved_event.id, new_event.id)
        self.assertEqual(saved_event.event_name, new_event.event_name)
        self.assertEqual(saved_event.contract, new_event.contract)
        self.assertEqual(saved_event.client, new_event.client)
        self.assertEqual(saved_event.client_name, new_event.client_name)
        self.assertEqual(saved_event.client_contact, new_event.client_contact)
        self.assertEqual(saved_event.event_date_start, new_event.event_date_start)
        self.assertEqual(saved_event.event_date_end, new_event.event_date_end)
        self.assertEqual(saved_event.support_contact, new_event.support_contact)
        self.assertEqual(saved_event.location, new_event.location)
        self.assertEqual(saved_event.attendees, new_event.attendees)
        self.assertEqual(saved_event.notes, new_event.notes)


@pytest.mark.django_db
class TestEventViewSet(TestCase):
    """
        Classe de tests pour les vues (EventViewSet).
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

    def create_event(
        self,
        event_name,
        contract,
        client,
        client_name,
        client_contact,
        event_date_start,
        event_date_end,
        support_contact,
        location,
        attendees,
        notes
    ):
        """
            Crée et retourne un événement avec les paramètres spécifiés.
        """
        return Event.objects.create(
            event_name=event_name,
            contract=contract,
            client=client,
            client_name=client_name,
            client_contact=client_contact,
            event_date_start=event_date_start,
            event_date_end=event_date_end,
            support_contact=support_contact,
            location=location,
            attendees=attendees,
            notes=notes,
        )

    def setUp(self):
        """
            Mets en place les données nécessaires pour les tests.
        """
        self.management_user1 = self.create_user(
            email='Milhouse@EpicEvents-Management.com',
            role=User.ROLE_MANAGEMENT,
            full_name='Milhouse Van Houten',
            phone_number='+567891234',
            is_staff=True
        )

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

        self.support_user1 = self.create_user(
            email='Homer@EpicEvents-Support.com',
            role=User.ROLE_SUPPORT,
            full_name='Homer Simpson',
            phone_number='+345678912',
            is_staff=True
        )

        self.support_user2 = self.create_user(
            email='Tahiti@EpicEvents-Support.com',
            role=User.ROLE_SUPPORT,
            full_name='Tahiti Bob',
            phone_number='+456789123',
            is_staff=True
        )

        self.client_user1 = self.create_client(
            email='Ned@EpicEvents.com',
            full_name='Ned Flanders',
            phone_number='+987654321',
            company_name='Flanders & Co',
            sales_contact=self.sales_user1,
        )

        self.client_user2 = self.create_client(
            email='Ralph@EpicEvents.com',
            full_name='Ralph Wiggum',
            phone_number='+654321987',
            company_name='Wiggum Gum & Co',
            sales_contact=self.sales_user1,
        )

        self.client_user3 = self.create_client(
            email='Lisa@EpicEvents.com',
            full_name='Lisa Simpson',
            phone_number='+765432198',
            company_name='Simpson & Co',
            sales_contact=self.sales_user1,
        )

        self.contract_user1 = self.create_contract(
            client=self.client_user1,
            total_amount=1500.0,
            remaining_amount=0.0,
            status_contract=True,
            sales_contact=self.sales_user1
        )

        self.contract_user2 = self.create_contract(
            client=self.client_user2,
            total_amount=1200.0,
            remaining_amount=0.0,
            status_contract=True,
            sales_contact=self.sales_user1
        )

        self.contract_user3 = self.create_contract(
            client=self.client_user3,
            total_amount=1100.0,
            remaining_amount=0.0,
            status_contract=True,
            sales_contact=self.sales_user1
        )

        self.contract_user4 = self.create_contract(
            client=self.client_user3,
            total_amount=1100.0,
            remaining_amount=1100.0,
            status_contract=False,
            sales_contact=self.sales_user1
        )

        self.event_user1 = self.create_event(
            event_name="Event Flanders",
            contract=self.contract_user1,
            client=self.client_user1,
            client_name=self.client_user1.full_name,
            client_contact=f"{self.client_user1.email} {self.client_user1.phone_number}",
            event_date_start=make_aware(datetime.datetime(2025, 2, 14, 12, 45)),
            event_date_end=make_aware(datetime.datetime(2025, 11, 25, 12, 55)),
            support_contact=self.support_user1,
            location="Rome",
            attendees=1,
            notes="Event notes"
        )

        self.event_user2 = self.create_event(
            event_name="Event Wiggum",
            contract=self.contract_user2,
            client=self.client_user2,
            client_name=self.client_user2.full_name,
            client_contact=f"{self.client_user2.email} {self.client_user2.phone_number}",
            event_date_start=make_aware(datetime.datetime(2025, 3, 16, 13, 55)),
            event_date_end=make_aware(datetime.datetime(2025, 4, 22, 16, 30)),
            support_contact=None,
            location="Japon",
            attendees=100,
            notes="Event notes"
        )

        # Crée un jeton d'accès pour sales_user1
        refresh_sales_user1 = RefreshToken.for_user(self.sales_user1)
        self.access_token_sales_user1 = str(refresh_sales_user1.access_token)

        # Crée un jeton d'accès pour sales_user2
        refresh_sales_user2 = RefreshToken.for_user(self.sales_user2)
        self.access_token_sales_user2 = str(refresh_sales_user2.access_token)

        # Crée un jeton d'accès pour management_user1
        refresh_management_user1 = RefreshToken.for_user(self.management_user1)
        self.access_token_management_user1 = str(refresh_management_user1.access_token)

        # Crée un jeton d'accès pour support_user1
        refresh_support_user1 = RefreshToken.for_user(self.support_user1)
        self.access_token_support_user1 = str(refresh_support_user1.access_token)

        # Crée un jeton d'accès pour support_user2
        refresh_support_user2 = RefreshToken.for_user(self.support_user2)
        self.access_token_support_user2 = str(refresh_support_user2.access_token)

    def tearDown(self):
        """
            Méthode appelée après l'exécution de chaque test.
            Réinitialise l'état de la base de données.
        """
        # Supprime toutes les instances des modèles après chaque test
        User.objects.all().delete()
        Client.objects.all().delete()
        Contract.objects.all().delete()
        Event.objects.all().delete()

    def test_events_list(self):
        # Test de la vue events_list
        url = '/crm/events/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token_sales_user1}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

        # Affiche la totalité de la réponse JSON dans la console
        print("Response Data:", response.data)
        # print(json.dumps(response.data, indent=2))

    def test_event_details(self):
        # Assure que event_user1 est associé à support_user1
        self.assertEqual(self.event_user1.support_contact, self.support_user1)

        # Crée un jeton d'accès pour support_user1
        refresh_support_user1 = RefreshToken.for_user(self.support_user1)
        access_token_support_user1 = str(refresh_support_user1.access_token)

        # Test de la vue event_details pour l'événement associé à support_user1
        url = f'/crm/events/{self.event_user1.pk}/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token_support_user1}')

        # Affiche la totalité de la réponse JSON dans la console
        print("Response Data:", response.data)
        # print(json.dumps(response.data, indent=2))

        # Vérifie que les données de la réponse correspondent aux détails de l'événement
        self.assertEqual(response.data['id'], self.event_user1.pk)
        self.assertEqual(response.data['event_name'], self.event_user1.event_name)
        self.assertEqual(response.data['client'], self.client_user1.full_name)
        self.assertEqual(response.data['client_contact'], f"{self.client_user1.email} {self.client_user1.phone_number}")
        self.assertEqual(response.data['contract'], self.contract_user1.pk)
        self.assertEqual(response.data['support_contact'], self.support_user1.full_name)
        self.assertEqual(response.data['location'], self.event_user1.location)
        self.assertEqual(response.data['attendees'], self.event_user1.attendees)
        self.assertEqual(response.data['notes'], self.event_user1.notes)

        # Vérifie event_date_start et event_date_end
        expected_start_date = self.event_user1.event_date_start
        expected_end_date = self.event_user1.event_date_end

        # Convertit la chaîne de date dans la réponse JSON en un objet Pendulum
        response_start_date_str = response.data['event_date_start']
        response_start_date = pendulum.parse(response_start_date_str)

        response_end_date_str = response.data['event_date_end']
        response_end_date = pendulum.parse(response_end_date_str)

        self.assertEqual(response_start_date, expected_start_date)
        self.assertEqual(response_end_date, expected_end_date)

    def test_event_details_unauthorized_user(self):
        # Assure que event_user1 est associé à support_user1
        self.assertEqual(self.event_user1.support_contact, self.support_user1)

        # Crée un jeton d'accès pour support_user2
        refresh_support_user2 = RefreshToken.for_user(self.support_user2)
        access_token_support_user2 = str(refresh_support_user2.access_token)

        # Test de la vue event_details pour event_user1 associé à support_user1 avec le jeton d'accès de support_user2
        url = f'/crm/events/{self.event_user1.pk}/event_details/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token_support_user2}')

        # Vérifie que la réponse a le statut HTTP 403 (Forbidden) car l'utilisateur n'est pas autorisé
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.content.decode())

        # Vérifie que le texte spécifié est présent dans la réponse
        self.assertIn("You do not have permission to access this event.", response.content.decode())

    def test_all_events_details(self):
        # Test la vue all_events_details
        url = '/crm/events/all_events_details/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token_support_user1}')

        # Affiche la totalité de la réponse JSON dans la console
        print("Response Data:", response.data)
        # print(json.dumps(response.data, indent=2))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_events_without_support(self):
        # Crée un jeton d'accès pour management_user1
        refresh_management_user1 = RefreshToken.for_user(self.management_user1)
        access_token_management_user1 = str(refresh_management_user1.access_token)

        # Effectue une requête GET vers la vue events_without_support avec le token d'accès de management_user1
        url = '/crm/events/events_without_support/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token_management_user1}')

        # Affiche la totalité de la réponse JSON dans la console
        print("Response Data:", response.data)
        # print(json.dumps(response.data, indent=2))

        # Vérifie que la réponse a le statut HTTP 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assure que la réponse est une liste JSON
        self.assertIsInstance(response.data, list)

        # Assure que la liste ne contient qu'un seul élément
        self.assertEqual(len(response.data), 1)

        # Assure que l'élément dans la liste correspond à event_user2
        event_data = response.data[0]
        self.assertEqual(event_data['id'], self.event_user2.id)
        self.assertEqual(event_data['event_name'], self.event_user2.event_name)
        self.assertEqual(event_data['contract'], self.event_user2.contract.id)
        self.assertEqual(event_data['client'], self.event_user2.client.full_name)
        self.assertEqual(event_data['client_contact'], self.event_user2.client_contact)
        self.assertEqual(event_data['support_contact'], None)
        self.assertEqual(event_data['location'], self.event_user2.location)
        self.assertEqual(event_data['attendees'], self.event_user2.attendees)
        self.assertEqual(event_data['notes'], self.event_user2.notes)

        # Vérifie event_date_start et event_date_end
        expected_start_date = self.event_user2.event_date_start
        expected_end_date = self.event_user2.event_date_end

        # Convertit la chaîne de date dans la réponse JSON en un objet Pendulum
        response_start_date_str = event_data['event_date_start']
        response_start_date = pendulum.parse(response_start_date_str)

        response_end_date_str = event_data['event_date_end']
        response_end_date = pendulum.parse(response_end_date_str)

        self.assertEqual(response_start_date, expected_start_date)
        self.assertEqual(response_end_date, expected_end_date)

    def test_create_event(self):
        # Assure que client_user1 est associé à sales_user1
        self.assertEqual(self.client_user3.sales_contact, self.sales_user1)

        # Assure que contract_user1 pour client_user1 est signé
        self.assertTrue(self.contract_user3.status_contract)

        # Crée un jeton d'accès pour sales_user1
        refresh_sales_user1 = RefreshToken.for_user(self.sales_user1)
        access_token_sales_user1 = str(refresh_sales_user1.access_token)

        # Données du nouvel événement à créer
        new_event_data = {
            'event_name': 'Event Simpson',
            'contract': self.contract_user3.id,
            'client': self.client_user3.full_name,
            'client_contact': f"{self.client_user3.email} {self.client_user3.phone_number}",
            'event_date_start': make_aware(datetime.datetime(2025, 1, 24, 10, 30)),
            'event_date_end': make_aware(datetime.datetime(2025, 2, 15, 12, 45)),
            'support_contact': self.support_user1.full_name,
            'location': 'Australie',
            'attendees': 50,
            'notes': 'Event notes'
        }

        # Test la vue create pour créer un nouvel événement
        url = '/crm/events/'
        response = self.client.post(
            url, data=new_event_data, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token_sales_user1}'
        )

        # Vérifie que la réponse a le statut HTTP 201 (Created) car l'événement a été créé avec succès
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Affiche la réponse pour vérifier le message de succès
        print(response.data)

        # Vérifie que le message de succès est présent dans la réponse
        self.assertIn("Event successfully created.", response.data.get("message"))

        # Vérifie que les données de l'événement créé sont présentes dans la réponse
        self.assertIn("data", response.data)
        self.assertEqual(response.data["data"]["event_name"], new_event_data["event_name"])
        self.assertEqual(response.data["data"]["contract"], new_event_data["contract"])
        self.assertEqual(response.data["data"]["client"], new_event_data["client"])
        self.assertEqual(response.data["data"]["client_contact"], new_event_data["client_contact"])
        self.assertEqual(response.data["data"]["support_contact"], new_event_data["support_contact"])
        self.assertEqual(response.data["data"]["location"], new_event_data["location"])
        self.assertEqual(response.data["data"]["attendees"], new_event_data["attendees"])
        self.assertEqual(response.data["data"]["notes"], new_event_data["notes"])

        # Vérifie event_date_start et event_date_end
        expected_start_date = make_aware(datetime.datetime(2025, 1, 24, 10, 30))
        expected_end_date = make_aware(datetime.datetime(2025, 2, 15, 12, 45))

        # Convertit la chaîne de date dans la réponse JSON en un objet Pendulum
        response_start_date_str = response.data['data']['event_date_start']
        response_start_date = pendulum.parse(response_start_date_str)

        response_end_date_str = response.data['data']['event_date_end']
        response_end_date = pendulum.parse(response_end_date_str)

        self.assertEqual(response_start_date, expected_start_date)
        self.assertEqual(response_end_date, expected_end_date)

    def test_create_event_unauthorized_user(self):
        # Assure que client_user1 est associé à sales_user1
        self.assertEqual(self.client_user3.sales_contact, self.sales_user1)

        # Assure que contract_user1 pour client_user3 est signé
        self.assertTrue(self.contract_user3.status_contract)

        # Crée un jeton d'accès pour support_user2
        refresh_support_user2 = RefreshToken.for_user(self.support_user2)
        access_token_support_user2 = str(refresh_support_user2.access_token)

        # Données du nouvel événement à créer
        new_event_data = {
            'event_name': 'Event Simpson',
            'contract': self.contract_user3.id,
            'client': self.client_user3.full_name,
            'client_contact': f"{self.client_user3.email} {self.client_user3.phone_number}",
            'event_date_start': make_aware(datetime.datetime(2025, 1, 24, 10, 30)),
            'event_date_end': make_aware(datetime.datetime(2025, 2, 15, 12, 45)),
            'support_contact': self.support_user1.full_name,
            'location': 'Australie',
            'attendees': 50,
            'notes': 'Event notes'
        }

        # Test la vue create pour créer un nouvel événement avec le jeton d'accès de support_user2
        url = '/crm/events/'
        response = self.client.post(
            url, data=new_event_data, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token_support_user2}'
        )

        # Vérifie que la réponse a le statut HTTP 403 (Forbidden) car l'utilisateur n'est pas autorisé
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.content.decode())

        # Vérifie que le message de succès est présent dans la réponse
        self.assertIn("You do not have permission to create an event.", response.content.decode())

    def test_create_event_contract_not_signed(self):
        # Assure que le contrat pour client_user4 n'est pas signé
        self.assertFalse(self.contract_user4.status_contract)

        # Crée un jeton d'accès pour sales_user1
        refresh_sales_user1 = RefreshToken.for_user(self.sales_user1)
        access_token_sales_user1 = str(refresh_sales_user1.access_token)

        # Données du nouvel événement à créer
        new_event_data = {
            'event_name': 'Event Simpson',
            'contract': self.contract_user4.id,
            'client': self.client_user3.full_name,
            'client_contact': f"{self.client_user3.email} {self.client_user3.phone_number}",
            'event_date_start': make_aware(datetime.datetime(2025, 1, 24, 10, 30)),
            'event_date_end': make_aware(datetime.datetime(2025, 2, 15, 12, 45)),
            'support_contact': self.support_user1.full_name,
            'location': 'Australie',
            'attendees': 50,
            'notes': 'Event notes'
        }

        # Test la vue create pour créer un nouvel événement avec le jeton d'accès de sales_user1
        url = '/crm/events/'
        response = self.client.post(
            url, data=new_event_data, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token_sales_user1}'
        )

        # Vérifie que la réponse a le statut HTTP 403 (Forbidden) car le contrat n'est pas signé
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.content.decode())

        # Vérifie que le message d'erreur est présent dans la réponse
        self.assertIn("The associated contract is not signed. Cannot create the event.", response.content.decode())

    def test_create_event_already_exists(self):
        # Assure que le contrat pour client_user1 est signé
        self.assertTrue(self.contract_user1.status_contract)

        # Assure qu'un événement existe déjà pour ce contrat
        existing_event = self.create_event(
            event_name="Event Flanders",
            contract=self.contract_user1,
            client=self.client_user1,
            client_name=self.client_user1.full_name,
            client_contact=f"{self.client_user1.email} {self.client_user1.phone_number}",
            event_date_start=make_aware(datetime.datetime(2025, 2, 14, 12, 45)),
            event_date_end=make_aware(datetime.datetime(2025, 11, 25, 12, 55)),
            support_contact=self.support_user1,
            location="Rome",
            attendees=1,
            notes="Event notes"
        )

        # Crée un jeton d'accès pour sales_user1
        refresh_sales_user1 = RefreshToken.for_user(self.sales_user1)
        access_token_sales_user1 = str(refresh_sales_user1.access_token)

        # Données du nouvel événement à créer avec le même contrat
        new_event_data = {
            'event_name': 'Event Flanders',
            'contract': self.contract_user1.id,
            'client': self.client_user1.full_name,
            'client_contact': f"{self.client_user1.email} {self.client_user1.phone_number}",
            'event_date_start': make_aware(datetime.datetime(2025, 3, 1, 14, 30)),
            'event_date_end': make_aware(datetime.datetime(2025, 3, 1, 16, 30)),
            'support_contact': self.support_user1.full_name,
            'location': 'Paris',
            'attendees': 5,
            'notes': 'Event notes'
        }

        # Test la vue create pour créer un nouvel événement avec le même contrat
        url = '/crm/events/'
        response = self.client.post(
            url, data=new_event_data, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token_sales_user1}'
        )

        # Vérifie que la réponse a le statut HTTP 403 (Forbidden) car un événement existe déjà pour ce contrat
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.content.decode())

        # Vérifie que la variable existing_client est égale à self.client_user1
        self.assertEqual(existing_event.client, self.client_user1)

        # Vérifie que le message d'erreur est présent dans la réponse
        self.assertIn(
            "An event already exists for this contract. Cannot create another event.",
            response.content.decode()
        )

    def test_update_event(self):
        # Assure que event_user1 est associé à support_user1
        self.assertEqual(self.event_user1.support_contact, self.support_user1)

        # Assure que contract_user1 pour client_user1 est signé
        self.assertTrue(self.contract_user1.status_contract)

        # Crée un jeton d'accès pour support_user1
        refresh_support_user1 = RefreshToken.for_user(self.support_user1)
        access_token_support_user1 = str(refresh_support_user1.access_token)

        # Données de l'événement mis à jour
        update_event_data = {
            'event_name': 'Event Flanders',
            'contract': self.contract_user1.id,
            'client': self.client_user1.full_name,
            'client_contact': f"{self.client_user1.email} {self.client_user1.phone_number}",
            'event_date_start': make_aware(datetime.datetime(2025, 2, 14, 20, 45)),
            'event_date_end': make_aware(datetime.datetime(2025, 11, 25, 23, 55)),
            'support_contact': self.support_user1.full_name,
            'location': 'Londres',
            'attendees': 200,
            'notes': 'Event notes'
        }

        # Test de la vue update pour mettre à jour event_user1
        url = f'/crm/events/{self.event_user1.pk}/'
        response = self.client.put(
            url,
            data=json.dumps(update_event_data, default=str),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {access_token_support_user1}'
        )

        # Vérifie que la réponse a le statut HTTP 200 (OK) car l'événement a été mis à jour avec succès
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Affiche la réponse pour vérifier le message de succès
        print(response.data)

        # Vérifie que le message de succès est présent dans la réponse
        self.assertIn("Event successfully updated.", response.data.get("message"))

        # Vérifie que les données mises à jour de l'événement créé sont présentes dans la réponse
        self.assertIn("data", response.data)
        self.assertEqual(response.data["data"]["event_name"], update_event_data["event_name"])
        self.assertEqual(response.data["data"]["contract"], update_event_data["contract"])
        self.assertEqual(response.data["data"]["client"], update_event_data["client"])
        self.assertEqual(response.data["data"]["client_contact"], update_event_data["client_contact"])
        self.assertEqual(response.data["data"]["support_contact"], update_event_data["support_contact"])
        self.assertEqual(response.data["data"]["location"], update_event_data["location"])
        self.assertEqual(response.data["data"]["attendees"], update_event_data["attendees"])
        self.assertEqual(response.data["data"]["notes"], update_event_data["notes"])

        # Vérifie event_date_start et event_date_end
        expected_start_date = make_aware(datetime.datetime(2025, 2, 14, 20, 45))
        expected_end_date = make_aware(datetime.datetime(2025, 11, 25, 23, 55))

        # Convertit la chaîne de date dans la réponse JSON en un objet Pendulum
        response_start_date_str = response.data['data']['event_date_start']
        response_start_date = pendulum.parse(response_start_date_str)

        response_end_date_str = response.data['data']['event_date_end']
        response_end_date = pendulum.parse(response_end_date_str)

        self.assertEqual(response_start_date, expected_start_date)
        self.assertEqual(response_end_date, expected_end_date)

    def test_update_event_unauthorized_user(self):
        # Assure que event_user1 est associé à support_user1
        self.assertEqual(self.event_user1.support_contact, self.support_user1)

        # Assure que contract_user1 pour client_user1 est signé
        self.assertTrue(self.contract_user1.status_contract)

        # Crée un jeton d'accès pour support_user2
        refresh_support_user2 = RefreshToken.for_user(self.support_user2)
        access_token_support_user2 = str(refresh_support_user2.access_token)

        # Données de l'événement mis à jour
        update_event_data = {
            'event_name': 'Event Flanders',
            'contract': self.contract_user1.id,
            'client': self.client_user1.full_name,
            'client_contact': f"{self.client_user1.email} {self.client_user1.phone_number}",
            'event_date_start': make_aware(datetime.datetime(2025, 2, 14, 20, 45)),
            'event_date_end': make_aware(datetime.datetime(2025, 11, 25, 23, 55)),
            'support_contact': self.support_user1.full_name,
            'location': 'Londres',
            'attendees': 200,
            'notes': 'Event notes'
        }

        # Test de la vue update pour mettre à jour event_user1 avec le jeton d'accès de support_user2
        url = f'/crm/events/{self.event_user1.pk}/'
        response = self.client.put(
            url,
            data=json.dumps(update_event_data, default=str),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {access_token_support_user2}'
        )

        # Vérifie que la réponse a le statut HTTP 403 (Forbidden) car l'utilisateur n'est pas autorisé
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.content.decode())

        # Vérifie que le texte spécifié est présent dans la réponse
        self.assertIn("You do not have permission to update this event.", response.content.decode())

    def test_destroy_event(self):
        # Assure que le event_user1 est associé à support_user1
        self.assertEqual(self.event_user1.support_contact, self.support_user1)

        # Crée un jeton d'accès pour support_user1
        refresh_support_user1 = RefreshToken.for_user(self.support_user1)
        access_token_support_user1 = str(refresh_support_user1.access_token)

        # Données de l'événement à supprimer
        destroy_event_data = {
            'event_name': 'Event Flanders',
            'contract': self.contract_user1.id,
            'client': self.client_user1.full_name,
            'client_contact': f"{self.client_user1.email} {self.client_user1.phone_number}",
            'event_date_start': make_aware(datetime.datetime(2025, 2, 14, 12, 45)),
            'event_date_end': make_aware(datetime.datetime(2025, 11, 25, 12, 55)),
            'support_contact': self.support_user1.full_name,
            'location': 'Rome',
            'attendees': 1,
            'notes': 'Event notes'
        }

        # Test de la vue destroy pour supprimer event_user1
        url = f'/crm/events/{self.event_user1.pk}/'
        response = self.client.delete(
            url, data=destroy_event_data, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token_support_user1}'
        )

        # Vérifie que la réponse a le statut HTTP 204 (No Content) car l'événement a été supprimé avec succès
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.data)

        # Vérifie que le message de succès est présent dans la réponse
        self.assertIn("Event successfully deleted.", response.data.get("message"))

    def test_destroy_event_unauthorized_user(self):
        # Assure que le event_user1 est associé à support_user1
        self.assertEqual(self.event_user1.support_contact, self.support_user1)

        # Crée un jeton d'accès pour support_user2
        refresh_support_user2 = RefreshToken.for_user(self.support_user2)
        access_token_support_user2 = str(refresh_support_user2.access_token)

        # Données de l'événement à supprimer
        destroy_event_data = {
            'event_name': 'Event Flanders',
            'contract': self.contract_user1.id,
            'client': self.client_user1.full_name,
            'client_contact': f"{self.client_user1.email} {self.client_user1.phone_number}",
            'event_date_start': make_aware(datetime.datetime(2025, 2, 14, 12, 45)),
            'event_date_end': make_aware(datetime.datetime(2025, 11, 25, 12, 55)),
            'support_contact': self.support_user1.full_name,
            'location': 'Rome',
            'attendees': 1,
            'notes': 'Event notes'
        }

        # Test de la vue destroy pour supprimer event_user1 avec le jeton d'accès de support_user2
        url = f'/crm/events/{self.event_user1.pk}/'
        response = self.client.delete(
            url, data=destroy_event_data, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token_support_user2}'
        )

        # Vérifie que la réponse a le statut HTTP 403 (Forbidden) car l'utilisateur n'est pas autorisé
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.content.decode())

        # Vérifie que le message de succès est présent dans la réponse
        self.assertIn("You do not have permission to delete this event.", response.content.decode())
