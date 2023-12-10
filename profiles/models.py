
import random

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, role=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, role=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, role, **extra_fields)


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
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    full_name = models.CharField(max_length=255, help_text="Full name of the user.")
    phone_number = models.CharField(max_length=20, help_text="Phone number of the user.")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role', 'full_name', 'phone_number']

    def __str__(self):
        return f"{self.get_role_display()} - {self.full_name} ({self.email})"


class Client(models.Model):

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, help_text="Full name of the client.")
    user_contact = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    phone_number = models.CharField(max_length=20, help_text="Phone number of the client.")
    company_name = models.CharField(max_length=255, help_text="Name of the client's company.")
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    last_contact = models.DateTimeField(null=True, blank=True)
    sales_contact = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': User.ROLE_SALES})
    email_contact_id = models.EmailField(null=True, blank=True, editable=False)

    class Meta:
        ordering = ['-update_date']

    def __str__(self):
        return f"Client {self.full_name} - Contact commercial {self.user_contact.full_name}"

    def save(self, *args, **kwargs):
        if not self.user_contact:
            sales_users_without_clients = User.objects.filter(
                role=User.ROLE_SALES,
                client_profile__isnull=True
            )
            if not sales_users_without_clients.exists():
                raise ValidationError("Aucun utilisateur avec le rôle 'ROLE_SALES' et sans client trouvé.")

            self.user = random.choice(sales_users_without_clients)

        # Mettez à jour la colonne email_id avec l'e-mail de l'utilisateur associé
        self.email_contact_id = self.user_contact.email
        self.sales_contact_id = self.user_contact.id
        self.update_date = timezone.now()
        super(Client, self).save(*args, **kwargs)


@receiver(pre_save, sender=Client)
def set_sales_contact_id(sender, instance, **kwargs):
    # Cette fonction sera appelée avant chaque enregistrement (save) d'un objet Client
    # Vérifiez si sales_contact est défini et sales_contact_id n'est pas défini
    if instance.sales_contact and not instance.sales_contact_id:
        # Mettez à jour sales_contact_id avec l'ID de l'utilisateur associé
        instance.sales_contact_id = instance.sales_contact.id
