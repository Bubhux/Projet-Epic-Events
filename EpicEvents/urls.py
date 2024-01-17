"""
URL configuration for EpicEvents project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from profiles.views import LoginViewSet, ClientViewSet, UserViewSet, AdminUserLoginViewSet, AdminUserViewSet, AdminUserClientViewSet
from contracts.views import ContractViewSet, AdminContractViewSet


# Création du routeur simple
router = SimpleRouter()

router.register(r"users", UserViewSet, basename="users")
router.register(r"clients", ClientViewSet, basename="clients")
router.register(r"contracts", ContractViewSet, basename="contracts")

router.register(r"users/(?P<user_pk>\d+)/", UserViewSet, basename="users")
router.register(r"users/(?P<user_pk>\d+)/user_details", UserViewSet, basename="user-details")

router.register(r"clients/(?P<client_pk>\d+)/", ClientViewSet, basename="clients")
router.register(r"clients/(?P<client_pk>\d+)/client_details", ClientViewSet, basename="client-details")

router.register(r"contracts/(?P<contract_pk>\d+)/", ContractViewSet, basename="contracts")
router.register(r"contracts/(?P<contract_pk>\d+)/contract_details", ContractViewSet, basename="contract-details")

router.register(r"admin/login", AdminUserLoginViewSet, basename="admin-login")
router.register(r"admin/users", AdminUserViewSet, basename="admin-users")
router.register(r"admin/clients", AdminUserClientViewSet, basename="admin-clients")
router.register(r"admin/contracts", AdminContractViewSet, basename="admin-contracts")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('crm-auth/', include('rest_framework.urls')),

    # URL pour l'obtention du token JWT lors de la connexion
    path('crm/login/', TokenObtainPairView.as_view(), name='obtain_token'),

    # URL pour le rafraîchissement du token JWT
    path('crm/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),

    # Configure le chemin pour l'action 'all_users_details' et 'user_details'
    path('crm/users/all_users_details/', UserViewSet.as_view({'get': 'all_users_details'}), name='all-users-details'),
    path('crm/users/user_details/<int:pk>/', UserViewSet.as_view({'get': 'user_details'}), name='user-details'),

    # Configure le chemin pour l'action 'all_clients_details' et 'client_details'
    path('crm/clients/all_clients_details/', ClientViewSet.as_view({'get': 'all_clients_details'}), name='all-clients-details'),
    path('crm/clients/client_details/<int:pk>/', ClientViewSet.as_view({'get': 'client_details'}), name='client-details'),

    # Configure le chemin pour l'action 'all_contracts_details' et 'contract_details'
    path('crm/contract/all_contracts_details/', ContractViewSet.as_view({'get': 'all_contracts_details'}), name='all-contracts-details'),
    path('crm/contract/contract_details/<int:pk>/', ContractViewSet.as_view({'get': 'contract_details'}), name='contract-details'),

    # Inclusion des URLs gérées par le routeur simple sous le préfixe "crm/"
    path('crm/', include(router.urls))
]
