from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Gestionnaire personnalisé pour le modèle User."""

    def create_user(self, email, password=None, **extra_fields):
        """
        Crée et enregistre un utilisateur avec un email et un mot de passe.
        """
        if not email:
            raise ValueError("L'utilisateur doit avoir une adresse email.")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crée et enregistre un superutilisateur (admin).
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Le superutilisateur doit avoir is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Le superutilisateur doit avoir is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Modèle personnalisé d'utilisateur basé sur l'email."""

    email = models.EmailField(
        unique=True,
        max_length=191,
        verbose_name="Adresse email"
    )
    full_name = models.CharField(
        max_length=191,
        verbose_name="Nom complet"
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
        verbose_name="Avatar"
    )

    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_staff = models.BooleanField(default=False, verbose_name="Membre du staff")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Date d'inscription")

    # Gestionnaire personnalisé
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    @property
    def first_name(self):
        """Retourne le premier prénom (utile pour les affichages courts)."""
        return self.full_name.split(" ")[0] if self.full_name else ""
