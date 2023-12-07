"""
Créer un modèle de fichier .env pour Epic Events
avec une clé secrète générée aléatoirement et des variables d'environnement préconfigurées.

Ce script génère un fichier .env qui peut être utilisé pour configurer
l'environnement de l'application oc_lettings_site
Il génère une clé secrète aléatoire pour la configuration de Django
et inclut également des noms de variables d'environnement
préconfigurés tels que :

    - 'DJANGO_SECRET_KEY'
    - 'DB_NAME'
    - 'DB_USER'
    - 'DB_PASSWORD'
    - 'DB_HOST'
    - 'DB_PORT'
    - 'SENTRY_DSN'

Le fichier .env généré doit être configuré avec des valeurs appropriées
pour chaque variable d'environnement avant utilisation.

Exemple d'utilisation :

    1. Exécutez ce script pour générer un fichier .env.
    2. Configurez les valeurs des variables d'environnement
       dans le fichier .env généré.
    3. Utilisez le fichier .env pour configurer
       l'environnement de votre application Epic Events.

.. note::
    Remarque :
    Le fichier .env généré ne doit pas être partagé publiquement
    car il contient des informations sensibles.

"""

from django.core.management.utils import get_random_secret_key

# Liste des noms de variables d'environnement
env_variable_names = [
    'DJANGO_SECRET_KEY',
    'DB_NAME',
    'DB_USER',
    'DB_PASSWORD',
    'DB_HOST',
    'DB_PORT',
    'SENTRY_DSN',
]

# Générer la clé secrète aléatoire
secret_key = get_random_secret_key()

# Ouvrir le fichier .env en mode écriture
with open(".env", "w") as f:
    # Écrire les noms des variables d'environnement avec leurs valeurs
    f.write(f"DJANGO_SECRET_KEY={secret_key}\n")
    for env_var in env_variable_names[1:]:
        f.write(f"{env_var}=\n")

# Afficher un message indiquant que le modèle de fichier .env a été créé
print("\n.env file created!")
