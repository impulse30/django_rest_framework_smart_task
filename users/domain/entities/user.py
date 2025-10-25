import uuid

class User:
    """
    Entité représentant un utilisateur dans le domaine.
    Indépendante de tout framework.
    """
    def __init__(
        self,
        id,
        email,
        full_name,
        password_hash=None,  # Ne pas stocker le mot de passe en clair
        avatar=None,
        is_active=True,
        is_staff=False,
        date_joined=None,
    ):
        self.id = id or uuid.uuid4()
        self.email = self._validate_email(email)
        self.full_name = self._validate_full_name(full_name)
        self.password_hash = password_hash
        self.avatar = avatar
        self.is_active = is_active
        self.is_staff = is_staff
        self.date_joined = date_joined

    def _validate_email(self, email):
        if not email or "@" not in email:
            raise ValueError("L'adresse email est invalide.")
        return email.lower()

    def _validate_full_name(self, full_name):
        if not full_name or len(full_name.strip()) == 0:
            raise ValueError("Le nom complet ne peut pas être vide.")
        return full_name.strip()

    def set_password(self, password, hasher):
        """
        Définit le mot de passe de l'utilisateur en utilisant un hasher externe.
        """
        if not password or len(password) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")
        self.password_hash = hasher.hash(password)

    def check_password(self, password, hasher):
        """
        Vérifie si un mot de passe correspond au hash stocké.
        """
        return hasher.verify(self.password_hash, password)

    def __eq__(self, other):
        return isinstance(other, User) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def first_name(self):
        """Retourne le premier prénom."""
        return self.full_name.split(" ")[0] if self.full_name else ""
