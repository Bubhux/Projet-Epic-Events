import click
from django.core.management.base import BaseCommand
from rich.console import Console
from profiles.models import User, Client
from colorama import Fore, Style


class Command(BaseCommand):
    """
        Cette commande permet de créer un nouveau client en utilisant Click pour gérer les arguments en ligne de commande
        et Rich pour améliorer la sortie dans la console.
    """
    help = 'Créer un nouveau client'

    def handle(self, *args, **options):
        """
            Gère l'exécution de la commande, récupère les informations nécessaires du nouveau client
            et créer un client en utilisant ces informations.
        """
        console = Console()

        # Utilise Rich pour améliorer la sortie en ligne de commande
        console.print("[bold green]Création d'un nouveau client[/bold green]")

        # Utilise Click pour gérer les arguments de ligne de commande
        email = self.colored_prompt('Email du client')
        full_name = self.colored_prompt('Nom complet du client')
        phone_number = self.colored_prompt('Numéro de téléphone du client')
        company_name = self.colored_prompt('Nom de l\'entreprise du client')

        try:
            # Créer un nouveau client
            client = Client.objects.create(
                email=email,
                full_name=full_name,
                phone_number=phone_number,
                company_name=company_name
            )
            console.print(f"[bold green]Client créé avec succès:[/bold green] {client}")

        except Exception as e:
            console.print(f"[bold red]Erreur lors de la création du client:[/bold red] {e}")

    def colored_prompt(self, text, color=Fore.CYAN):
        """
            Affiche un prompt coloré et récupère la saisie de l'utilisateur.
            Parameters:
            - text (str): Le texte du prompt.
            - color (str): La couleur du texte.
            Returns:
            str: La saisie de l'utilisateur.
        """
        return click.prompt(f'{color}{text}{Style.RESET_ALL} ')
