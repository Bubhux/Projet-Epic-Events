import click
from django.core.management.base import BaseCommand
from rich.console import Console
from colorama import Fore, Style
from rich.table import Table
from django.utils import timezone
from datetime import datetime

from contracts.models import Contract
from profiles.models import User, Client
from events.models import Event
from events.views import EventViewSet


class Command(BaseCommand):
    """
        Cette commande permet de créer un nouvel événement en utilisant Click pour gérer les arguments en ligne de commande
        et Rich pour améliorer la sortie dans la console.
    """
    help = 'Afficher ou créer de nouveaux événements'

    def add_arguments(self, parser):
        """
            Ajoute les arguments spécifiques à la commande.
            Args:
                parser (argparse.ArgumentParser): Le parseur d'arguments.
        """
        parser.add_argument('--display_events', action='store_true', help='Affiche tous les événements')
        parser.add_argument('--create_event', action='store_true', help='Créer un nouvel événement')

    def handle(self, *args, **options):
        """
            Gère l'exécution de la commande, récupère les informations nécessaires du nouvel événement
            et créer un événement en utilisant ces informations.
        """
        console = Console()
        event_view_set = EventViewSet()

        if options['display_events']:
            # Appele la méthode all_events_details pour lire les informations des événements
            response = event_view_set.all_events_details(request=None)

            # Utilise la propriété data de l'objet Response pour accéder au contenu JSON
            data = response.data

            # Affiche les données sous forme de tableau avec rich
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("ID", style="cyan")
            table.add_column("Nom de l'événement", style="cyan")
            table.add_column("Nom du client", style="cyan")
            table.add_column("Contact du client", style="cyan")
            table.add_column("Date de début de l'événement", style="cyan")
            table.add_column("Date de fin de l'événement", style="cyan")
            table.add_column("Contact de support", style="cyan")
            table.add_column("Lieu", style="cyan")
            table.add_column("Nombre d'invités", style="cyan")
            table.add_column("Notes", style="cyan")

            for event in data:
                # Assure que 'client' est présent dans le dictionnaire de l'événement
                if 'client' in event and isinstance(event['client'], dict):
                    # Met à jour client_name et client_contact avant l'affichage
                    event['client_name'] = event['client']['full_name']
                    event['client_contact'] = f"{event['client']['email']} {event['client']['phone_number']}"

                table.add_row(
                    str(event['id']),
                    str(event['event']),
                    str(event['client']),
                    str(event.get('client_contact', '')),
                    str(event.get('event_date_start', '')),
                    str(event.get('event_date_end', '')),
                    str(event.get('support_contact', '')),
                    str(event.get('location', '')),
                    str(event.get('attendees', '')),
                    str(event.get('notes', ''))
                )

            console.print(table)

        elif options['create_event']:
            # Utilise Rich pour améliorer la sortie en ligne de commande
            console.print("[bold magenta]Création d'un nouvel événement[/bold magenta]")

            # Utilise Click pour gérer les arguments de ligne de commande
            event_name = self.colored_prompt('Nom de l\'événement', color=Fore.CYAN)
            if self.should_exit():
                return

            client_name = self.colored_prompt('Nom complet du client', color=Fore.CYAN)
            if self.should_exit():
                return

            event_date_start_str = self.colored_prompt('Date de début de l\'événement (format: YYYY-MM-DD HH:MM)', color=Fore.CYAN)
            if self.should_exit():
                return

            event_date_end_str = self.colored_prompt('Date de fin de l\'événement (format: YYYY-MM-DD HH:MM)', color=Fore.CYAN)
            if self.should_exit():
                return

            support_contact_name = self.colored_prompt('Nom complet du contact de support', color=Fore.CYAN)
            if self.should_exit():
                return

            location = self.colored_prompt('Lieu de l\'événement', color=Fore.CYAN)
            if self.should_exit():
                return

            attendees = self.colored_prompt('Nombre d\'invités', color=Fore.CYAN)
            if self.should_exit():
                return

            notes = self.colored_prompt('Notes sur l\'événement', color=Fore.CYAN)

            try:
                # Récupére l'instance du client à partir de la base de données
                client = Client.objects.get(full_name=client_name)

                # Récupére l'instance du contact de support à partir de la base de données
                support_contact = User.objects.get(full_name=support_contact_name)

                # Convertir les chaînes en objets datetime avec information sur le fuseau horaire
                event_date_start = timezone.make_aware(datetime.strptime(event_date_start_str, '%Y-%m-%d %H:%M'))
                event_date_end = timezone.make_aware(datetime.strptime(event_date_end_str, '%Y-%m-%d %H:%M'))

                # Créer un nouvel événement
                event = Event.objects.create(
                    event=event_name,
                    client=client,
                    event_date_start=event_date_start,
                    event_date_end=event_date_end,
                    support_contact=support_contact,
                    location=location,
                    attendees=attendees,
                    notes=notes
                )
                console.print(f"[bold green]Événement créé avec succès :[/bold green] {event_name}")

            except Client.DoesNotExist:
                console.print(f"[bold red]Le client avec le nom '{client_name}' n'existe pas dans la base de données.[/bold red]")

            except User.DoesNotExist:
                console.print(f"[bold red]Le contact de support avec le nom '{support_contact_name}' n'existe pas dans la base de données.[/bold red]")

            except Exception as e:
                console.print(f"[bold red]Erreur lors de la création de l'événement :[/bold red] {e}")

        else:
            console.print("[bold red]Aucune action spécifiée. Utilisez --display_events, --create_event.[/bold red]")

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
