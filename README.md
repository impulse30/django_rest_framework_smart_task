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
