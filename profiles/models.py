from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, pre_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Count
from itertools import cycle


class UserManager(BaseUserManager):

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

        # Imprime les détails du superutilisateur
        print(f"Nom du superutilisateur : {superuser.full_name}")
        print(f"Role du superutilisateur : {superuser.get_role_display()}")
        print(f"Statut 'is_staff' du superutilisateur : {superuser.is_staff}")
        print(f"Statut 'is_superuser' du superutilisateur : {superuser.is_superuser}")


class User(AbstractBaseUser, PermissionsMixin):

    ROLE_MANAGEMENT = 'Management team'
    ROLE_SALES = 'Sales team'
    ROLE_SUPPORT = 'Support team'

    ROLE_CHOICES = (
        (ROLE_MANAGEMENT, 'Équipe Gestion'),
        (ROLE_SALES, 'Équipe Commerciale'),
        (ROLE_SUPPORT, 'Équipe Support'),
    )

    email = models.EmailField(unique=True)
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
        return f"{self.get_role_display()} - {self.full_name} ({self.email})"

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

    email = models.EmailField(unique=True, editable=True)
    full_name = models.CharField(max_length=255, help_text="Full name of the client.")
    user_contact = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True, related_name='client_profiles', related_query_name='client_profile', default=None)
    phone_number = models.CharField(max_length=20, help_text="Phone number of the client.")
    company_name = models.CharField(max_length=255, help_text="Name of the client's company.")
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    last_contact = models.DateTimeField(null=True, blank=True)
    sales_contact = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True, editable=True, limit_choices_to={'role': User.ROLE_SALES})
    email_contact_id = models.EmailField(null=True, blank=True, editable=True)

    class Meta:
        ordering = ['update_date']

    def __str__(self):
        if self.user_contact:
            return f"Client {self.full_name} - Contact commercial {self.user_contact.full_name}"
        else:
            return f"Client {self.full_name} - Aucun contact commercial associé"

    def print_details(self):
        print(f"ID du client : {self.id}")
        print(f"Nom du client : {self.full_name}")
        print(f"E-mail du client : {self.email}")
        print(f"Compagnie du client : {self.company_name}")

        # Imprime les détails du contact commercial
        if self.sales_contact:
            print(f"Contact commercial : {self.sales_contact.full_name}")
            print(f"E-mail du contact commercial : {self.sales_contact.email}")
            print(f"Téléphone du contact commercial : {self.sales_contact.phone_number}")

    @classmethod
    def assign_sales_contact(cls):
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
        unassigned_clients = cls.objects.filter(user_contact=None)
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

    def save(self, *args, **kwargs):
        # Imprime le nombre total de clients avant la sauvegarde
        print(f"Nombre total de clients avant la sauvegarde : {Client.objects.count()}")

        # Met à jour la colonne email_id avec l'e-mail de l'utilisateur associé
        self.email_contact_id = self.user_contact.email if self.user_contact else None
        self.sales_contact_id = self.user_contact.id if self.user_contact else None
        self.update_date = timezone.now()
        super().save(*args, **kwargs)

        # Imprime les détails après la sauvegarde
        self.print_details()

        # Imprime le nombre total de clients après la sauvegarde
        print(f"Nombre total de clients après la sauvegarde : {Client.objects.count()}")


class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


@receiver(pre_delete, sender=Client)
def delete_client_from_group(sender, instance, **kwargs):
    # Vérifie si le groupe "Client" existe
    client_group, created = Group.objects.get_or_create(name='Client')
    # Retire l'instance du groupe si user_contact est défini
    if instance.user_contact:
        instance.user_contact.groups.remove(client_group)
    elif instance.user_contact_id:
        # Si user_contact_id est défini mais user_contact est None, utilisez-le pour retirer du groupe
        user_contact = User.objects.get(id=instance.user_contact_id)
        user_contact.groups.remove(client_group)

@receiver(post_save, sender=Client)
def add_client_to_group(sender, instance, **kwargs):
    # Vérifie si le groupe "Client" existe
    client_group, created = Group.objects.get_or_create(name='Client')

    # Ajoute l'instance de Client au groupe, même si user_contact est None
    if instance.user_contact:
        instance.user_contact.groups.add(client_group)
    elif instance.sales_contact:
        instance.sales_contact.groups.add(client_group)

@receiver(pre_delete, sender=User)
def delete_user_groups(sender, instance, **kwargs):
    # Supprime les enregistrements associés dans la table UserGroup
    UserGroup.objects.filter(user=instance).delete()

@receiver(pre_save, sender=Client)
def set_sales_contact_id(sender, instance, **kwargs):
    # Cette fonction sera appelée avant chaque enregistrement (save) d'un objet Client
    # Vérifie si sales_contact est défini et sales_contact_id n'est pas défini
    if instance.sales_contact and not instance.sales_contact_id:
        # Mets à jour sales_contact_id avec l'ID de l'utilisateur associé
        instance.sales_contact_id = instance.sales_contact.id
