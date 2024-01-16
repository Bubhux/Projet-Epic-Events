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

from profiles.views import LoginViewSet, ClientViewSet, UserViewSet
# from contracts.views import ContractClientViewSet


# Création du routeur simple
router = SimpleRouter()

router.register(r"clients", ClientViewSet, basename="clients")
router.register(r"users", UserViewSet, basename="users")

router.register(r"clients/(?P<client_pk>\d+)/client_details", ClientViewSet, basename="client-details")
router.register(r"users/(?P<user_pk>\d+)/user_details", UserViewSet, basename="user-details")

# router.register(r"users/user_details", UserViewSet, basename="user-details")
# router.register(r'clients/(?P<client_pk>\d+)/', ClientViewSet, basename='clients-details')

# http://127.0.0.1:8000/crm/clients/:client_id/client_details/
# http://127.0.0.1:8000/crm/users/:user_id/user_details/

# http://127.0.0.1:8000/crm/users/user_details/:user_id/
# router.register(r"clients/all_details", ClientViewSet, basename="all-clients-details")
# router.register(r"clients/(?P<client_pk>\d+)/contracts", ContractClientViewSet, basename="clients")
# router.register(r'clients/(?P<client_pk>\d+)/contracts/(?P<contract_pk>\d+)', ContractClientViewSet, basename='data-clients')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crm-auth/', include('rest_framework.urls')),

    # URL pour l'obtention du token JWT lors de la connexion
    path('crm/login/', TokenObtainPairView.as_view(), name='obtain_token'),

    # URL pour le rafraîchissement du token JWT
    path('crm/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),

    # Configurer le chemin pour l'action 'all_clients_details'
    path('crm/clients/all_clients_details/', ClientViewSet.as_view({'get': 'all_clients_details'}), name='all-clients-details'),
    # Configurer le chemin pour l'action 'client_details'
    path('crm/clients/client_details/<int:pk>/', ClientViewSet.as_view({'get': 'client_details'}), name='client-details'),
    
    # Configurer le chemin pour l'action 'all_users_details'
    path('crm/users/all_users_details/', UserViewSet.as_view({'get': 'all_users_details'}), name='all-users-details'),
    # Configurer le chemin pour l'action 'user_details'
    path('crm/users/user_details/<int:pk>/', UserViewSet.as_view({'get': 'user_details'}), name='user-details'),

    # Inclusion des URLs gérées par le routeur simple sous le préfixe "crm/"
    path('crm/', include(router.urls))
]