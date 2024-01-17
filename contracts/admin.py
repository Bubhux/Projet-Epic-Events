from django.contrib import admin

from .models import Contract


class ContractAdmin(admin.ModelAdmin):
    """
    Personnalisation de l'interface d'administration pour le modèle Contract.
    Affiche et configure les champs spécifiques pour l'administration des utilisateurs.
    """

    list_display = ( 'client', 'status_contract', 'sales_contact', 'creation_date', 'update_date')
    ordering = ('status_contract',)
    search_fields = ('sales_contact__full_name', 'client__full_name')

    fieldsets = (
        ('Informations du contrat', {
            'fields': ('client', 'sales_contact', 'status_contract','total_amount', 'remaining_amount', 'creation_date', 'update_date'),
        }),
    )

    readonly_fields = ('creation_date', 'update_date')

    def get_readonly_fields(self, request, obj=None):
        # Retourne une liste de champs en lecture seule
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj:
            # Ajoute 'creation_date' et 'update_date' à la liste des champs en lecture seule lors de la modification d'un objet existant
            readonly_fields += ('creation_date', 'update_date')
        return readonly_fields


# Enregistrer la classe ContractAdmin avec le modèle Contract
admin.site.register(Contract, ContractAdmin)
