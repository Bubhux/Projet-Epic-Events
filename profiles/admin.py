from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.db.models import Count, Subquery, OuterRef

from .models import User, Client


class CustomUserAdmin(UserAdmin):
    """
    Personnalisation de l'interface d'administration pour le modèle User.
    Affiche et configure les champs spécifiques pour l'administration des utilisateurs.
    """

    list_display = ('full_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'role')
    ordering = ('full_name',)
    search_fields = ('full_name', 'email')

    fieldsets = (
        # Section pour les champs d'authentification (email et mot de passe)
        (None, {'fields': ('email', 'password')}),

        # Section pour les informations personnelles (nom, numéro de téléphone, rôle)
        ('Informations personnelles', {'fields': ('full_name', 'phone_number', 'role')}),

        # Section pour les permissions
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),

        # Section pour les dates importantes (dernière connexion, date d'inscription)
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        # Section pour les champs lors de l'ajout d'un nouvel utilisateur
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'phone_number', 'is_active', 'is_staff', 'role', 'date_joined'),
        }),
    )


class ClientAdmin(admin.ModelAdmin):
    """
    Personnalisation de l'interface d'administration pour le modèle Client.
    Affiche et configure les champs spécifiques pour l'administration des clients.
    """

    list_display = ('full_name', 'email', 'company_name', 'sales_contact', 'last_contact')
    ordering = ('full_name',)
    search_fields = ('full_name', 'email', 'company_name', 'user_contact__full_name', 'sales_contact__full_name')


class GroupAdmin(admin.ModelAdmin):
    """
    Personnalisation de l'interface d'administration pour le modèle Group.
    Affiche le nombre total d'utilisateurs pour chaque groupe.
    """

    list_display = ('name', 'total_users')

    def get_queryset(self, request):
        """
        Surcharge la méthode get_queryset pour annoter chaque groupe avec le nombre total d'utilisateurs.
        """
        # Récupérer le queryset de la classe parent
        queryset = super().get_queryset(request)

        # Annoter avec le nombre total d'utilisateurs
        # Filtrer les objets du modèle Client associés au groupe en cours d'annotation dans la requête GroupAdmin.
        # OuterRef('id') fait référence à l'ID du groupe actuel dans la requête GroupAdmin.
        # Récupérer les valeurs du champ user_contact__groups pour les objets filtrés.
        # Cela représente les groupes associés aux clients filtrés.
        # Ajouter une annotation 'count' en comptant le nombre d'objets dans chaque groupe.
        # Récupérer les valeurs de l'annotation 'count' pour le premier objet (le seul objet).
        # Cela donne le nombre total d'objets dans le modèle Client associés au groupe actuel.
        # La sous-requête Subquery retourne le nombre total d'objets dans le modèle Client associés au groupe actuel.
        # Cette valeur est utilisée comme annotation 'client_count' pour chaque objet Group dans la requête GroupAdmin.
        # Annoter chaque objet Group avec le résultat de la sous-requête, représentant le nombre total d'objets associés dans le modèle Client.
        # Retourner le queryset annoté
        queryset = queryset.annotate(
            client_count=Subquery(
                Client.objects.filter(user_contact__groups=OuterRef('id'))
                .values('user_contact__groups')
                .annotate(count=Count('id'))
                .values('count')[:1]
            )
        )
        return queryset

    def total_users(self, obj):
        """
        Retourne le nombre total d'utilisateurs pour chaque groupe.
        """
        if obj.name == 'Client':
            return obj.client_count
        elif obj.name == 'Staff':
            # Obtient le groupe "Staff" et retourne le nombre d'utilisateurs dans ce groupe
            staff_group = Group.objects.get(name='Staff')
            return staff_group.user_set.count()

    total_users.short_description = "Nombre d'utilisateurs"


# Enregistrer la classe CustomUserAdmin avec le modèle User
admin.site.register(User, CustomUserAdmin)

# Enregistrer la classe ClientAdmin avec le modèle Client
admin.site.register(Client, ClientAdmin)

# Enregistre le nouveau admin.ModelAdmin pour Group
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
