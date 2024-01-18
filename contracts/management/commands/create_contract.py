import click
from django.core.management.base import BaseCommand
from rich.console import Console
from colorama import Fore, Style
from rich.table import Table

from profiles.models import Client
from contracts.models import Contract
from contracts.views import ContractViewSet


class Command(BaseCommand):
    """
        Cette commande permet de créer un nouveau contrat en utilisant Click pour gérer les arguments en ligne de commande
        et Rich pour améliorer la sortie dans la console.
    """
    help = 'Afficher ou créer de nouveaux contrats'

    def add_arguments(self, parser):
        """
            Ajoute les arguments spécifiques à la commande.
            Args:
                parser (argparse.ArgumentParser): Le parseur d'arguments.
        """
        parser.add_argument('--display_contracts', action='store_true', help='Affiche tous les contrats')
        parser.add_argument('--create_contract', action='store_true', help='Créer un nouveau contrat')

    def handle(self, *args, **options):
        """
            Gère l'exécution de la commande, récupère les informations nécessaires du nouveau contrat
            et créer un client en utilisant ces informations.
        """
        console = Console()
        contract_view_set = ContractViewSet()

        if options['display_contracts']:
            # Appele la méthode all_clients_details pour lire les informations des clients
            response = contract_view_set.all_contracts_details(request=None)

            # Utilise la propriété data de l'objet Response pour accéder au contenu JSON
            data = response.data

            # Affiche les données sous forme de tableau avec rich
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("ID", style="cyan")
            table.add_column("Client", style="cyan")
            table.add_column("Contact commercial", style="cyan")
            table.add_column("Date de création", style="cyan")
            table.add_column("Status du contrat", style="cyan")
            table.add_column("Montant total du contrat", style="cyan")
            table.add_column("Montant restant à payer sur le contrat", style="cyan")
            
            for contract in data:
                # Convertit la valeur booléenne en une chaîne lisible
                status_contract_str = "Signé" if contract.get('status_contract', False) else "Non signé"

                # Convertit les valeurs de type float en chaînes de caractères
                total_amount_str = str(contract.get('total_amount', ''))
                remaining_amount_str = str(contract.get('remaining_amount', ''))

                table.add_row(
                    str(contract.get('id', '')),
                    contract.get('client', ''),
                    contract.get('sales_contact', ''),
                    contract.get('creation_date', ''),
                    status_contract_str,
                    total_amount_str,
                    remaining_amount_str
                )

            console.print(table)

        elif options['create_contract']:
            # Utilise Rich pour améliorer la sortie en ligne de commande
            console.print("[bold magenta]Création d'un nouveau contrat[/bold magenta]")

            # Utilise Click pour gérer les arguments de ligne de commande
            client_name = self.colored_prompt('Nom complet du client', color=Fore.CYAN)
            if self.should_exit():
                return

            total_amount = self.colored_prompt('Montant total du contrat', color=Fore.CYAN)
            if self.should_exit():
                return

            remaining_amount = self.colored_prompt('Montant restant à payer sur le contrat', color=Fore.CYAN)

            try:
                # Récupérer l'instance du client à partir de la base de données
                client = Client.objects.get(full_name=client_name)

                # Créer un nouveau contrat
                contract = Contract.objects.create(
                    client=client,
                    status_contract=click.confirm('Est-ce que le contrat est signé ?'),
                    total_amount=total_amount,
                    remaining_amount=remaining_amount
                )
                console.print(f"[bold green]Contrat créé avec succès pour le client :[/bold green] {client_name}")

            except Client.DoesNotExist:
                console.print(f"[bold red]Le client avec le nom '{client_name}' n'existe pas dans la base de données.[/bold red]")

            except Exception as e:
                console.print(f"[bold red]Erreur lors de la création du contrat :[/bold red] {e}")

        else:
            console.print("[bold red]Aucune action spécifiée. Utilisez --display_contracts, --create_contract.[/bold red]")

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
