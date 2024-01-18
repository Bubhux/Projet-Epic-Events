import pytest
import json
from django.test import TestCase, Client
from django.utils import timezone
from django.utils.timezone import make_aware
from rest_framework import status

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
        pass

    def create_client(self, email, full_name, phone_number, company_name):
        pass

    def create_contract(self, client, total_amount, remaining_amount, sales_contact=None, status_contract=False):
        pass

    def create_event(self, event_name, contract, client_name, client_contact, event_date_start, event_date_end, support_contact, location, attendees, notes):
        pass

    def setUp(self):
        """
            Met en place les données nécessaires pour les tests.
        """
        pass

    def tearDown(self):
        """
            Méthode appelée après l'exécution de chaque test.
            Réinitialise l'état de la base de données.
        """
        pass

    def test_event_str_representation(self):
        pass

    def test_event_print_details(self):
        pass

    def test_save_method(self):
        pass


@pytest.mark.django_db
class TestEventViewSet(TestCase):
    """
        Classe de tests pour les vues (EventViewSet).
    """
    def create_user(self, email, role, full_name, phone_number, is_staff=True):
        pass

    def create_client(self, email, full_name, phone_number, company_name):
        pass

    def create_contract(self, client, total_amount, remaining_amount, sales_contact=None, status_contract=False):
        pass

    def create_event(self, event_name, contract, client_name, client_contact, event_date_start, event_date_end, support_contact, location, attendees, notes):
        pass

    def setUp(self):
        """
            Met en place les données nécessaires pour les tests.
        """
        pass

    def tearDown(self):
        """
            Méthode appelée après l'exécution de chaque test.
            Réinitialise l'état de la base de données.
        """
        pass

    def test_events_list(self):
        pass

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
