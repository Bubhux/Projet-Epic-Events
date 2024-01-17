from django.db import models
from django.utils import timezone

from profiles.models import User, Client


class Contract(models.Model):
    """
        Modèle représentant un contrat entre un vendeur et un client.

        Attributs:
        - sales_contact: Vendeur associé au contrat.
        - client: Client associé au contrat.
        - creation_date: Date de création du contrat (auto-générée lors de la création).
        - update_date: Date de la dernière mise à jour du contrat (auto-générée lors de chaque sauvegarde).
        - status_contract: Statut du contrat (signé ou non signé).
        - total_amount: Montant total du contrat.
        - remaining_amount: Montant restant à payer sur le contrat.
    """
    sales_contact = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Sales Contact")
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='contracts', verbose_name="Client")

    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    status_contract = models.BooleanField(default=False, verbose_name="Contract signed")
    total_amount = models.FloatField(default=0.0)
    remaining_amount = models.FloatField(default=0.0)

    def __str__(self):
        """Renvoie une représentation lisible de l'instance de Contrat."""
        client_name = f"{self.client.full_name}" if self.client else "No Client"
        status_contract_str = "Contract signed" if self.status_contract else "Contract not signed"

        return f"Contrat ID : {self.id} {status_contract_str} - {client_name}"

    def print_details(self):
        print()
        print(f"ID du contrat : {self.id}")

        if self.client:
            print(f"Nom du client : {self.client.full_name}")
            print(f"E-mail du client : {self.client.email}")
            print(f"Compagnie du client : {self.client.company_name}")
        else:
            print("Aucun client associé.")
        print()

    def save(self, *args, **kwargs):
        # Si le contrat est nouvellement créé et le sales_contact n'est pas défini,
        # attribuez-le automatiquement en utilisant le sales_contact du client associé
        if not self.id and not self.sales_contact and self.client and self.client.sales_contact:
            self.sales_contact = self.client.sales_contact

        # Mettre à jour la date de mise à jour avant de sauvegarder
        self.update_date = timezone.now()
        super(Contract, self).save(*args, **kwargs)

        # Imprime les détails après la sauvegarde
        self.print_details()
