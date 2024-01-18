from django.db import models
from contracts.models import Contract
from profiles.models import User, Client


class Event(models.Model):
    """
        Modèle représentant un événement lié à un contrat et à un client.

        Attributes:
            event (str): Le nom de l'événement.
            contract (Contract): Le contrat associé à l'événement.
            client (Client): Le client associé à l'événement.
            client_name (str): Le nom complet du client.
            client_contact (str): Les coordonnées du client (e-mail et numéro de téléphone).
            event_date_start (datetime): La date de début de l'événement.
            event_date_end (datetime): La date de fin de l'événement.
            support_contact (str): Le contact de support associé à l'événement.
            location (str): L'emplacement de l'événement.
            attendees (int): Le nombre d'invités prévu.
            notes (str): Des notes ou des détails supplémentaires sur l'événement.

        Methods:
            __str__: Renvoie une représentation sous forme de chaîne de l'événement.
            print_details: Affiche les détails de l'événement dans la console.
            save: Surcharge la méthode save pour mettre à jour client_name et client_contact avant la sauvegarde.
    """
    event = models.CharField(max_length=255, blank=True)
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True, blank=True, related_name='contract_events', verbose_name="Contract")
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='client_events', verbose_name="Client")
    client_name = models.CharField(max_length=255, blank=True)
    client_contact = models.CharField(max_length=255, blank=True)
    event_date_start = models.DateTimeField(null=True, blank=True)
    event_date_end = models.DateTimeField(null=True, blank=True)
    support_contact = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='support_contact_events', verbose_name="Support Contact", limit_choices_to={'role': User.ROLE_SUPPORT})
    location = models.TextField(blank=True)
    attendees = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        """Renvoie une représentation lisible de l'instance de Event."""
        return f"Evénement ID: {self.id} {self.event} - {self.client_name}"

    def print_details(self):
        """
            Affiche les détails de l'événement dans la console.
        """
        print()
        print(f"ID de l'événement : {self.id}")

        attributes = [
            ("Nom de l'événement", self.event if self.event else None),
            ("Nom du client", self.client.full_name if self.client else None),
            ("E-mail du client", self.client.email if self.client else None),
            ("Compagnie du client", self.client.company_name if self.client else None),
            ("Contact du client", self.client_contact if self.client else None),
            ("Date de début de l'événement", self.event_date_start if self.event_date_start else None),
            ("Date de fin de l'événement", self.event_date_end if self.event_date_end else None),
            ("Contact de support", self.support_contact if self.support_contact else None),
            ("Lieu", self.location if self.location else None),
            ("Nombre d'invités", self.attendees if self.attendees else None),
            ("Notes", self.notes if self.notes else None),
        ]

        for attribute, value in attributes:
            print(f"{attribute} : {value}" if value is not None else f"Aucun {attribute} défini.")
        print()

    def save(self, *args, **kwargs):
        """
            Surcharge la méthode save pour mettre à jour client_name et client_contact avant la sauvegarde,
            puis imprime les détails de l'événement.
        """
        # Met à jour client_name et client_contact avant la sauvegarde si le client est défini
        if self.client:
            self.client_name = self.client.full_name
            # Concatène l'e-mail et le numéro de téléphone pour le champ client_contact
            self.client_contact = f"{self.client.email} {self.client.phone_number}"

        super(Event, self).save(*args, **kwargs)

        # Imprime les détails après la sauvegarde
        self.print_details()
