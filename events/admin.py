from django.contrib import admin

from .models import Event


class EventAdmin(admin.ModelAdmin):
    """
        Personnalisation de l'interface d'administration pour le modèle Event.
        Affiche et configure les champs spécifiques pour l'administration des utilisateurs.
    """

    list_display = ( 'client', 'event', 'contract', 'support_contact')
    ordering = ('client',)
    search_fields = ('client', 'event')

    fieldsets = (
        ("Informations de l'événement", {
            'fields': ('client', 'client_name', 'event', 'contract','event_date_start', 'event_date_end',
                        'client_contact', 'support_contact','location', 'attendees', 'notes'
                      ),
        }),
    )


# Enregistrer la classe ContractAdmin avec le modèle Contract
admin.site.register(Event, EventAdmin)
