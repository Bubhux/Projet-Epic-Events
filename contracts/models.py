
from django.db import models
from django.utils import timezone
from profiles.models import User, Client


class Contract(models.Model):

    sales_contact = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Sales Contact")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contracts', verbose_name="Client")

    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    status_contract = models.BooleanField(default=False, verbose_name="Contract signed")
    total_amount = models.FloatField(default=0.0)
    remaining_amount = models.FloatField(default=0.0)

    def __str__(self):
        client_name = f"{self.client.full_name}"
        status_contract_str = "Contract signed" if self.status_contract else "Contract not signed"

        return f"Contrat ID : {self.id} {client_name} {status_contract_str}"

    def save(self, *args, **kwargs):
        # Mettre à jour la date de mise à jour avant de sauvegarder
        self.update_date = timezone.now()
        super(Contract, self).save(*args, **kwargs)
