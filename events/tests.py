import pytest
import json
import datetime
from django.test import TestCase, Client
from django.utils import timezone
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

    def create_event(self, event_name, contract, client, client_name, client_contact, event_date_start, event_date_end, support_contact, location, attendees, notes):
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
            Met en place les données nécessaires pour les tests.
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
            event_date_start = make_aware(datetime.datetime(2024, 2, 14, 12, 45)),
            event_date_end=make_aware(datetime.datetime(2024, 11, 25, 12, 55)),
            support_contact=self.support_user1,
            location="Rome",
            attendees=1,
            notes="Event notes"
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
        Event.objects.all().delete()

    def test_event_str_representation(self):
        """Teste la méthode __str__ du modèle Event."""
        # Définis les valeurs initiales
        self.event_user1.contract = self.contract_user1
        self.event_user1.support_contact = self.support_user1
        self.event_user1.client = self.client_user1
        
        # Sauvegarde l'événement après avoir lié le client
        self.event_user1.save()
        
        # Chaîne attendue pour l'événement créé avec un client
        expected_str_event_created = f"Evénement ID: {self.event_user1.id} {self.event_user1.event_name} - {self.event_user1.client_name}"
        self.assertEqual(str(self.event_user1), expected_str_event_created)

    def test_event_print_details(self):
        """Teste la méthode print_details du modèle Event."""
        # Définis les valeurs initiales
        self.event_user1.contract = self.contract_user1
        self.event_user1.support_contact = self.support_user1
        self.event_user1.client = self.client_user1

        # Appelle la méthode print_details
        self.event_user1.print_details()

        # Chaîne attendue pour les détails de l'événement
        expected_output = f"\nID de l'événement : {self.event_user1.id}\n" \
                            f"Nom de l'événement : {self.event_user1.event_name}\n" \
                            f"ID du contrat associé : {self.event_user1.contract}\n" \
                            f"Nom du client : {self.client_user1.full_name}\n" \
                            f"E-mail du client : {self.client_user1.email}\n" \
                            f"Compagnie du client : {self.client_user1.company_name}\n" \
                            f"Contact du client : {self.event_user1.client_contact}\n" \
                            f"Date de début de l'événement : {self.event_user1.event_date_start}\n" \
                            f"Date de fin de l'événement : {self.event_user1.event_date_end}\n" \
                            f"Contact de support : {self.support_user1.full_name}\n" \
                            f"Lieu : {self.event_user1.location}\n" \
                            f"Nombre d'invités : {self.event_user1.attendees}\n" \
                            f"Notes : {self.event_user1.notes}\n\n"

        # Compare les attributs de l'événement avec les valeurs attendues
        self.assertEqual(self.event_user1.id, 1)
        self.assertEqual(self.event_user1.event_name, 'Event Flanders')
        self.assertEqual(self.client_user1.full_name, 'Ned Flanders')
        self.assertEqual(self.client_user1.email, 'Ned@EpicEvents.com')
        self.assertEqual(self.client_user1.company_name, 'Flanders & Co')
        self.assertEqual(self.event_user1.client_contact, 'Ned@EpicEvents.com +987654321')
        self.assertEqual(self.event_user1.event_date_start, make_aware(datetime.datetime(2024, 2, 14, 12, 45)))
        self.assertEqual(self.event_user1.event_date_end, make_aware(datetime.datetime(2024, 11, 25, 12, 55)))
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
            event_date_start=make_aware(datetime.datetime(2024, 2, 14, 12, 45)),
            event_date_end=make_aware(datetime.datetime(2024, 11, 25, 12, 55)),
            support_contact=self.support_user1,
            location="Rome",
            attendees=1,
            notes="Event notes"
        )

        # Associez le contrat et le client à l'événement
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

    def create_client(self, email, full_name, phone_number, company_name,sales_contact=None):
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

    def create_event(self, event_name, contract, client, client_name, client_contact, event_date_start, event_date_end, support_contact, location, attendees, notes):
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
            Met en place les données nécessaires pour les tests.
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

        self.support_user2 = self.create_user(
            email='Tahiti@EpicEvents-Support.com',
            role=User.ROLE_SUPPORT,
            full_name='Tahiti Bob',
            phone_number='+456789123',
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
            client_name=self.client_user1.full_name,
            client_contact=f"{self.client_user1.email} {self.client_user1.phone_number}",
            event_date_start=make_aware(datetime.datetime(2024, 2, 14, 12, 45)),
            event_date_end=make_aware(datetime.datetime(2024, 11, 25, 12, 55)),
            support_contact=self.support_user1,
            location="Rome",
            attendees=1,
            notes="Event notes"
        )

        # Créer un jeton d'accès pour sales_user1
        refresh_sales_user1 = RefreshToken.for_user(self.sales_user1)
        self.access_token_sales_user1 = str(refresh_sales_user1.access_token)

        # Créer un jeton d'accès pour management_user1
        refresh_management_user1 = RefreshToken.for_user(self.management_user1)
        self.access_token_management_user1 = str(refresh_management_user1.access_token)

        # Créer un jeton d'accès pour support_user1
        refresh_support1 = RefreshToken.for_user(self.support_user1)
        self.access_token_support1 = str(refresh_support1.access_token)

        # Créer un jeton d'accès pour support_user2
        refresh_support2 = RefreshToken.for_user(self.support_user2)
        self.access_token_support2 = str(refresh_support2.access_token)

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

        print("Response Data:", response.data)

    def test_event_details(self):
        pass

    def test_event_details_unauthorized_user(self):
        pass

    def test_all_events_details(self):
        pass

    def test_filtered_events(self):
        pass

    def test_create_event(self):
        pass

    def test_create_event_unauthorized_user(self):
        pass

    def test_update_event(self):
        pass

    def test_update_event_unauthorized_user(self):
        pass

    def test_destroy_event(self):
        pass

    def test_destroy_event_unauthorized_user(self):
        pass
