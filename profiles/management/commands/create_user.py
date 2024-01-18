import click
from django.core.management.base import BaseCommand
from rich.console import Console
from colorama import Fore, Style
from rich.table import Table

from profiles.models import User
from profiles.views import UserViewSet


class Command(BaseCommand):
    """
        Cette commande permet d'afficher les utilisateurs de créer un nouvel utilisateur ou un administrateur
        en utilisant Click pour gérer les arguments en ligne de commande
        et Rich pour améliorer la sortie dans la console.
    """
    help = 'Afficher ou créer des utilisateurs (lecture/création)'

    def add_arguments(self, parser):
        """
            Ajoute les arguments spécifiques à la commande.
            Args:
                parser (argparse.ArgumentParser): Le parseur d'arguments.
        """
        parser.add_argument('--display_users', action='store_true', help='Affiche tous les utilisateurs')
        parser.add_argument('--create_user', action='store_true', help='Créer un nouvel utilisateur')
        parser.add_argument('--create_superuser', action='store_true', help='Créer un nouvel administrateur')

    def handle(self, *args, **options):
        """
            Gère l'exécution de la commande en fonction des options fournies.
            Args:
                args: Les arguments non nommés.
                options (dict): Les options de la commande.
            Raises:
                CommandError: En cas d'erreur lors de l'exécution de la commande.
        """
        console = Console()
        user_view_set = UserViewSet()

        if options['display_users']:
            # Appele la méthode all_users_details pour lire les informations des utilisateurs
            response = user_view_set.all_users_details(request=None)

            # Utilise la propriété data de l'objet Response pour accéder au contenu JSON
            data = response.data

            # Affiche les données sous forme de tableau avec rich
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("ID", style="cyan")
            table.add_column("Nom complet", style="cyan")
            table.add_column("Email", style="cyan")
            table.add_column("Rôle", style="cyan")

            for user in data:
                table.add_row(str(user['id']), user['full_name'], user['email'], user['role'])

            console.print(table)

        elif options['create_user']:
            # Utilise Rich pour améliorer la sortie en ligne de commande
            console.print("[bold magenta]Création d'un nouvel utilisateur[/bold magenta]")

            # Utilise Click pour gérer les arguments de ligne de commande
            email = self.colored_prompt('Email de l\'utilisateur', color=Fore.CYAN)
            if self.should_exit():
                return

            password = self.colored_prompt('Mot de passe', hide_input=True, color=Fore.CYAN)
            if self.should_exit():
                return

            role = self.colored_prompt('Rôle de l\'utilisateur (Management/Sales/Support)', color=Fore.CYAN)
            if self.should_exit():
                return

            try:
                # Créer un nouvel utilisateur
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    role=role,
                    full_name=self.colored_prompt('Nom complet', color=Fore.CYAN),
                    phone_number=self.colored_prompt('Numéro de téléphone', color=Fore.CYAN),
                    is_staff=click.confirm('Est-ce un membre du personnel ?')
                )
                console.print(f"[bold green]Utilisateur créé avec succès :[/bold green] {user}")

            except Exception as e:
                console.print(f"[bold red]Erreur lors de la création de l'utilisateur :[/bold red] {e}")

        elif options['create_superuser']:
            # Utilise Rich pour améliorer la sortie en ligne de commande
            console.print("[bold magenta]Création d'un nouvel administrateur[/bold magenta]")

            # Utilise Click pour gérer les arguments de ligne de commande
            email = self.colored_prompt('Email de l\'utilisateur', color=Fore.CYAN)
            if self.should_exit():
                return

            password = self.colored_prompt('Mot de passe', hide_input=True, color=Fore.CYAN)
            if self.should_exit():
                return

            role = self.colored_prompt('Rôle de l\'utilisateur (Management/Sales/Support)', color=Fore.CYAN)
            if self.should_exit():
                return

            full_name = self.colored_prompt('Nom complet', color=Fore.CYAN)
            if self.should_exit():
                return

            phone_number = self.colored_prompt('Numéro de téléphone', color=Fore.CYAN)

            try:
                # Créer un nouvel administrateur
                superuser = User.objects.create_superuser(
                    email=email,
                    password=password,
                    role=role,
                    full_name=full_name,
                    phone_number=phone_number,
                    is_staff=click.confirm('Est-ce un membre du personnel ?')
                )
                console.print(f"[bold green]Administrateur créé avec succès[/bold green]")

            except Exception as e:
                console.print(f"[bold red]Erreur lors de la création de l'administrateur :[/bold red] {e}")

        else:
            console.print("[bold red]Aucune action spécifiée. Utilisez --display_users, --create_user, create_superuser.[/bold red]")

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

    def should_exit(self):
        """
            Demande à l'utilisateur s'il souhaite quitter et retourne True si oui, False sinon.
        """
        exit_choice = click.confirm('Voulez-vous quitter le gestionnaire de commandes ?', default=False)
        return exit_choice
