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
    help = 'Afficher, créer, modifier, supprimer des utilisateurs.'

    def add_arguments(self, parser):
        """
            Ajoute les arguments spécifiques à la commande.
            Args:
                parser (argparse.ArgumentParser): Le parseur d'arguments.
        """
        parser.add_argument('--display_users', action='store_true', help='Affiche tous les utilisateurs')
        parser.add_argument('--create_user', action='store_true', help='Créer un nouvel utilisateur')
        parser.add_argument('--create_superuser', action='store_true', help='Créer un nouvel administrateur')
        parser.add_argument('--update_user', type=int, help='Mettre à jour un utilisateur en spécifiant son ID')
        parser.add_argument('--delete_user', type=int, help='Supprimer un utilisateur en spécifiant son ID')

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
            role = self.colored_prompt(
                'Rôle de l\'utilisateur (Management team/Sales team/Support team)',
                color=Fore.CYAN
            )

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
            role = self.colored_prompt(
                'Rôle de l\'utilisateur (Management team/Sales team/Support team)',
                color=Fore.CYAN
            )

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
                console.print(f"[bold green]Administrateur créé avec succès[/bold green] {superuser}")

            except Exception as e:
                console.print(f"[bold red]Erreur lors de la création de l'administrateur :[/bold red] {e}")

        elif options['update_user']:
            user_id = options['update_user']
            self.update_user(user_id)

        elif options['delete_user']:
            user_id = options['delete_user']
            self.delete_user(user_id)

        else:
            console.print(
                "[bold red]Aucune action spécifiée. Utilisez "
                "--display_users, --create_user, --create_superuser, --update_user, --delete_user.[/bold red]"
            )

    def update_user(self, user_id):
        """
            Fonction pour la mise à jour d'un utilisateur.
        """
        console = Console()
        user_view_set = UserViewSet()

        try:
            # Récupère l'utilisateur à mettre à jour
            user = User.objects.get(id=user_id)

            # Affiche les détails actuels de l'utilisateur sous forme de tableau avec rich
            console.print(f"[bold magenta]Mise à jour de l'utilisateur ID {user_id}[/bold magenta]")

            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Champs", style="cyan")
            table.add_column("Valeurs actuelles", style="cyan")

            table.add_row("ID", str(user.id))
            table.add_row("Email", user.email)
            table.add_row("Rôle", user.role)
            table.add_row("Nom complet", user.full_name)
            table.add_row("Numéro de téléphone", user.phone_number)
            table.add_row("Statut membre de l'équipe", str(user.is_staff))

            console.print(table)

            # Demande les nouvelles informations
            new_email = self.colored_prompt('Nouvel email de l\'utilisateur', color=Fore.CYAN)
            if self.should_exit():
                return
            new_password = self.colored_prompt(
                'Nouveau mot de passe de l\'utilisateur', hide_input=True, color=Fore.CYAN
            )

            if self.should_exit():
                return
            new_role = self.colored_prompt(
                'Nouveau rôle de l\'utilisateur (Management team/Sales team/Support team)', color=Fore.CYAN
            )

            if self.should_exit():
                return
            new_full_name = self.colored_prompt('Nouveau nom complet de l\'utilisateur', color=Fore.CYAN)
            if self.should_exit():
                return
            new_phone_number = self.colored_prompt('Nouveau numéro de téléphone de l\'utilisateur', color=Fore.CYAN)
            if self.should_exit():
                return
            new_is_staff = click.confirm('Est-ce un membre du personnel ?')

            # Met à jour l'utilisateur
            user.email = new_email
            user.set_password(new_password)
            user.role = new_role
            user.full_name = new_full_name
            user.phone_number = new_phone_number
            user.is_staff = new_is_staff

            user.save()

            console.print(f"[bold green]Utilisateur ID {user_id} mis à jour avec succès.[/bold green]")

        except User.DoesNotExist:
            console.print(f"[bold red]Utilisateur ID {user_id} introuvable.[/bold red]")

        except Exception as e:
            console.print(f"[bold red]Erreur lors de la mise à jour de l'utilisateur :[/bold red] {e}")

    def delete_user(self, user_id):
        """
            Fonction pour la suppression d'un utilisateur.
        """
        console = Console()
        user_view_set = UserViewSet()

        try:
            # Récupére l'utilisateur à supprimer
            user = User.objects.get(id=user_id)

            # Affiche les détails actuels de l'utilisateur sous forme de tableau avec rich
            console.print(f"[bold magenta]Suppression de l'utilisateur ID {user_id}[/bold magenta]")

            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Champs", style="cyan")
            table.add_column("Valeurs actuelles", style="cyan")

            table.add_row("ID", str(user.id))
            table.add_row("Email", user.email)
            table.add_row("Rôle", user.role)
            table.add_row("Nom complet", user.full_name)
            table.add_row("Numéro de téléphone", user.phone_number)
            table.add_row("Statut membre de l'équipe", str(user.is_staff))

            console.print(table)

            # Confirme la suppression avec l'utilisateur
            confirm_delete = click.confirm('Voulez-vous vraiment supprimer cet utilisateur ?', default=False)
            if confirm_delete:
                user.delete()
                console.print(f"[bold green]Utilisateur ID {user_id} supprimé avec succès.[/bold green]")
            else:
                console.print("[bold yellow]Suppression annulée.[/bold yellow]")

        except User.DoesNotExist:
            console.print(f"[bold red]Utilisateur ID {user_id} introuvable.[/bold red]")

        except Exception as e:
            console.print(f"[bold red]Erreur lors de la suppression de l'utilisateur :[/bold red] {e}")

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
