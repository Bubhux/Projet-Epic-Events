import pytest
import json
from django.test import TestCase, Client
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import HTTP_401_UNAUTHORIZED
from django.contrib.auth import authenticate, login
from rest_framework.response import Response

from .models import User, Client, Group, add_client_to_group


@pytest.mark.django_db
class TestProfilesApp(TestCase):
    """
        Classe de test pour le module Profiles de l'application Epic Events.
        Cette classe contient plusieurs méthodes de test pour vérifier le bon fonctionnement
        des fonctionnalités liées aux profiles d'utilisateurs et aux clients dans l'application.
    """
    def create_superuser(self, email, role, full_name, phone_number, **extra_fields):
        """
            Crée et retourne un superutilisateur avec les paramètres spécifiés.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, role, full_name, phone_number, **extra_fields)

    def create_user(self, email, role, full_name, phone_number, is_staff=True, is_superuser=False):
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
            is_superuser=is_superuser,
        )

    def create_client(self, email, full_name, phone_number, company_name, user_contact=None, sales_contact=None):
        """
            Crée et retourne un client avec les paramètres spécifiés.
        """
        return Client.objects.create(
            email=email,
            full_name=full_name,
            phone_number=phone_number,
            company_name=company_name,
            user_contact=user_contact,
            sales_contact=sales_contact,
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
            user_contact=self.sales_user1,
            sales_contact=self.sales_user1,
        )

        self.client2 = self.create_client(
            email='Troyf@EpicEvents.com',
            full_name='Troy McClure',
            phone_number='+56781234',
            company_name='McClure & Co',
            user_contact=None,
            sales_contact=None,
        )

    def tearDown(self):
        """
            Méthode appelée après l'exécution de chaque test.
            Réinitialise l'état de la base de données.
        """
        # Supprime toutes les instances des modèles après chaque test
        User.objects.all().delete()
        Client.objects.all().delete()

    def test_create_superuser(self):
        """
            Teste la création d'un superutilisateur avec la méthode create_superuser.

            Vérifie que la méthode create_superuser crée un superutilisateur avec les paramètres par défaut
            (is_staff=True, is_superuser=True, role=User.ROLE_MANAGEMENT).
        """
        email = 'admin@example.com'
        password = 'adminpass'

        # Utilise la méthode create_superuser de la classe de test
        superuser = self.create_superuser(email, User.ROLE_MANAGEMENT, 'Admin User', '+123456789')

        # Vérifie que les attributs is_staff, is_superuser et role sont correctement définis
        assert superuser.is_staff is True
        assert superuser.is_superuser is True
        assert superuser.role == User.ROLE_MANAGEMENT

        # Vérifie que l'utilisateur a été correctement enregistré dans la base de données
        assert User.objects.filter(email=email).exists()

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
        expected_str = (
            f"Client ID: {new_client.id} "
            f"Jeff Albertson - Contact commercial {new_client.sales_contact.full_name}"
        )

        self.assertEqual(str(new_client), expected_str)

    def test_create_client2(self):
        """
            Vérifie la création et les propriétés d'un client.
        """
        new_client = self.client2
        new_client.save()

        self.assertEqual(new_client.full_name, 'Troy McClure')
        self.assertEqual(new_client.sales_contact, self.sales_user2)
        expected_str = (
            f"Client ID : {new_client.id} "
            f"Troy McClure - Contact commercial {new_client.sales_contact.full_name}"
        )
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

    def test_create_user_with_empty_email(self):
        """
            Teste la levée de l'exception ValueError lorsque la méthode create_user est appelée avec un e-mail vide.

            Vérifie que la création d'un utilisateur avec un e-mail vide déclenche une exception de type ValueError
            avec le message 'The Email field must be set'.
        """
        with pytest.raises(ValueError, match='The Email field must be set'):
            User.objects.create_user(
                email='',
                password='Pingou123',
                role=User.ROLE_MANAGEMENT,
                full_name='John Doe',
                phone_number='+123456789',
                is_staff=True
            )

    def test_create_superuser_invalid_attributes(self):
        """
            Teste la levée d'exceptions lorsque la méthode create_superuser est appelée avec des paramètres invalides.

            Vérifie que la méthode create_superuser lève une exception ValueError lorsque les paramètres
            is_staff ou is_superuser sont définis à False.
        """
        with pytest.raises(ValueError, match='Superuser must have is_staff=True.'):
            User.objects.create_superuser('admin@example.com', 'adminpass', is_staff=False)

        with pytest.raises(ValueError, match='Superuser must have is_superuser=True.'):
            User.objects.create_superuser('admin@example.com', 'adminpass', is_superuser=False)

    def test_has_perm(self):
        # Teste la méthode has_perm
        perm = 'some_permission'
        self.assertTrue(self.management_user.has_perm(perm))

    def test_has_module_perms(self):
        # Teste la méthode has_module_perms
        app_label = 'some_app'
        self.assertTrue(self.management_user.has_module_perms(app_label))

    def test_str_method_with_sales_contact(self):
        # Teste la méthode __str__ avec un contact commercial associé
        expected_str = f"Client ID : {self.client1.id} Jeff Albertson - Contact commercial {self.sales_user1.full_name}"
        self.assertEqual(str(self.client1), expected_str)

    def test_add_client_to_group(self):
        # Crée une instance de Client avec le contact commercial déjà existant
        client_instance = Client.objects.create(
            email='client@example.com',
            full_name='Test Client',
            phone_number='1234567890',
            company_name='Test Company',
            user_contact=self.sales_user1,
            sales_contact=self.sales_user1
        )

        # Supprime tous les groupes "Client" existants avant le test
        Group.objects.filter(name='Client').delete()

        # Vérifie si le groupe "Client" existe avant l'appel à la fonction add_client_to_group
        assert not Group.objects.filter(name='Client').exists()

        # Appelle la fonction add_client_to_group
        add_client_to_group(sender=None, instance=client_instance)

        # Vérifie si le groupe "Client" existe après l'appel à la fonction add_client_to_group
        assert Group.objects.filter(name='Client').exists()

        # Actualise l'instance avec les données actuelles de la base de données
        client_instance.refresh_from_db()

        # Vérifie si l'instance de Client est associée au groupe "Client"
        assert client_instance.sales_contact.groups.filter(name='Client').exists()

        # Vérifie si user_contact est correctement défini après l'appel à add_client_to_group
        assert client_instance.user_contact is not None

        # Réinitialise les groupes pour éviter des effets de bord sur d'autres tests
        client_instance.sales_contact.groups.clear()


@pytest.mark.django_db
class TestLoginViewSet(TestCase):
    """
        Classe de tests pour les vues de connexion (LoginViewSet).
    """
    def create_user(self, email, role, full_name, phone_number, is_staff=True, is_active=True):
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
            is_active=is_active,
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
            is_staff=True,
            is_active=True
        )

    def tearDown(self):
        """
            Méthode appelée après l'exécution de chaque test.
            Réinitialise l'état de la base de données.
        """
        # Supprime toutes les instances des modèles après chaque test
        User.objects.all().delete()

    def test_user_login_successful(self):
        """
            Teste la connexion réussie d'un utilisateur.
        """
        # Récupère l'utilisateur créé dans la méthode setUp()
        user = self.user

        # Envoie une demande POST à la vue
        url = reverse('obtain_token')
        data = {'email': user.email, 'password': 'Pingou123'}
        response = self.client.post(url, data, format='json')

        # Affiche la réponse pour vérifier le message
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_invalid_credentials(self):
        """
            Teste la connexion avec des identifiants invalides.
        """
        # Récupère l'utilisateur créé dans la méthode setUp()
        user = self.user

        # Envoie une demande POST à la vue
        url = reverse('obtain_token')
        data = {'email': user.email, 'password': 'wrongpassword'}
        response = self.client.post(url, data, format='json')

        # Affiche la réponse pour vérifier le message
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertIn('No active account found', response.data['detail'])

    def test_user_login_inactive_account(self):
        """
            Teste la connexion avec un utilisateur inactif.
        """
        # Récupère l'utilisateur créé dans la méthode setUp()
        user = self.user

        # Désactive l'utilisateur
        user.is_active = False
        user.save()

        # Envoie une demande POST à la vue
        url = reverse('obtain_token')
        data = {'email': user.email, 'password': 'Pingou123'}
        response = self.client.post(url, data, format='json')

        # Affiche la réponse pour vérifier le message
        print(response.data)

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertIn('No active account found with the given credentials', response.data['detail'])


@pytest.mark.django_db
class TestClientViewSet(TestCase):
    """
        Classe de tests pour les vues (ClientViewSet).
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

        self.support_user1 = self.create_user(
            email='Homer@EpicEvents-Support.com',
            role=User.ROLE_SUPPORT,
            full_name='Homer Simpson',
            phone_number='+345678912',
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
        refresh_sales_user1 = RefreshToken.for_user(self.sales_user1)
        self.access_token_sales_user1 = str(refresh_sales_user1.access_token)

        # Créer un jeton d'accès pour support_user1
        refresh_support_user1 = RefreshToken.for_user(self.support_user1)
        self.access_token_support_user1 = str(refresh_support_user1.access_token)

    def tearDown(self):
        """
            Méthode appelée après l'exécution de chaque test.
            Réinitialise l'état de la base de données.
        """
        # Supprime toutes les instances des modèles après chaque test
        User.objects.all().delete()
        Client.objects.all().delete()

    def test_clients_list(self):
        # Test de la vue clients_list
        url = '/crm/clients/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token_sales_user1}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

        # Affiche la totalité de la réponse JSON dans la console
        print("Response Data:", response.data)
        # print(json.dumps(response.data, indent=2))

    def test_client_details(self):
        # Assure que le client1 est associé à sales_user1
        self.assertEqual(self.client1.user_contact, self.sales_user1)

        # Crée un jeton d'accès pour sales_user1
        refresh_sales_user1 = RefreshToken.for_user(self.sales_user1)
        access_token_sales_user1 = str(refresh_sales_user1.access_token)

        # Test de la vue client_details pour le client associé à sales_user1
        url = f'/crm/clients/{self.client1.pk}/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token_sales_user1}')

        # Vérifie que la réponse a le statut HTTP 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vérifie que les données de la réponse correspondent aux détails du client
        self.assertEqual(response.data['id'], self.client1.pk)
        self.assertEqual(response.data['full_name'], self.client1.full_name)

        # Vérifie que l'accès a bien été autorisé
        self.assertIn('id', response.data)
        self.assertIn('full_name', response.data)

        # Affiche la totalité de la réponse JSON dans la console
        print("Response Data:", response.data)
        # print(json.dumps(response.data, indent=2))

    def test_client_details_unauthorized_user(self):
        # Assure que le client2 est associé à sales_user2
        self.assertEqual(self.client2.user_contact, self.sales_user2)

        # Crée un jeton d'accès pour sales_user1
        refresh_sales_user1 = RefreshToken.for_user(self.sales_user1)
        access_token_sales_user1 = str(refresh_sales_user1.access_token)

        # Test de la vue client_details pour le client associé à sales_user2 avec le jeton d'accès de sales_user1
        url = f'/crm/clients/{self.client2.pk}/client_details/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token_sales_user1}')

        # Vérifie que la réponse a le statut HTTP 403 (Forbidden) car l'utilisateur n'est pas autorisé
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.content.decode())

        # Vérifie que le texte spécifié est présent dans la réponse
        self.assertIn("You do not have permission to access this client.", response.content.decode())

    def test_all_clients_details(self):
        # Test la vue all_clients_details
        url = '/crm/clients/all_clients_details/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token_support_user1}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_create_client(self):
        # Créer un jeton d'accès pour sales_user1
        refresh_sales_user1 = RefreshToken.for_user(self.sales_user1)
        access_token_sales_user1 = str(refresh_sales_user1.access_token)

        # Données du nouveau client à créer
        new_client_data = {
            'email': 'Ned@EpicEvents.com',
            'full_name': 'Ned Flanders',
            'phone_number': '+987654321',
            'company_name': 'Flanders & Co'
        }

        # Test de la vue create pour créer un nouveau client
        url = '/crm/clients/'
        response = self.client.post(
            url, data=new_client_data, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token_sales_user1}'
        )

        # Vérifie que la réponse a le statut HTTP 201 (Created) car le client a été créé avec succès
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Affiche la réponse pour vérifier le message de succès
        print(response.data)

        # Vérifie que le message de succès est présent dans la réponse
        self.assertIn("Client successfully created.", response.data.get("message"))

        # Vérifie que les données du client créé sont présentes dans la réponse
        self.assertIn("data", response.data)
        self.assertEqual(response.data["data"]["full_name"], new_client_data["full_name"])
        self.assertEqual(response.data["data"]["email"], new_client_data["email"])

    def test_create_clients_unauthorized_user(self):
        # Créer un jeton d'accès pour support_user1
        refresh_support_user1 = RefreshToken.for_user(self.support_user1)
        access_token_support_user1 = str(refresh_support_user1.access_token)

        # Données du nouveau client à créer
        new_client_data = {
            'email': 'Ned@EpicEvents.com',
            'full_name': 'Ned Flanders',
            'phone_number': '+987654321',
            'company_name': 'Flanders & Co'
        }

        # Test de la vue create pour créer un nouveau client avec le jeton d'accès de support_user1
        url = '/crm/clients/'
        response = self.client.post(
            url, data=new_client_data, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token_support_user1}'
        )

        # Vérifie que la réponse a le statut HTTP 403 (Forbidden) car l'utilisateur n'est pas autorisé
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.content.decode())

        # Vérifie que le texte spécifié est présent dans la réponse
        self.assertIn("You do not have permission to create a client.", response.content.decode())

    def test_update_client(self):
        # Assure que le client1 est associé à sales_user1
        self.assertEqual(self.client1.user_contact, self.sales_user1)

        # Créer un jeton d'accès pour sales_user1
        refresh_sales_user1 = RefreshToken.for_user(self.sales_user1)
        access_token_sales_user1 = str(refresh_sales_user1.access_token)

        # Données du client mis à jour
        update_client_data = {
            'email': 'Jeff@EpicEvents.com',
            'full_name': 'Jeffrey Albertsons',
            'phone_number': '+123456789',
            'company_name': 'Albertson & Co'
        }

        # Test de la vue update pour mettre à jour le client1
        url = f'/crm/clients/{self.client1.pk}/'
        response = self.client.put(
            url,
            data=json.dumps(update_client_data),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {access_token_sales_user1}'
        )

        # Vérifie que la réponse a le statut HTTP 200 (OK) car le client a été mis à jour avec succès
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Affiche la réponse pour vérifier le message de succès
        print(response.data)

        # Vérifie que le message de succès est présent dans la réponse
        self.assertIn("Client successfully updated.", response.data.get("message"))

        # Vérifie que les données mises à jour du client créé sont présentes dans la réponse
        self.assertIn("data", response.data)
        self.assertEqual(response.data["data"]["full_name"], update_client_data["full_name"])
        self.assertEqual(response.data["data"]["email"], update_client_data["email"])

    def test_update_client_unauthorized_user(self):
        # Assure que le client2 est associé à sales_user2
        self.assertEqual(self.client2.user_contact, self.sales_user2)

        # Créer un jeton d'accès pour sales_user1
        refresh_sales_user1 = RefreshToken.for_user(self.sales_user1)
        access_token_sales_user1 = str(refresh_sales_user1.access_token)

        # Données du client mis à jour
        update_client_data = {
            'email': 'Troyf@EpicEvents.com',
            'full_name': 'Troy Boy McClure',
            'phone_number': '+123456789',
            'company_name': 'McClure & Co'
        }

        # Test de la vue update pour mettre à jour le client2 avec le jeton d'accès de sales_user1
        url = f'/crm/clients/{self.client2.pk}/'
        response = self.client.put(
            url, data=update_client_data, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token_sales_user1}'
        )

        # Vérifie que la réponse a le statut HTTP 403 (Forbidden) car l'utilisateur n'est pas autorisé
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.content.decode())

        # Vérifie que le texte spécifié est présent dans la réponse
        self.assertIn("You do not have permission to update this client.", response.content.decode())

    def test_destroy_client(self):
        # Assure que le client1 est associé à sales_user1
        self.assertEqual(self.client1.user_contact, self.sales_user1)

        # Créer un jeton d'accès pour sales_user1
        refresh_sales_user1 = RefreshToken.for_user(self.sales_user1)
        access_token_sales_user1 = str(refresh_sales_user1.access_token)

        # Données du client à supprimer
        destroy_client_data = {
            'email': 'Ned@EpicEvents.com',
            'full_name': 'Ned Flanders',
            'phone_number': '+987654321',
            'company_name': 'Flanders & Co'
        }

        # Test de la vue destroy pour supprimer le client1
        url = f'/crm/clients/{self.client1.pk}/'
        response = self.client.delete(
            url, data=destroy_client_data, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token_sales_user1}'
        )

        # Vérifie que la réponse a le statut HTTP 204 (No Content) car le client a été supprimé avec succès
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.data)

        # Vérifie que le message de succès est présent dans la réponse
        self.assertIn("Client successfully deleted.", response.data.get("message"))

    def test_destroy_client_unauthorized_user(self):
        # Assure que le client2 est associé à sales_user2
        self.assertEqual(self.client2.user_contact, self.sales_user2)

        # Créer un jeton d'accès pour sales_user1
        refresh_sales_user1 = RefreshToken.for_user(self.sales_user1)
        access_token_sales_user1 = str(refresh_sales_user1.access_token)

        # Données du client à supprimer
        destroy_client_data = {
            'email': 'Troyf@EpicEvents.com',
            'full_name': 'Troy Boy McClure',
            'phone_number': '+123456789',
            'company_name': 'McClure & Co'
        }

        # Test de la vue destroy pour supprimer le client2 avec le jeton d'accès de sales_user1
        url = f'/crm/clients/{self.client2.pk}/'
        response = self.client.delete(
            url, data=destroy_client_data, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token_sales_user1}'
        )

        # Vérifie que la réponse a le statut HTTP 403 (Forbidden) car l'utilisateur n'est pas autorisé
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.content.decode())

        # Vérifie que le texte spécifié est présent dans la réponse
        self.assertIn("You do not have permission to delete this client.", response.content.decode())


@pytest.mark.django_db
class TestUserViewSet(TestCase):
    """
        Classe de tests pour les vues (UserViewSet).
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
        self.management_user = self.create_user(
            email='Milhouse@EpicEvents-Management.com',
            role=User.ROLE_MANAGEMENT,
            full_name='Milhouse Van Houten',
            phone_number='+567891234',
            is_staff=True
        )

        self.sales_user = self.create_user(
            email='Joe@EpicEvents-Sales.com',
            role=User.ROLE_SALES,
            full_name='Joe Quimby',
            phone_number='+456789123',
            is_staff=True
        )

        self.support_user = self.create_user(
            email='Homer@EpicEvents-Support.com',
            role=User.ROLE_SUPPORT,
            full_name='Homer Simpson',
            phone_number='+345678912',
            is_staff=True
        )

        # Créer un jeton d'accès pour management_user
        refresh_management = RefreshToken.for_user(self.management_user)
        self.access_token_management = str(refresh_management.access_token)

        # Créer un jeton d'accès pour sales_user
        refresh_sales = RefreshToken.for_user(self.sales_user)
        self.access_token_sales = str(refresh_sales.access_token)

        # Créer un jeton d'accès pour support_user
        refresh_support = RefreshToken.for_user(self.support_user)
        self.access_token_support = str(refresh_support.access_token)

    def tearDown(self):
        """
            Méthode appelée après l'exécution de chaque test.
            Réinitialise l'état de la base de données.
        """
        # Supprime toutes les instances des modèles après chaque test
        User.objects.all().delete()

    def test_users_list(self):
        # Test la vue users_list
        url = '/crm/users/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token_support}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

        # Affiche la totalité de la réponse JSON dans la console
        print("Response Data:", response.data)
        # print(json.dumps(response.data, indent=2))

    def test_user_details(self):
        # Crée un jeton d'accès pour support_user
        refresh_support = RefreshToken.for_user(self.support_user)
        access_token_support = str(refresh_support.access_token)

        # Test de la vue user_details pour l'utilisateur support_user
        url = f'/crm/users/{self.sales_user.pk}/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token_support}')

        # Vérifie que la réponse a le statut HTTP 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vérifie que les données de la réponse correspondent aux détails de l'utilisateur
        self.assertEqual(response.data['id'], self.sales_user.pk)
        self.assertEqual(response.data['full_name'], self.sales_user.full_name)

        # Vérifie que l'accès a bien été autorisé
        self.assertIn('id', response.data)
        self.assertIn('full_name', response.data)

        # Vérifie que l'utilisateur a les données de l'utilisateur
        self.assertEqual(response.data['id'], self.sales_user.pk)
        self.assertEqual(response.data['full_name'], self.sales_user.full_name)

        # Affiche la totalité de la réponse JSON dans la console
        print("Response Data:", response.data)
        # print(json.dumps(response.data, indent=2))

    def test_all_users_details(self):
        # Test la vue all_users_details
        url = '/crm/users/all_users_details/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token_support}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_create_user(self):
        # Assure que le management_user a bien le rôle ROLE_MANAGEMENT
        self.assertEqual(self.management_user.role, User.ROLE_MANAGEMENT)

        # Créer un jeton d'accès pour management_user
        refresh_management_user = RefreshToken.for_user(self.management_user)
        access_token_management_user = str(refresh_management_user.access_token)

        # Données du nouvel utilisateur à créer
        new_user_data = {
            'email': 'Marge@EpicEvents-Sales.com',
            'full_name': 'Marge Simpson',
            'phone_number': '+123456789',
            'role': User.ROLE_SALES,
            'password': 'Pingou123',
            'is_staff': 'True'
        }

        # Test de la vue create pour créer un nouvel utilisateur
        url = '/crm/users/'
        response = self.client.post(
            url, data=new_user_data, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token_management_user}'
        )

        # Vérifie que la réponse a le statut HTTP 201 (Created) car l'utilisateur a été créé avec succès
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Affiche la réponse pour vérifier le message de succès
        print(response.data)

        # Vérifie que le message de succès est présent dans la réponse
        self.assertIn("User successfully created.", response.data.get("message"))

        # Vérifie que les données de l'utilisateur créé sont présentes dans la réponse
        self.assertIn("data", response.data)
        self.assertEqual(response.data["data"]["full_name"], new_user_data["full_name"])
        self.assertEqual(response.data["data"]["email"], new_user_data["email"])

    def test_create_user_unauthorized_user(self):
        # Créer un jeton d'accès pour sales_user
        refresh_sales_user = RefreshToken.for_user(self.sales_user)
        access_token_sales_user = str(refresh_sales_user.access_token)

        # Données du nouvel utilisateur à créer
        new_user_data = {
            'email': 'Marge@EpicEvents-Sales.com',
            'full_name': 'Marge Simpson',
            'phone_number': '+123456789',
            'role': User.ROLE_SALES,
            'password': 'Pingou123',
            'is_staff': 'True'
        }

        # Test de la vue create pour créer un nouvel utilisateur avec le jeton d'accès de sales_user
        url = '/crm/users/'
        response = self.client.post(
            url, data=new_user_data, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token_sales_user}'
        )

        # Vérifie que la réponse a le statut HTTP 403 (Forbidden) car l'utilisateur n'est pas autorisé
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.content.decode())

        # Vérifie que le texte spécifié est présent dans la réponse
        self.assertIn("You do not have permission to create a user.", response.content.decode())

    def test_update_user(self):
        # Assure que le management_user a bien le rôle ROLE_MANAGEMENT
        self.assertEqual(self.management_user.role, User.ROLE_MANAGEMENT)

        # Créer un jeton d'accès pour management_user
        refresh_management_user = RefreshToken.for_user(self.management_user)
        access_token_management_user = str(refresh_management_user.access_token)

        # Données de l'utilisateur mis à jour
        update_user_data = {
            'email': 'Joe@EpicEvents-Sales.com',
            'full_name': 'Joey Quimby',
            'phone_number': '+456789123',
            'role': User.ROLE_SALES,
            'password': 'Pingou123',
            'is_staff': 'True'
        }

        # Test de la vue update pour mettre à jour l'utilisateur
        url = f'/crm/users/{self.sales_user.pk}/'
        response = self.client.put(
            url,
            data=json.dumps(update_user_data),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {access_token_management_user}'
        )

        # Vérifie que la réponse a le statut HTTP 200 (OK) car l'utilisateur a été mis à jour avec succès
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Affiche la réponse pour vérifier le message de succès
        print(response.data)

        # Vérifie que le message de succès est présent dans la réponse
        self.assertIn("User successfully updated.", response.data.get("message"))

        # Vérifie que les données mises à jour du client créé sont présentes dans la réponse
        self.assertIn("data", response.data)
        self.assertEqual(response.data["data"]["full_name"], update_user_data["full_name"])
        self.assertEqual(response.data["data"]["email"], update_user_data["email"])

    def test_update_user_unauthorized_user(self):
        # Créer un jeton d'accès pour support_user
        refresh_support_user = RefreshToken.for_user(self.support_user)
        access_token_support_user = str(refresh_support_user.access_token)

        # Données de l'utilisateur mis à jour
        update_user_data = {
            'email': 'Joe@EpicEvents-Sales.com',
            'full_name': 'Joey Quimby',
            'phone_number': '+456789123',
            'role': User.ROLE_SALES,
            'password': 'Pingou123',
            'is_staff': 'True'
        }

        # Test de la vue update pour mettre à jour sales_user avec le jeton d'accès de support_user
        url = f'/crm/users/{self.sales_user.pk}/'
        response = self.client.put(
            url, data=update_user_data, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token_support_user}'
        )

        # Vérifie que la réponse a le statut HTTP 403 (Forbidden) car l'utilisateur n'est pas autorisé
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.content.decode())

        # Vérifie que le texte spécifié est présent dans la réponse
        self.assertIn("You do not have permission to update this user.", response.content.decode())

    def test_destroy_user(self):
        # Assure que le management_user a bien le rôle ROLE_MANAGEMENT
        self.assertEqual(self.management_user.role, User.ROLE_MANAGEMENT)

        # Créer un jeton d'accès pour management_user
        refresh_management_user = RefreshToken.for_user(self.management_user)
        access_token_management_user = str(refresh_management_user.access_token)

        # Données de l'utilisateur à supprimer
        destroy_user_data = {
            'email': 'Marge@EpicEvents-Sales.com',
            'full_name': 'Marge Simpson',
            'phone_number': '+123456789',
            'role': User.ROLE_SALES,
            'password': 'Pingou123',
            'is_staff': 'True'
        }

        # Test de la vue destroy pour supprimer sales_user
        url = f'/crm/users/{self.sales_user.pk}/'
        response = self.client.delete(
            url, data=destroy_user_data, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token_management_user}'
        )

        # Vérifie que la réponse a le statut HTTP 204 (No Content) car l'utilisateur a été supprimé avec succès
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.data)

        # Vérifie que le message de succès est présent dans la réponse
        self.assertIn("User successfully deleted.", response.data.get("message"))

    def test_destroy_user_unauthorized_user(self):
        # Créer un jeton d'accès pour support_user
        refresh_support_user = RefreshToken.for_user(self.support_user)
        access_token_support_user = str(refresh_support_user.access_token)

        # Données de l'utilisateur à supprimer
        destroy_user_data = {
            'email': 'Marge@EpicEvents-Sales.com',
            'full_name': 'Marge Simpson',
            'phone_number': '+123456789',
            'role': User.ROLE_SALES,
            'password': 'Pingou123',
            'is_staff': 'True'
        }

        # Test de la vue destroy pour supprimer sales_user avec le jeton d'accès de support_user
        url = f'/crm/users/{self.sales_user.pk}/'
        response = self.client.delete(
            url, data=destroy_user_data, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token_support_user}'
        )

        # Vérifie que la réponse a le statut HTTP 403 (Forbidden) car l'utilisateur n'est pas autorisé
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Affiche la réponse pour vérifier que le message spécifié est présent
        print(response.content.decode())

        # Vérifie que le texte spécifié est présent dans la réponse
        self.assertIn("You do not have permission to delete this user.", response.content.decode())
