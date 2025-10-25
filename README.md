# Guide de Configuration et d'Architecture du Projet Django

Ce document sert de guide complet pour l'installation, la configuration et la compréhension de l'architecture de ce projet Django. Il est destiné à aider les développeurs à mettre en place leur environnement et à comprendre les choix de conception qui sous-tendent le code.

## Table des matières
1. [Gestion de l'Environnement](#gestion-de-lenvironnement)
    - [Environnement Virtuel (venv)](#environnement-virtuel-venv)
    - [Variables d'Environnement (.env)](#variables-denvironnement-env)
2. [Configuration de Django : Settings multi-environnements](#configuration-de-django--settings-multi-environnements)
    - [Structure des fichiers](#structure-des-fichiers)
    - [Principe de fonctionnement](#principe-de-fonctionnement)
    - [Mise en place](#mise-en-place)
3. [Clean Architecture avec Django REST Framework](#clean-architecture-avec-django-rest-framework)
    - [Les 4 Couches de l'Architecture](#les-4-couches-de-larchitecture)
    - [Exemple d'un flux de requête](#exemple-dun-flux-de-requête)
4. [Workflow de Démarrage Rapide](#workflow-de-démarrage-rapide)
5. [Structure et Fonctionnalités des Applications](#structure-et-fonctionnalités-des-applications)
6. [Guide d'implémentation : Ajout de la fonctionnalité d'inscription](#guide-dimplémentation--ajout-de-la-fonctionnalité-dinscription)
7. [Guide d'implémentation : Ajout de la création de projet](#guide-dimplémentation--ajout-de-la-création-de-projet)

---

## Gestion de l'Environnement

Une gestion saine de l'environnement est cruciale pour la reproductibilité et la sécurité du projet.

### Environnement Virtuel (venv)

Nous utilisons un environnement virtuel pour isoler les dépendances du projet de celles du système global.

**Pourquoi ?**
- **Isolation** : Évite les conflits de versions entre les paquets de différents projets.
- **Reproductibilité** : Le fichier `requirements.txt` garantit que tous les développeurs utilisent les mêmes versions des dépendances.

**Mise en place :**
1.  **Créez l'environnement virtuel** (à la racine du projet) :
    ```bash
    python -m venv venv
    ```
2.  **Activez-le** :
    - Sur macOS/Linux :
      ```bash
      source venv/bin/activate
      ```
    - Sur Windows :
      ```bash
      venv\Scripts\activate
      ```
3.  **Installez les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```

### Variables d'Environnement (.env)

Les informations sensibles (clés d'API, mots de passe de base de données, etc.) et les configurations spécifiques à un environnement (développement, production) ne doivent jamais être versionnées dans le code.

**Mise en place :**
1.  Ce projet utilise un fichier `.env` pour charger ces variables. Ce fichier est ignoré par Git (via `.gitignore`).
2.  Pour commencer, copiez le fichier d'exemple :
    ```bash
    cp .env.example .env
    ```
3.  **Modifiez le fichier `.env`** avec vos propres valeurs.

Le projet utilise la bibliothèque `python-dotenv` pour charger automatiquement les variables de ce fichier au démarrage de l'application.

---

## Configuration de Django : Settings multi-environnements

Pour gérer facilement les configurations entre les différents environnements (développement, test, production), nous avons centralisé et divisé les fichiers de `settings`.

### Structure des fichiers

La configuration de Django se trouve dans le dossier `votre_projet/settings/` et est structurée comme suit :

```
votre_projet/
├── settings/
│   ├── __init__.py
│   ├── base.py         # Configuration commune à tous les environnements
│   ├── development.py  # Configuration spécifique pour le développement
│   └── production.py   # Configuration spécifique pour la production
└── ...
```

### Principe de fonctionnement

-   `base.py` : Contient 90% de la configuration : `INSTALLED_APPS`, `MIDDLEWARE`, `TEMPLATES`, chemins statiques, etc. Il lit les variables du fichier `.env` (ex: `SECRET_KEY`).
-   `development.py` : Importe toute la configuration de `base.py` (`from .base import *`) et y ajoute ou modifie des paramètres spécifiques au développement (ex: `DEBUG = True`, base de données SQLite, `ALLOWED_HOSTS = ['*']`).
-   `production.py` : Importe également de `base.py` et configure l'application pour la production (ex: `DEBUG = False`, base de données PostgreSQL, `ALLOWED_HOSTS` restreints, paramètres de sécurité renforcés).

### Mise en place

Pour que Django sache quel fichier de configuration utiliser, nous définissons la variable d'environnement `DJANGO_SETTINGS_MODULE`.

1.  **Dans votre fichier `.env`**, ajoutez la ligne suivante pour le développement local :
    ```dotenv
    DJANGO_SETTINGS_MODULE=votre_projet.settings.development
    ```
2.  Les fichiers `manage.py` et `votre_projet/wsgi.py` sont configurés pour lire cette variable et ainsi charger le bon module de settings.

---

## Clean Architecture avec Django REST Framework

Pour garantir que le code reste maintenable, testable et évolutif, ce projet adopte les principes de la **Clean Architecture**. L'idée principale est la **séparation des responsabilités** (`Separation of Concerns`).

### Les 4 Couches de l'Architecture

Notre architecture est divisée en quatre couches logiques, de la plus interne à la plus externe.

#### 1. Domaine (Entities)
-   **Rôle** : Le cœur de votre application. Contient la logique métier et les règles les plus fondamentales.
-   **Implémentation** : Des classes Python pures qui ne dépendent d'aucun framework. Dans l'application `users`, l'entité `User` (`users/domain/entities/user.py`) est un exemple de cette couche.

#### 2. Application (Use Cases / Services)
-   **Rôle** : Orchestre le flux de données et exécute les cas d'utilisation (logique applicative). C'est ici que se trouve la logique métier spécifique à une action (ex: "créer un utilisateur", "calculer le total d'une commande").
-   **Implémentation** : Des fichiers `services.py` ou `use_cases.py`. Ces fichiers contiennent des classes qui prennent des données simples en entrée, appliquent la logique, et interagissent avec la couche Domaine via les Repositories. **Cette couche ne connaît ni HTTP, ni Django REST Framework.** L'`AuthService` (`users/application/services/auth_service.py`) en est un bon exemple.

#### 3. Présentation (API / Framework)
-   **Rôle** : Gère tout ce qui est lié à l'interface externe (dans notre cas, une API REST). Elle reçoit les requêtes HTTP, valide les données entrantes, et renvoie des réponses formatées (JSON).
-   **Implémentation** : Les `views.py` (ViewSets, APIViews), `serializers.py` et `urls.py` de Django REST Framework. Le rôle de cette couche est de traduire les requêtes HTTP en appels à la couche Application et de formater les résultats pour le client. **Elle ne doit contenir aucune logique métier.** Les vues de l'application `users` (`users/presentation/views/auth_view.py`) utilisent l'injection de dépendances pour appeler les services de la couche application.

#### 4. Infrastructure (Frameworks & Drivers)
-   **Rôle** : Contient tout ce qui est externe à l'application : la base de données, les services externes (APIs tierces), le cache, etc.
-   **Implémentation** : Cette couche est matérialisée par le **Repository Pattern** et les modèles Django. Les `repositories.py` abstraient l'accès à la base de données. Par exemple, au lieu d'appeler `User.objects.create()` directement dans la couche Application, on appellerait `user_repository.create_user()`. Les modèles Django, comme `UserModel` (`users/infrastructure/models/user_model.py`), sont considérés comme des détails d'implémentation de la persistance des données.

### Exemple d'un flux de requête

Imaginons une requête `POST /api/users/register/` pour créer un nouvel utilisateur :

1.  **Présentation (API)**
    -   `urls.py` dirige la requête vers `RegisterView`.
    -   `RegisterView` utilise `RegisterSerializer` pour valider les données JSON reçues (`request.data`).
    -   Si la validation réussit, la vue injecte les dépendances nécessaires dans `AuthService` et l'appelle :
        ```python
        # users/presentation/views/auth_view.py
        auth_service = get_auth_service()
        user = auth_service.register_user(**serializer.validated_data)
        ```

2.  **Application (Service)**
    -   `AuthService` reçoit les données validées.
    -   Il exécute la logique métier : vérifier si l'email existe déjà, hacher le mot de passe, etc.
    -   Il appelle ensuite la couche Infrastructure (Repository) pour persister les données :
        ```python
        # users/application/services/auth_service.py
        password_hash = self.password_hasher.hash(password)
        user = User(email=email, full_name=full_name, password_hash=password_hash)
        return self.user_repository.create_user(user)
        ```

3.  **Infrastructure (Repository)**
    -   Le `UserRepository` dans `users/infrastructure/repositories/user_repository.py` contient la logique d'accès à la base de données, qui est spécifique à l'ORM de Django. Il utilise un `UserMapper` pour convertir l'entité `User` en `UserModel` avant de la sauvegarder.
        ```python
        # users/infrastructure/repositories/user_repository.py
        user_model = UserMapper.to_model(user_entity)
        user_model.set_password(user_entity.password_hash)
        user_model.save()
        ```

4.  **Domaine (Entity)**
    -   L'entité `User` est utilisée tout au long du processus pour représenter l'utilisateur de manière agnostique au framework.

Le flux de retour remonte ensuite les couches jusqu'à la vue, qui renvoie une réponse HTTP 201 Created avec les données de l'utilisateur sérialisées.

---

## Workflow de Démarrage Rapide

Pour un nouveau développeur, voici les étapes à suivre pour lancer le projet :

1.  **Clonez le dépôt Git.**
2.  **Créez et activez l'environnement virtuel** comme décrit [ci-dessus](#environnement-virtuel-venv).
3.  **Installez les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configurez vos variables d'environnement** :
    ```bash
    cp .env.example .env
    # Modifiez le fichier .env avec vos informations
    ```
5.  **Appliquez les migrations** de la base de données :
    ```bash
    python manage.py migrate
    ```
6.  **Lancez le serveur de développement** :
    ```bash
    python manage.py runserver
    ```

L'application devrait maintenant être accessible à l'adresse `http://127.0.0.1:8000/`.

---

## Structure et Fonctionnalités des Applications

Cette section détaille l'organisation des applications du projet selon la Clean Architecture et les fonctionnalités qu'elles exposent.

### Fonctionnalités par Application

#### Application `users`
- **Inscription (Registration)**
  - **Endpoint** : `POST /api/users/register/`
  - **Description** : Permet à un nouvel utilisateur de créer un compte.
- **Connexion (Login)**
  - **Endpoint** : `POST /api/users/login/`
  - **Description** : Permet à un utilisateur d'obtenir des jetons d'accès JWT.

#### Application `projects`
- **Création de Projet (Project Creation)**
  - **Endpoint** : `POST /api/projects/`
  - **Description** : Permet à un utilisateur authentifié de créer un nouveau projet. Le créateur devient administrateur du projet.

### Arborescence Détaillée

Voici la structure des fichiers de l'application `users`, expliquée couche par couche :

```
users/
├── domain/                      # 1. Le cœur de la logique métier (indépendant de tout)
│   └── entities/
│       └── user.py              # -> La classe User pure, qui représente un utilisateur.
│
├── application/                 # 2. La logique applicative (cas d'utilisation)
│   └── services/
│       ├── auth_service.py      # -> Orchestre l'inscription et la connexion.
│       ├── password_hasher.py   # -> Interface ABSTRAITE pour le hachage de mdp.
│       └── token_generator.py   # -> Interface ABSTRAITE pour la génération de token.
│
├── infrastructure/              # 3. Les détails techniques (Django, base de données, etc.)
│   ├── models/
│   │   └── user_model.py        # -> Le modèle Django qui est mappé à la table en BDD.
│   ├── repositories/
│   │   └── user_repository.py   # -> La classe qui communique avec la BDD via le UserModel.
│   ├── mappers/
│   │   └── user_mapper.py       # -> Traduit un User (domaine) en UserModel (BDD) et vice-versa.
│   └── services/
│       ├── django_password_hasher.py # -> Implémentation CONCRÈTE du hasher avec Django.
│       └── jwt_token_generator.py    # -> Implémentation CONCRÈTE du token avec JWT.
│
├── presentation/                # 4. L'interface avec l'extérieur (API REST)
│   ├── views/
│   │   └── auth_view.py         # -> Gère les requêtes HTTP pour /register et /login.
│   ├── serializers/
│   │   └── auth_serializers.py  # -> Valide les données JSON envoyées par le client.
│   └── urls.py                  # -> Définit les URLs de l'application.
│
├── admin.py                     # Fichier de configuration pour l'interface admin de Django.
├── models.py                    # Fichier "pont" pour que Django découvre notre UserModel.
├── apps.py                      # Configuration de l'application Django.
└── migrations/                  # Fichiers de migration de la base de données.
```

---

## Guide d'implémentation : Ajout de la fonctionnalité d'inscription

Cette section sert de tutoriel pour illustrer comment implémenter une fonctionnalité en respectant la Clean Architecture. Nous allons construire l'endpoint d'inscription (`POST /api/users/register/`) pas à pas.

### Étape 1 : Le Domaine (Le cœur)

On commence toujours par le domaine. On définit ce qu'est un `User` pour notre application, sans se soucier de la base de données ou du web.

**Fichier** : `users/domain/entities/user.py`

**Rôle** : Définir la structure, les validations de base et les règles métier de l'entité `User`. C'est un simple objet Python.

```python
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
        password_hash=None,
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

    # ... autres méthodes métier ...
```

### Étape 2 : L'Application (Les cas d'utilisation)

Maintenant, on définit le cas d'utilisation "Inscrire un utilisateur". On a besoin d'un service qui orchestre cette action. Ce service aura besoin de dépendances (comme un "hasher" de mot de passe), mais il ne connaîtra que leurs interfaces abstraites.

#### 2.1. Définir le contrat du Hasher

**Fichier** : `users/application/services/password_hasher.py`

**Rôle** : Définir ce que n'importe quel service de hachage doit pouvoir faire. C'est un contrat, pas une implémentation.

```python
import abc

class PasswordHasher(abc.ABC):
    @abc.abstractmethod
    def hash(self, password: str) -> str:
        ...

    @abc.abstractmethod
    def verify(self, password_hash: str, password: str) -> bool:
        ...
```

#### 2.2. Créer le Service d'Authentification

**Fichier** : `users/application/services/auth_service.py`

**Rôle** : Contenir la logique de l'inscription. Il dépend du `UserRepository` (pour parler à la BDD) et du `PasswordHasher`, mais uniquement via leurs abstractions.

```python
from users.domain.entities.user import User
from users.infrastructure.repositories.user_repository import UserRepository
from users.application.services.password_hasher import PasswordHasher

class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        # ... token_generator: TokenGenerator,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        # ...

    def register_user(self, email, password, full_name):
        if self.user_repository.exists_by_email(email):
            raise ValueError("Un utilisateur avec cet email existe déjà.")

        password_hash = self.password_hasher.hash(password)
        user = User(
            id=None,
            email=email,
            full_name=full_name,
            password_hash=password_hash
        )
        return self.user_repository.create_user(user)

    # ... login_user ...
```

### Étape 3 : L'Infrastructure (Les détails techniques)

C'est ici qu'on implémente les détails concrets : comment on stocke les données (avec Django) et comment on hache les mots de passe (avec les outils de Django).

#### 3.1. Le Modèle Django

**Fichier** : `users/infrastructure/models/user_model.py`

**Rôle** : La représentation de notre utilisateur dans la base de données. Ce fichier dépend de Django.

```python
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
import uuid

class UserModel(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=191)
    full_name = models.CharField(max_length=191)
    # ... autres champs ...

    # ... UserManager ...
```

#### 3.2. Le Mapper

**Fichier** : `users/infrastructure/mappers/user_mapper.py`

**Rôle** : Traduire l'objet `User` du domaine en `UserModel` pour la BDD, et vice-versa.

```python
from users.domain.entities.user import User
from users.infrastructure.models.user_model import UserModel

class UserMapper:
    @staticmethod
    def to_entity(user_model: UserModel) -> User:
        # ... logique de conversion ...

    @staticmethod
    def to_model(user_entity: User) -> UserModel:
        # ... logique de conversion ...
```

#### 3.3. Le Repository

**Fichier** : `users/infrastructure/repositories/user_repository.py`

**Rôle** : Implémenter la logique d'accès aux données. Il utilise le `UserModel` de Django et le `UserMapper`.

```python
from users.domain.entities.user import User
from users.infrastructure.models.user_model import UserModel
from users.infrastructure.mappers.user_mapper import UserMapper

class UserRepository:
    def create_user(self, user_entity: User) -> User:
        user_model = UserMapper.to_model(user_entity)
        user_model.set_password(user_entity.password_hash) # Note: set_password vient de l'AbstractBaseUser de Django
        user_model.save()
        return UserMapper.to_entity(user_model)

    def exists_by_email(self, email: str) -> bool:
        return UserModel.objects.filter(email=email).exists()

    # ... autres méthodes ...
```

#### 3.4. L'implémentation du Hasher

**Fichier** : `users/infrastructure/services/django_password_hasher.py`

**Rôle** : Fournir une implémentation concrète de l'interface `PasswordHasher` en utilisant les fonctions de Django.

```python
from django.contrib.auth.hashers import make_password, check_password
from users.application.services.password_hasher import PasswordHasher

class DjangoPasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return make_password(password)

    def verify(self, password_hash: str, password: str) -> bool:
        return check_password(password, password_hash)
```

### Étape 4 : La Présentation (L'API REST)

Enfin, on expose notre cas d'utilisation via une API.

#### 4.1. Le Serializer

**Fichier** : `users/presentation/serializers/auth_serializers.py`

**Rôle** : Valider les données JSON qui arrivent dans la requête HTTP.

```python
from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=191)
    password = serializers.CharField(write_only=True)
```

#### 4.2. La Vue

**Fichier** : `users/presentation/views/auth_view.py`

**Rôle** : Gérer la requête HTTP. Elle utilise le Serializer pour valider les données, puis instancie et appelle `AuthService` avec toutes ses dépendances concrètes. C'est ce qu'on appelle l'**Injection de Dépendances**.

```python
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from users.application.services.auth_service import AuthService
from users.infrastructure.repositories.user_repository import UserRepository
from users.infrastructure.services.django_password_hasher import DjangoPasswordHasher

# C'est ici que l'on assemble nos composants
def get_auth_service():
    user_repository = UserRepository()
    password_hasher = DjangoPasswordHasher()
    return AuthService(user_repository, password_hasher)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            auth_service = get_auth_service()
            user = auth_service.register_user(**serializer.validated_data)
            # ... retourner une réponse succès ...
        except ValueError as e:
            # ... retourner une erreur ...
```

#### 4.3. L'URL

**Fichier** : `users/presentation/urls.py`

**Rôle** : Lier l'URL `/register/` à notre `RegisterView`.

```python
from django.urls import path
from .views.auth_view import RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    # ...
]
```

Et voilà ! Nous avons implémenté une fonctionnalité complète en respectant la séparation des couches. Chaque fichier a un rôle unique et clair.

---

## Guide d'implémentation : Ajout de la création de projet

Ce second tutoriel montre comment ajouter une nouvelle application (`projects`) et sa première fonctionnalité (créer un projet) en suivant le même modèle architectural.

### Étape 1 : Le Domaine (`projects`)

On définit d'abord les concepts métier liés aux projets.

#### 1.1. L'entité `Project`

**Fichier** : `projects/domain/entities/project.py`

**Rôle** : Représenter un projet avec ses propriétés fondamentales.

```python
import uuid
from datetime import datetime

class Project:
    def __init__(self, id, name, description, owner_id, created_at=None, updated_at=None):
        self.id = id or uuid.uuid4()
        self.name = self._validate_name(name)
        self.description = description
        self.owner_id = owner_id
        # ...
```

#### 1.2. L'entité `ProjectMember`

**Fichier** : `projects/domain/entities/project_member.py`

**Rôle** : Représenter la relation entre un utilisateur et un projet, incluant son rôle.

```python
import uuid
from datetime import datetime

class ProjectMember:
    class Role:
        ADMIN = "ADMIN"
        MEMBER = "MEMBER"

    def __init__(self, id, project_id, user_id, role, joined_at=None):
        self.id = id or uuid.uuid4()
        self.project_id = project_id
        self.user_id = user_id
        self.role = self._validate_role(role)
        # ...
```

### Étape 2 : L'Application (`projects`)

On définit le cas d'utilisation "Créer un projet".

**Fichier** : `projects/application/services/project_service.py`

**Rôle** : Orchestrer la création d'un projet. La logique métier est claire : quand un projet est créé, son créateur devient automatiquement un membre avec le rôle "ADMIN".

```python
from projects.domain.entities import Project, ProjectMember
from projects.infrastructure.repositories.project_repository import ProjectRepository
from users.infrastructure.repositories.user_repository import UserRepository

class ProjectService:
    def __init__(self, project_repository: ProjectRepository, user_repository: UserRepository):
        self.project_repository = project_repository
        self.user_repository = user_repository

    def create_project(self, name: str, description: str, owner_id: str) -> Project:
        owner = self.user_repository.get_by_id(owner_id)
        if not owner:
            raise ValueError("Le propriétaire du projet n'existe pas.")

        project = Project(id=None, name=name, description=description, owner_id=owner_id)
        created_project = self.project_repository.create_project(project)

        member = ProjectMember(id=None, project_id=created_project.id, user_id=owner_id, role=ProjectMember.Role.ADMIN)
        self.project_repository.add_member(member)

        return created_project
```

### Étape 3 : L'Infrastructure (`projects`)

On implémente les détails techniques pour la persistance des données.

#### 3.1. Les Modèles Django

**Fichiers** : `projects/infrastructure/models/project_model.py` et `project_member_model.py`

**Rôle** : Définir les tables en base de données avec les relations `ForeignKey` vers `UserModel`.

```python
# project_model.py
class ProjectModel(models.Model):
    # ...
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="owned_projects")
    # ...

# project_member_model.py
class ProjectMemberModel(models.Model):
    # ...
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="project_memberships")
    # ...
```

#### 3.2. Les Mappers et le Repository

**Fichiers** : `projects/infrastructure/mappers/` et `projects/infrastructure/repositories/project_repository.py`

**Rôle** : Le `ProjectRepository` utilise les `Mappers` pour communiquer avec la base de données, fournissant des méthodes comme `create_project` et `add_member` au `ProjectService`.

### Étape 4 : La Présentation (`projects`)

On expose la fonctionnalité via l'API.

#### 4.1. Le Serializer et la Vue

**Fichiers** : `projects/presentation/serializers/project_serializers.py` et `projects/presentation/views/project_views.py`

**Rôle** : La `ProjectCreateView` utilise `IsAuthenticated` pour s'assurer que seul un utilisateur connecté peut créer un projet. Elle valide les données avec `ProjectCreateSerializer` et appelle le `ProjectService` en lui passant l'ID de l'utilisateur (`request.user.id`) comme propriétaire.

#### 4.2. L'intégration

- **`projects/models.py`** est créé pour que Django découvre les modèles.
- **`settings.py`** est mis à jour pour inclure `'projects'` dans `INSTALLED_APPS`.
- **`core/urls.py`** est mis à jour pour inclure les URLs de `projects` sous `/api/projects/`.
- Les migrations sont créées (`makemigrations`) et appliquées (`migrate`).
