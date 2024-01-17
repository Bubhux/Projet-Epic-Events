from django.contrib import admin

from .models import Event


class EventAdmin(admin.ModelAdmin):
    """
        Personnalisation de l'interface d'administration pour le modèle Event.

        Cette classe personnalisée pour l'administration des événements (Event) permet de configurer
        l'affichage et les champs spécifiques dans l'interface d'administration Django.

        Attributs :
            - list_display : Liste des champs à afficher dans la liste d'aperçu.
            - ordering : Ordre de tri par défaut pour la liste des événements.
            - search_fields : Champs utilisés pour la recherche dans l'interface d'administration.
            - fieldsets : Définition des sections de champs dans le formulaire d'édition.

        Méthodes :
            - get_form : Surcharge de la méthode pour ajuster le queryset du champ 'contract'
                        en fonction du client associé lors de l'édition.
    """
    list_display = ('client', 'event', 'contract', 'support_contact')
    ordering = ('client',)
    search_fields = ('client', 'event')

    fieldsets = (
        ("Informations de l'événement", {
            'fields': ('client', 'client_name', 'event', 'contract', 'event_date_start', 'event_date_end',
                       'client_contact', 'support_contact', 'location', 'attendees', 'notes'),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        """
            Surcharge de la méthode get_form pour ajuster le queryset du champ 'contract'
            en fonction du client associé lors de l'édition.

            Args:
                - request : L'objet HttpRequest.
                - obj : L'objet Event en cours d'édition.
                - kwargs : Les arguments supplémentaires.

            Returns:
                - Le formulaire personnalisé.
        """
        form = super().get_form(request, obj, **kwargs)
        # Limitez les choix du champ contract aux contrats du client associé
        if obj:
            client_id = obj.client_id
            form.base_fields['contract'].queryset = form.base_fields['contract'].queryset.filter(client_id=client_id)
        return form


# Enregistrer la classe EventAdmin avec le modèle Event
admin.site.register(Event, EventAdmin)
