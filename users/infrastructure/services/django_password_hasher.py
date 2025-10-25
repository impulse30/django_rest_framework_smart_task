from django.contrib.auth.hashers import make_password, check_password
from users.application.services.password_hasher import PasswordHasher

class DjangoPasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return make_password(password)

    def verify(self, password_hash: str, password: str) -> bool:
        return check_password(password, password_hash)
