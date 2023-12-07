
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime


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

    ROLE_MANAGEMENT = 'management team'
    ROLE_SALES = 'sales team'
    ROLE_SUPPORT = 'support team'

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

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    company_name = models.CharField(max_length=255, help_text="Name of the client's company.")
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    last_contact = models.DateField(null=True, blank=True)
    sales_contact = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': User.ROLE_SALES})

    class Meta:
        ordering = ['-update_date']  # Tri par défaut, modification la plus récente en premier

    def __str__(self):
        return f"{self.id} - {self.user.full_name}"

    def save(self, *args, **kwargs):
        self.update_date = datetime.now()
        super(Client, self).save(*args, **kwargs)

