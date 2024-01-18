import click
from django.core.management.base import BaseCommand
from rich.console import Console
from colorama import Fore, Style
from rich.table import Table

from profiles.models import Client
from profiles.views import ClientViewSet


class Command(BaseCommand):
    """
        Cette commande permet de créer un nouveau client en utilisant Click pour gérer les arguments en ligne de commande
        et Rich pour améliorer la sortie dans la console.
    """
    help = 'Afficher, créer, modifier, supprimer des clients.'

    def add_arguments(self, parser):
        """
            Ajoute les arguments spécifiques à la commande.
            Args:
                parser (argparse.ArgumentParser): Le parseur d'arguments.
        """
        parser.add_argument('--display_clients', action='store_true', help='Affiche tous les clients')
        parser.add_argument('--create_client', action='store_true', help='Créer un nouveau client')
        parser.add_argument('--update_client', type=int, help='Mettre à jour un client en spécifiant son ID')
        parser.add_argument('--delete_client', type=int, help='Supprimer un client en spécifiant son ID')

    def handle(self, *args, **options):
        """
            Gère l'exécution de la commande, récupère les informations nécessaires du nouveau client
            et créer un client en utilisant ces informations.
        """
        console = Console()
        client_view_set = ClientViewSet()

        if options['display_clients']:
            # Appele la méthode all_clients_details pour lire les informations des clients
            response = client_view_set.all_clients_details(request=None)

            # Utilise la propriété data de l'objet Response pour accéder au contenu JSON
            data = response.data

            # Affiche les données sous forme de tableau avec rich
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("ID", style="cyan")
            table.add_column("Nom complet", style="cyan")
            table.add_column("Email", style="cyan")
            table.add_column("Entreprise", style="cyan")
            table.add_column("Contact commercial", style="cyan")

            for client in data:
                table.add_row(str(client['id']), client['full_name'], client['email'], client['company_name'], client['sales_contact'])

            console.print(table)

        elif options['create_client']:
            # Utilise Rich pour améliorer la sortie en ligne de commande
            console.print("[bold magenta]Création d'un nouveau client[/bold magenta]")

            # Utilise Click pour gérer les arguments de ligne de commande
            email = self.colored_prompt('Email du client', color=Fore.CYAN)
            if self.should_exit():
                return
            full_name = self.colored_prompt('Nom complet du client', color=Fore.CYAN)
            if self.should_exit():
                return
            phone_number = self.colored_prompt('Numéro de téléphone du client', color=Fore.CYAN)
            if self.should_exit():
                return
            company_name = self.colored_prompt('Nom de l\'entreprise du client', color=Fore.CYAN)

            try:
                # Créer un nouveau client
                client = Client.objects.create(
                    email=email,
                    full_name=full_name,
                    phone_number=phone_number,
                    company_name=company_name
                )
                console.print(f"[bold green]Client créé avec succès :[/bold green] {client}")

            except Exception as e:
                console.print(f"[bold red]Erreur lors de la création du client :[/bold red] {e}")

        elif options['update_client']:
            client_id = options['update_client']
            self.update_client(client_id)

        elif options['delete_client']:
            client_id = options['delete_client']
            self.delete_client(client_id)

        else:
            console.print("[bold red]Aucune action spécifiée. Utilisez "
                          "--display_clients, --create_client, --update_client, --delete_client.[/bold red]"
            )

    def update_client(self, client_id):
        """
            Fonction pour la mise à jour d'un client.
        """
        console = Console()
        client_view_set = ClientViewSet()

        try:
            # Récupère le client à mettre à jour
            client = Client.objects.get(id=client_id)

            # Affiche les détails actuels du client sous forme de tableau avec rich
            console.print(f"[bold magenta]Mise à jour du client ID {client_id}[/bold magenta]")

            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Champs", style="cyan")
            table.add_column("Valeurs actuelles", style="cyan")

            table.add_row("ID", str(client.id))
            table.add_row("Email", client.email)
            table.add_row("Nom complet", client.full_name)
            table.add_row("Numéro de téléphone", client.phone_number)
            table.add_row("Nom de l\'entreprise", client.company_name)

            console.print(table)

            # Demande les nouvelles informations
            new_email = self.colored_prompt('Nouvel email du client', color=Fore.CYAN)
            if self.should_exit():
                return
            new_full_name = self.colored_prompt('Nouveau nom complet du client', color=Fore.CYAN)
            if self.should_exit():
                return
            new_phone_number = self.colored_prompt('Nouveau numéro de téléphone du client', color=Fore.CYAN)
            if self.should_exit():
                return
            new_company_name = self.colored_prompt('Nouveau nom de l\'entreprise du client', color=Fore.CYAN)

            # Met à jour le client
            client.email = new_email
            client.full_name = new_full_name
            client.phone_number = new_phone_number
            new_company_name = new_company_name

            client.save()

            console.print(f"[bold green]Client ID {client_id} mis à jour avec succès.[/bold green]")

        except User.DoesNotExist:
            console.print(f"[bold red]Client ID {client_id} introuvable.[/bold red]")

        except Exception as e:
            console.print(f"[bold red]Erreur lors de la mise à jour du client :[/bold red] {e}")

    def delete_client(self, client_id):
        """
            Fonction pour la suppression d'un client.
        """
        console = Console()
        client_view_set = ClientViewSet()

        try:
            # Récupére le client à supprimer
            client = Client.objects.get(id=client_id)

            # Affiche les détails actuels du client sous forme de tableau avec rich
            console.print(f"[bold magenta]Suppression du client ID {client_id}[/bold magenta]")

            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Champs", style="cyan")
            table.add_column("Valeurs actuelles", style="cyan")

            table.add_row("ID", str(client.id))
            table.add_row("Email", client.email)
            table.add_row("Nom complet", client.full_name)
            table.add_row("Numéro de téléphone", client.phone_number)
            table.add_row("Nom de l\'entreprise", client.company_name)

            console.print(table)

            # Confirme la suppression avec l'utilisateur
            confirm_delete = click.confirm('Voulez-vous vraiment supprimer ce client ?', default=False)
            if confirm_delete:
                client.delete()
                console.print(f"[bold green]Client ID {client_id} supprimé avec succès.[/bold green]")
            else:
                console.print("[bold yellow]Suppression annulée.[/bold yellow]")

        except User.DoesNotExist:
            console.print(f"[bold red]Client ID {client_id} introuvable.[/bold red]")

        except Exception as e:
            console.print(f"[bold red]Erreur lors de la suppression du client :[/bold red] {e}")

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

    def should_exit(self):
        """
            Demande à l'utilisateur s'il souhaite quitter et retourne True si oui, False sinon.
        """
        exit_choice = click.confirm('Voulez-vous quitter le gestionnaire de commandes ?', default=False)
        return exit_choice
