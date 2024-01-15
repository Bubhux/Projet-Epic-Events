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

from profiles.views import SignupView

# Création du routeur simple
router = SimpleRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crm-auth/', include('rest_framework.urls')),

    path('crm/signup/', SignupView.as_view(), name='signup'),
    path('crm/login/', TokenObtainPairView.as_view(), name='obtain_token'),
    path('crm/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),

    # Inclusion des URLs gérées par le routeur simple sous le préfixe "crm/"
    path('crm/', include(router.urls))
]