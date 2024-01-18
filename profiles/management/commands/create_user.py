import click
from django.core.management.base import BaseCommand
from rich.console import Console
from profiles.models import User
from colorama import Fore, Style


class Command(BaseCommand):
    """
        Cette commande permet de créer un nouvel utilisateur en utilisant Click pour gérer les arguments en ligne de commande
        et Rich pour améliorer la sortie dans la console.
    """
    help = 'Créer un nouvel utilisateur'

    def handle(self, *args, **options):
        """
            Gère l'exécution de la commande, récupère les informations nécessaires du nouvelle utilisateur
            et créer un utilisateur en utilisant ces informations.
        """
        console = Console()

        # Utilise Rich pour améliorer la sortie en ligne de commande
        console.print("[bold green]Création d'un nouvel utilisateur[/bold green]")

        # Utilise Click pour gérer les arguments de ligne de commande
        email = self.colored_prompt('Email de l\'utilisateur', color=Fore.CYAN)
        password = self.colored_prompt('Mot de passe', hide_input=True, color=Fore.CYAN)
        role = self.colored_prompt('Rôle de l\'utilisateur (Management/Sales/Support)', color=Fore.CYAN)

        try:
            # Créer un nouvel utilisateur
            user = User.objects.create_user(
                email=email,
                password=password,
                role=role,
                full_name=self.colored_prompt('Nom complet', color=Fore.CYAN),
                phone_number=self.colored_prompt('Numéro de téléphone', color=Fore.CYAN),
                is_staff=click.confirm('Est-ce un membre du personnel?', color=Fore.CYAN)
            )
            console.print(f"[bold green]Utilisateur créé avec succès:[/bold green] {user}")

        except Exception as e:
            console.print(f"[bold red]Erreur lors de la création de l'utilisateur:[/bold red] {e}")

    def colored_prompt(self, text, color=Fore.CYAN, **kwargs):
        """
            Affiche un prompt coloré et récupère la saisie de l'utilisateur.
            Parameters:
            - text (str): Le texte du prompt.
            - color (str): La couleur du texte.
            Returns:
            str: La saisie de l'utilisateur.
        """
        return click.prompt(f'{color}{text}{Style.RESET_ALL} ', **kwargs)
