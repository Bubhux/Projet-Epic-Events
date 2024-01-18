from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Count
from itertools import cycle


class UserManager(BaseUserManager):
    """
        Gestionnaire d'utilisateurs personnalisé pour la classe User.

        Méthode create_user:
            Crée et enregistre un utilisateur avec un e-mail, un mot de passe et un rôle.
            Si l'utilisateur fait partie de l'équipe de gestion, définir is_superuser à True.
            Imprime les détails de l'utilisateur après la création.

        Méthode create_superuser:
            Crée et enregistre un superutilisateur avec un e-mail, un mot de passe et des privilèges d'administration.
            Appelle la méthode create_user pour créer le superutilisateur.
            Imprime les détails du superutilisateur après la création.
    """
    def create_user(self, email, password=None, role=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)

        # Si l'utilisateur fait partie de l'équipe de gestion, définir is_superuser à True
        if role == User.ROLE_MANAGEMENT:
            user.is_superuser = True

        user.save(using=self._db)

        # Imprime les détails de l'utilisateur
        print()
        print(f"Nom de l'utilisateur : {user.full_name}")
        print(f"Role de l'utilisateur : {user.get_role_display()}")
        print(f"Statut 'is_staff' de l'utilisateur : {user.is_staff}")
        print(f"Est superutilisateur : {user.is_superuser}")
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.ROLE_MANAGEMENT)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Appel la méthode create_user pour créer le superutilisateur
        superuser = self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
        Modèle d'utilisateur personnalisé avec prise en charge des rôles et des privilèges d'administration.

        Attributs:
            ROLE_MANAGEMENT: Constante pour le rôle de l'équipe de gestion.
            ROLE_SALES: Constante pour le rôle de l'équipe commerciale.
            ROLE_SUPPORT: Constante pour le rôle de l'équipe de support.
            ROLE_CHOICES: Choix de rôles disponibles.

        Champs:
            email: Adresse e-mail de l'utilisateur.
            role: Rôle de l'utilisateur.
            is_active: Indique si l'utilisateur est actif.
            is_staff: Indique si l'utilisateur a des privilèges d'administration.
            full_name: Nom complet de l'utilisateur.
            phone_number: Numéro de téléphone de l'utilisateur.
            date_joined: Date d'adhésion de l'utilisateur.

        Méthodes:
            __str__: Renvoie une représentation en chaîne de l'utilisateur.
            has_perm: Vérifie les permissions individuelles.
            has_module_perms: Vérifie les permissions du module d'application.
            save: Enregistre l'utilisateur et l'ajoute au groupe "Staff".
    """
    ROLE_MANAGEMENT = 'Management team'
    ROLE_SALES = 'Sales team'
    ROLE_SUPPORT = 'Support team'

    ROLE_CHOICES = (
        (ROLE_MANAGEMENT, 'Équipe Gestion'),
        (ROLE_SALES, 'Équipe Commerciale'),
        (ROLE_SUPPORT, 'Équipe Support'),
    )

    email = models.EmailField(unique=True, editable=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True, editable=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    full_name = models.CharField(max_length=255, unique=True, help_text="Full name of the user.")
    phone_number = models.CharField(max_length=20, help_text="Phone number of the user.")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='date joined')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        """Renvoie une représentation lisible de l'instance de User."""
        return f"User ID : {self.id} {self.get_role_display()} - {self.full_name} ({self.email})"

    def has_perm(self, perm, obj=None):
        # Vérifie les permissions individuelles
        # Vérifie si l'utilisateur a la permission spécifiée
        return True

    def has_module_perms(self, app_label):
        # Vérifie les permissions du module d'application
        # Vérifie si l'utilisateur a des permissions pour l'application spécifiée
        return True

    def save(self, *args, **kwargs):
        # Appel la méthode save de la classe parent
        super().save(*args, **kwargs)

        # Ajoute l'utilisateur au groupe "Staff" s'il n'y est pas déjà
        staff_group, created = Group.objects.get_or_create(name='Staff')
        self.groups.add(staff_group)


class Client(models.Model):
    """
        Modèle représentant un client dans le CRM.

        Champs:
            email: Adresse e-mail du client.
            full_name: Nom complet du client.
            user_contact: Utilisateur associé au client.
            phone_number: Numéro de téléphone du client.
            company_name: Nom de l'entreprise du client.
            creation_date: Date de création du client.
            update_date: Date de mise à jour du client.
            last_contact: Dernier contact du client.
            sales_contact: Contact commercial associé au client.
            email_contact: E-mail du contact commercial.

        Méthodes:
            __str__: Renvoie une représentation en chaîne du client.
            print_details: Imprime les détails du client.
            assign_sales_contact: Affecte un contact commercial à un client non associé.
            save: Enregistre le client avec gestion des erreurs d'intégrité.
    """
    email = models.EmailField(unique=True, editable=True)
    full_name = models.CharField(max_length=255, help_text="Full name of the client.")
    user_contact = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True, related_name='user_contact_clients', related_query_name='user_contact_client', default=None)
    phone_number = models.CharField(max_length=20, help_text="Phone number of the client.")
    company_name = models.CharField(max_length=255, help_text="Name of the client's company.")
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True, editable=True)
    last_contact = models.DateTimeField(null=True, blank=True)
    sales_contact = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True, editable=True, limit_choices_to={'role': User.ROLE_SALES})
    email_contact = models.EmailField(null=True, blank=True, editable=True)

    class Meta:
        ordering = ['update_date']

    def __str__(self):
        """Renvoie une représentation lisible de l'instance de Client."""
        if self.user_contact:
            return f"Client ID : {self.id} {self.full_name} - Contact commercial {self.user_contact.full_name}"
        #else:
        #    return f"Client ID : {self.id} {self.full_name} - Aucun contact commercial associé"

    def print_details(self):
        """Affiche les détails de client dans la console."""
        # Imprime les détails du contact commercial
        if self.sales_contact:
            print()
            print(f"Contact commercial : {self.sales_contact.full_name}")
            print(f"E-mail du contact commercial : {self.sales_contact.email}")
            print(f"Téléphone du contact commercial : {self.sales_contact.phone_number}")
            print()

    def assign_sales_contact(self):
        """Affecte un contact commercial à un client non associé."""
        # Obtient tous les utilisateurs de l'équipe commerciale avec le nombre de clients associés à chacun
        sales_team = User.objects.filter(role=User.ROLE_SALES)

        if not sales_team.exists():
            print("Aucun utilisateur dans l'équipe de vente.")
            return

        sales_counts = sales_team.annotate(client_count=Count('client'))

        # Trie les utilisateurs par nombre de clients, puis par ordre d'ID
        sorted_sales_team = sorted(sales_counts, key=lambda x: (x.client_count, x.id))

        # Crée un itérateur cyclique pour la répartition équilibrée
        sales_cycle = cycle(sorted_sales_team)

        # Obtient le groupe "Client"
        client_group, created = Group.objects.get_or_create(name='Client')

        # Parcourt tous les clients non associés et leur assigne un contact commercial
        unassigned_clients = Client.objects.filter(user_contact=None)
        for client in unassigned_clients:
            # Vérifie si user_contact est défini avant d'assigner le client à un contact commercial
            if not client.user_contact:
                # Obtient le prochain utilisateur dans la séquence cyclique
                sales_contact = next(sales_cycle)

                # Associe le client à l'utilisateur actuel
                client.user_contact = sales_contact
                client.sales_contact = sales_contact
                client.save()

                # Ajoute l'instance de Client au groupe Client
                client.user_contact.groups.add(client_group)

                # Actualise l'instance avec les données actuelles de la base de données
                # Cela garantit que les changements persistants dans la base de données sont reflétés dans l'instance
                self.refresh_from_db()

    def save(self, *args, **kwargs):
        """
            Sauvegarde l'instance après vérification de la non-existence d'un client avec le même e-mail.
            Met à jour les colonnes email_id et sales_contact_id.
            Appelle la méthode save de la classe parent pour effectuer la sauvegarde réelle.
            Imprime les détails avant et après la sauvegarde.
            Exécute automatiquement la méthode assign_sales_contact après la sauvegarde.
        """
        try:
            # Vérifie si un client avec le même e-mail existe déjà
            client_existant = Client.objects.filter(email=self.email).exclude(id=self.id).first()

            if client_existant:
                raise IntegrityError("This user already exists in the database.")
        except IntegrityError as e:
            # Gère l'IntegrityError en imprimant le message d'erreur personnalisé
            print(f"Erreur d'intégrité : {e}")
            return
        else:
            # Récupère l'utilisateur associé à partir de user_contact_id
            user_contact = User.objects.filter(id=self.user_contact_id).first()

            # Met à jour la colonne email_contact avec l'e-mail de l'utilisateur associé
            self.email_contact = self.user_contact.email if self.user_contact else None
            self.sales_contact = self.user_contact if self.user_contact else None
            self.update_date = timezone.now()

            # Appelle la méthode save de la classe parent pour effectuer la sauvegarde réelle
            super().save(*args, **kwargs)

            # Imprime les détails après la sauvegarde
            self.print_details()

            # Exécute automatiquement la méthode assign_sales_contact après la sauvegarde
            self.assign_sales_contact()


class UserGroup(models.Model):
    """
        Modèle représentant un groupe d'utilisateurs dans le CRM.

        Champs:
            user: Utilisateur associé au groupe.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)


@receiver(post_save, sender=Client)
def add_client_to_group(sender, instance, **kwargs):
    """
        Fonction de réception appelée après la sauvegarde d'une instance de Client.
        Ajoute l'instance de Client au groupe "Client" si elle est associée à un contact utilisateur ou un utilisateur commercial.
    """
    # Vérifie si le groupe "Client" existe
    client_group, created = Group.objects.get_or_create(name='Client')

    # Ajoute l'instance de Client au groupe, même si user_contact est None
    if instance.user_contact:
        instance.user_contact.groups.add(client_group)
    elif instance.sales_contact:
        instance.sales_contact.groups.add(client_group)

@receiver(pre_delete, sender=User)
def delete_user_groups(sender, instance, **kwargs):
    """
        Fonction de réception appelée avant la suppression d'une instance de User.
        Supprime les enregistrements associés dans la table UserGroup.
    """
    # Supprime les enregistrements associés dans la table UserGroup
    UserGroup.objects.filter(user=instance).delete()

@receiver(pre_save, sender=Client)
def set_sales_contact_id(sender, instance, **kwargs):
    """
        Fonction de réception appelée avant chaque sauvegarde d'un objet Client.
        Vérifie si sales_contact est défini et sales_contact_id n'est pas défini.
        Mets à jour sales_contact_id avec l'ID de l'utilisateur associé.
    """
    # Cette fonction sera appelée avant chaque enregistrement (save) d'un objet Client
    # Vérifie si sales_contact est défini et sales_contact_id n'est pas défini
    if instance.sales_contact and not instance.sales_contact_id:
        # Mets à jour sales_contact_id avec l'ID de l'utilisateur associé
        instance.sales_contact_id = instance.sales_contact.id
