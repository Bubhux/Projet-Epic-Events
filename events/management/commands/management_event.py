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
        Cette commande permet de créer un nouvel événement en utilisant Click
        pour gérer les arguments en ligne de commande
        et Rich pour améliorer la sortie dans la console.
    """
    help = 'Afficher, créer, modifier, supprimer des événements'

    def add_arguments(self, parser):
        """
            Ajoute les arguments spécifiques à la commande.
            Args:
                parser (argparse.ArgumentParser): Le parseur d'arguments.
        """
        parser.add_argument('--display_events', action='store_true', help='Affiche tous les événements')
        parser.add_argument('--create_event', action='store_true', help='Créer un nouvel événement')
        parser.add_argument('--update_event', type=int, help='Mettre à jour un événement en spécifiant son ID')
        parser.add_argument('--delete_event', type=int, help='Supprimer un événement en spécifiant son ID')

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
                    str(event['event_name']),
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
            event_date_start_str = self.colored_prompt(
                'Date de début de l\'événement (format: YYYY-MM-DD HH:MM)', color=Fore.CYAN
            )

            if self.should_exit():
                return
            event_date_end_str = self.colored_prompt(
                'Date de fin de l\'événement (format: YYYY-MM-DD HH:MM)', color=Fore.CYAN
            )

            if self.should_exit():
                return

            # Le champ support_contact_name est facultatif
            use_support_contact = click.confirm('Voulez-vous spécifier un contact de support ?', default=False)
            support_contact_name = None

            if use_support_contact:
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
                # Récupère l'instance du client à partir de la base de données
                client = Client.objects.get(full_name=client_name)

                # Récupère l'instance du contact de support à partir de la base de données
                support_contact = User.objects.get(full_name=support_contact_name) if support_contact_name else None

                # Convertit les chaînes en objets datetime avec information sur le fuseau horaire
                event_date_start = timezone.make_aware(datetime.strptime(event_date_start_str, '%Y-%m-%d %H:%M'))
                event_date_end = timezone.make_aware(datetime.strptime(event_date_end_str, '%Y-%m-%d %H:%M'))

                # Crée un nouvel événement
                event = Event.objects.create(
                    event_name=event_name,
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
                console.print(
                    f"[bold red]Le client avec le nom '{client_name}' "
                    f"n'existe pas dans la base de données.[/bold red]"
                )

            except User.DoesNotExist:
                console.print(
                    f"[bold red]Le contact de support avec le nom '{support_contact_name}' "
                    f"n'existe pas dans la base de données.[/bold red]"
                )

            except Exception as e:
                console.print(f"[bold red]Erreur lors de la création de l'événement :[/bold red] {e}")

        elif options['update_event']:
            event_id = options['update_event']
            self.update_event(event_id)

        elif options['delete_event']:
            event_id = options['delete_event']
            self.delete_event(event_id)

        else:
            console.print("[bold red]Aucune action spécifiée. Utilisez "
                          "--display_events, --create_event, --update_event, --delete_event.[/bold red]")

    def update_event(self, event_id):
        """
            Fonction pour la mise à jour d'un événement.
        """
        console = Console()
        event_view_set = EventViewSet()

        try:
            # Récupère l'événement à mettre à jour
            event = Event.objects.get(id=event_id)

            # Affiche les détails actuels de l'événement sous forme de tableau avec rich
            console.print(f"[bold magenta]Mise à jour de l'événement ID {event_id}[/bold magenta]")

            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Champs", style="cyan")
            table.add_column("Valeurs actuelles", style="cyan")

            table.add_row("ID", str(event.id))
            table.add_row("Nom de l'événement", str(event.event_name))
            table.add_row("Nom du client", str(event.client))
            table.add_row("Contact du client", str(event.client_contact))
            table.add_row("Date de début de l'événement", str(event.event_date_start))
            table.add_row("Date de fin de l'événement", str(event.event_date_end))
            table.add_row("Contact de support", str(event.support_contact))
            table.add_row("Lieu", str(event.location))
            table.add_row("Nombre d'invités", str(event.attendees))
            table.add_row("Notes", str(event.notes))

            console.print(table)

            # Demande les nouvelles informations
            new_event_name = self.colored_prompt('Nouveau nom de l\'événement', color=Fore.CYAN)
            if self.should_exit():
                return
            new_event_date_start_str = self.colored_prompt(
                'Nouvelle date de début de l\'événement (format: YYYY-MM-DD HH:MM)', color=Fore.CYAN
            )

            if self.should_exit():
                return
            new_event_date_end_str = self.colored_prompt(
                'Nouvelle date de fin de l\'événement (format: YYYY-MM-DD HH:MM)', color=Fore.CYAN
            )

            if self.should_exit():
                return

            # Demande le nom du contact de support seulement si l'utilisateur le souhaite
            use_new_support_contact = click.confirm(
                'Voulez-vous spécifier un nouveau contact de support ?', default=False
            )

            new_support_contact_name = None

            if use_new_support_contact:
                new_support_contact_name = self.colored_prompt('Nouveau nom du contact de support', color=Fore.CYAN)
                if self.should_exit():
                    return

            # Laisse l'utilisateur saisir les informations suivantes même si le contact de support n'est pas renseigné
            new_location = self.colored_prompt('Nouveau lieu de l\'événement', color=Fore.CYAN)
            if self.should_exit():
                return
            new_attendees = self.colored_prompt('Nouveaux nombres d\'invités', color=Fore.CYAN)
            if self.should_exit():
                return
            new_notes = self.colored_prompt('Nouvelles notes', color=Fore.CYAN)

            # Convertit les chaînes en objets datetime avec information sur le fuseau horaire
            new_event_date_start = timezone.make_aware(datetime.strptime(new_event_date_start_str, '%Y-%m-%d %H:%M'))
            new_event_date_end = timezone.make_aware(datetime.strptime(new_event_date_end_str, '%Y-%m-%d %H:%M'))

            # Récupère l'instance du contact de support à partir de la base de données, s'il est spécifié
            new_support_contact = User.objects.get(
                full_name=new_support_contact_name
            ) if new_support_contact_name else None

            # Met à jour l'événement
            event.event_name = new_event_name
            event.event_date_start = new_event_date_start
            event.event_date_end = new_event_date_end
            event.support_contact = new_support_contact
            event.location = new_location
            event.attendees = new_attendees
            event.notes = new_notes

            event.save()

            console.print(f"[bold green]Événement ID {event_id} mis à jour avec succès.[/bold green]")

        except Event.DoesNotExist:
            console.print(f"[bold red]Événement ID {event_id} introuvable.[/bold red]")

        except User.DoesNotExist:
            console.print(
                f"[bold red]Le contact de support avec le nom '{new_support_contact_name}' "
                f"n'existe pas dans la base de données.[/bold red]"
            )

        except Exception as e:
            console.print(f"[bold red]Erreur lors de la mise à jour de l'événement :[/bold red] {e}")

    def delete_event(self, event_id):
        """
            Fonction pour la suppression d'un événement.
        """
        console = Console()
        event_view_set = EventViewSet()

        try:
            # Récupére l'événement à supprimer
            event = Event.objects.get(id=event_id)

            # Affiche les détails actuels de l'événement sous forme de tableau avec rich
            console.print(f"[bold magenta]Suppression de l'événement ID {event_id}[/bold magenta]")

            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Champs", style="cyan")
            table.add_column("Valeurs actuelles", style="cyan")

            table.add_row("ID", str(event.id))
            table.add_row("Nom de l'événement", str(event.event_name))
            table.add_row("Nom du client", str(event.client))
            table.add_row("Contact du client", str(event.client_contact))
            table.add_row("Date de début de l'événement", str(event.event_date_start))
            table.add_row("Date de fin de l'événement", str(event.event_date_end))
            table.add_row("Contact de support", str(event.support_contact))
            table.add_row("Lieu", str(event.location))
            table.add_row("Nombre d'invités", str(event.attendees))
            table.add_row("Notes", str(event.notes))

            console.print(table)

            # Confirme la suppression avec l'utilisateur
            confirm_delete = click.confirm('Voulez-vous vraiment supprimer cet événement ?', default=False)
            if confirm_delete:
                event.delete()
                console.print(f"[bold green]Événement ID {event_id} supprimé avec succès.[/bold green]")
            else:
                console.print("[bold yellow]Suppression annulée.[/bold yellow]")

        except User.DoesNotExist:
            console.print(f"[bold red]Événement ID {event_id} introuvable.[/bold red]")

        except Exception as e:
            console.print(f"[bold red]Erreur lors de la suppression de l'événement :[/bold red] {e}")

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
