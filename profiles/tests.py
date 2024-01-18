import pytest
from django.test import TestCase, Client
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Client, Group
from .serializers import UserLoginSerializer, ClientListSerializer, ClientDetailSerializer


@pytest.mark.django_db
class TestProfilesApp(TestCase):
    """
        Classe de test pour le module Profiles de l'application Epic Events.

        Cette classe contient plusieurs méthodes de test pour vérifier le bon fonctionnement
        des fonctionnalités liées aux profils d'utilisateurs et aux clients dans l'application.
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

    def setUp(self):
        """
            Met en place les données nécessaires pour les tests.
        """
        self.management_user = self.create_user(
            email='Martin@EpicEvents-Management.com',
            role=User.ROLE_MANAGEMENT,
            full_name='Martin Prince',
            phone_number='+234567891',
            is_staff=True,
        )

        self.support_user = self.create_user(
            email='Carl@EpicEvents-Support.com',
            role=User.ROLE_SUPPORT,
            full_name='Carl Carlson',
            phone_number='+567891234',
            is_staff=True,
        )

        self.sales_user1 = self.create_user(
            email='Timothy@EpicEvents-Sales.com',
            role=User.ROLE_SALES,
            full_name='Timothy Lovejoy',
            phone_number='+345678912',
            is_staff=True
        )

        self.sales_user2 = self.create_user(
            email='Joe@EpicEvents-Sales.com',
            role=User.ROLE_SALES,
            full_name='Joe Quimby',
            phone_number='+45678913',
            is_staff=True
        )

        self.client1 = self.create_client(
            email='Jeff@EpicEvents.com',
            full_name='Jeff Albertson',
            phone_number='+123456789',
            company_name='Albertson & Co',
        )

        self.client2 = self.create_client(
            email='Troyf@EpicEvents.com',
            full_name='Troy McClure',
            phone_number='+56781234',
            company_name='McClure & Co',
        )

    def test_create_user_management(self):
        """
            Vérifie la création et les propriétés d'un utilisateur de gestion.
        """
        new_user = self.management_user
        new_user.save()

        self.assertEqual(new_user.get_role_display(), 'Équipe Gestion')
        expected_str = f"User ID : {new_user.id} Équipe Gestion - {new_user.full_name} ({new_user.email})"
        self.assertEqual(str(new_user), expected_str)

    def test_create_user_support(self):
        """
            Vérifie la création et les propriétés d'un utilisateur de support.
        """
        new_user = self.support_user
        new_user.save()

        self.assertEqual(new_user.get_role_display(), 'Équipe Support')
        expected_str = f"User ID : {new_user.id} Équipe Support - {new_user.full_name} ({new_user.email})"
        self.assertEqual(str(new_user), expected_str)

    def test_create_user_sales(self):
        """
            Vérifie la création et les propriétés d'un utilisateur commercial.
        """
        new_user = self.sales_user1
        new_user.save()

        self.assertEqual(new_user.get_role_display(), 'Équipe Commerciale')
        expected_str = f"User ID : {new_user.id} Équipe Commerciale - {new_user.full_name} ({new_user.email})"
        self.assertEqual(str(new_user), expected_str)

    def test_create_client1(self):
        """
            Vérifie la création et les propriétés d'un client.
        """
        new_client = self.client1
        new_client.save()

        self.assertEqual(new_client.full_name, 'Jeff Albertson')
        self.assertEqual(new_client.sales_contact, self.sales_user1)
        expected_str = f"Client ID : {new_client.id} Jeff Albertson - Contact commercial {new_client.sales_contact.full_name}"
        self.assertEqual(str(new_client), expected_str)

    def test_create_client2(self):
        """
            Vérifie la création et les propriétés d'un client.
        """
        new_client = self.client2
        new_client.save()

        self.assertEqual(new_client.full_name, 'Troy McClure')
        self.assertEqual(new_client.sales_contact, self.sales_user2)
        expected_str = f"Client ID : {new_client.id} Troy McClure - Contact commercial {new_client.sales_contact.full_name}"
        self.assertEqual(str(new_client), expected_str)

    def test_assign_sales_contact(self):
        """
            Vérifie l'attribution correcte des contacts de vente aux clients.
        """
        client_group, created = Group.objects.get_or_create(name='Client')

        self.client1.assign_sales_contact()
        self.client2.assign_sales_contact()

        self.assertEqual(self.client1.sales_contact, self.sales_user1)
        self.assertEqual(self.client2.sales_contact, self.sales_user2)

        # Vérifie si l'utilisateur associé au client1 est dans client_group
        client_user1 = self.client1.sales_contact
        self.assertIn(client_user1, client_group.user_set.all())

        # Vérifie si l'utilisateur associé au client2 est dans client_group
        client_user2 = self.client2.sales_contact
        self.assertIn(client_user2, client_group.user_set.all())

    def test_obtain_jwt_token_url(self):
        """
            Vérifie que l'URL pour l'obtention du token JWT lors de la connexion est correcte.
        """
        # Obtiens l'URL à partir du nom de la vue
        url = reverse('obtain_token')

        # Vérifie que l'URL est correcte
        self.assertEqual(url, '/crm/login/')

        # Vérifie que l'URL est correctement résolue vers la vue associée
        view = resolve(url)
        self.assertEqual(view.func.view_class, TokenObtainPairView)

    def test_refresh_jwt_token_url(self):
        """
            Vérifie que l'URL pour le rafraîchissement du token JWT est correcte.
        """
        # Obtiens l'URL à partir du nom de la vue
        url = reverse('refresh_token')

        # Vérifie que l'URL est correcte
        self.assertEqual(url, '/crm/token/refresh/')

        # Vérifie que l'URL est correctement résolue vers la vue associée
        view = resolve(url)
        self.assertEqual(view.func.view_class, TokenRefreshView)


@pytest.mark.django_db
class TestLoginViewSet(TestCase):
    """
        Classe de tests pour les vues de connexion (LoginViewSet).
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

    def setUp(self):
        """
            Met en place les données nécessaires pour les tests.
        """
        self.user = self.create_user(
            email='Timothy@EpicEvents-Sales.com',
            role=User.ROLE_SALES,
            full_name='Timothy Lovejoy',
            phone_number='+345678912',
            is_staff=True
        )

    def test_user_login_successful(self):
        """
            Teste la connexion réussie d'un utilisateur.
        """
        url = reverse('obtain_token')
        data = {'email': 'Timothy@EpicEvents-Sales.com', 'password': 'Pingou123'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_invalid_credentials(self):
        """
            Teste la connexion avec des identifiants invalides.
        """
        url = reverse('obtain_token')
        data = {'email': 'Timothy@EpicEvents-Sales.com', 'password': 'wrongpassword'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertIn('No active account found', response.data['detail'])


@pytest.mark.django_db
class TestClientViewSet(TestCase):

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

    def create_client(self, email, full_name, phone_number, company_name, sales_contact, user_contact):
        """
            Crée et retourne un client avec les paramètres spécifiés.
        """
        return Client.objects.create(
            email=email,
            full_name=full_name,
            phone_number=phone_number,
            company_name=company_name,
            sales_contact=sales_contact,
            user_contact=user_contact,
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
            email='Joe@EpicEvents-Sales.com',
            role=User.ROLE_SALES,
            full_name='Joe Quimby',
            phone_number='+45678913',
            is_staff=True
        )

        self.client1 = self.create_client(
            email='Jeff@EpicEvents.com',
            full_name='Jeff Albertson',
            phone_number='+123456789',
            company_name='Albertson & Co',
            sales_contact=self.sales_user1,
            user_contact=self.sales_user1
        )

        self.client2 = self.create_client(
            email='Troyf@EpicEvents.com',
            full_name='Troy McClure',
            phone_number='+56781234',
            company_name='McClure & Co',
            sales_contact=self.sales_user2,
            user_contact=self.sales_user2
        )

        # Créer un jeton d'accès pour sales_user1
        refresh = RefreshToken.for_user(self.sales_user1)
        self.access_token = str(refresh.access_token)

    def test_clients_list(self):
        # Test la vue clients_list
        url = '/crm/clients/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_client_details(self):
        # Assure que le client1 est associé à sales_user1
        self.assertEqual(self.client1.user_contact, self.sales_user1)

        # Crée un jeton d'accès pour sales_user1
        refresh = RefreshToken.for_user(self.sales_user1)
        access_token = str(refresh.access_token)

        # Test de la vue client_details pour le client associé à sales_user1
        url = f'/crm/clients/{self.client1.pk}/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Vérifie que la réponse a le statut HTTP 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vérifie que les données de la réponse correspondent aux détails du client
        self.assertEqual(response.data['id'], self.client1.pk)
        self.assertEqual(response.data['full_name'], self.client1.full_name)

        # Vérifie que l'accès a bien été autorisé
        self.assertIn('id', response.data)
        self.assertIn('full_name', response.data)

        # Vérifie que l'utilisateur a les données du client
        self.assertEqual(response.data['id'], self.client1.pk)
        self.assertEqual(response.data['full_name'], self.client1.full_name)

    def test_client_details_unauthorized_user(self):
        # Assure que le client2 est associé à sales_user2
        self.assertEqual(self.client2.user_contact, self.sales_user2)

        # Crée un jeton d'accès pour sales_user1
        refresh = RefreshToken.for_user(self.sales_user1)
        access_token = str(refresh.access_token)

        # Test de la vue client_details pour le client associé à sales_user2 avec le jeton d'accès de sales_user1
        url = f'/crm/clients/{self.client2.pk}/client_details/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Vérifie que la réponse a le statut HTTP 403 (Forbidden) car l'utilisateur n'est pas autorisé
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.content.decode())

        # Vérifie que le texte spécifié est présent dans la réponse
        self.assertIn("You do not have permission to access this client.", response.content.decode())
