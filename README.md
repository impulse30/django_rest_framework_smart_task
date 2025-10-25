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
-   **Implémentation Django** : Les `models.py`. Ils définissent la structure des données et les validations de base. Cette couche ne doit dépendre de rien d'autre.

#### 2. Application (Use Cases / Services)
-   **Rôle** : Orchestre le flux de données et exécute les cas d'utilisation (logique applicative). C'est ici que se trouve la logique métier spécifique à une action (ex: "créer un utilisateur", "calculer le total d'une commande").
-   **Implémentation Django** : Des fichiers `services.py` ou `use_cases.py`. Ces fichiers contiennent des fonctions ou des classes qui prennent des données simples en entrée (dictionnaires, etc.), appliquent la logique, et interagissent avec la couche Domaine via les Repositories. **Cette couche ne connaît ni HTTP, ni Django REST Framework.**

#### 3. Présentation (API / Framework)
-   **Rôle** : Gère tout ce qui est lié à l'interface externe (dans notre cas, une API REST). Elle reçoit les requêtes HTTP, valide les données entrantes, et renvoie des réponses formatées (JSON).
-   **Implémentation Django** : Les `views.py` (ViewSets, APIViews), `serializers.py` et `urls.py` de Django REST Framework. Le rôle de cette couche est de traduire les requêtes HTTP en appels à la couche Application et de formater les résultats pour le client. **Elle ne doit contenir aucune logique métier.**

#### 4. Infrastructure (Frameworks & Drivers)
-   **Rôle** : Contient tout ce qui est externe à l'application : la base de données, les services externes (APIs tierces), le cache, etc.
-   **Implémentation Django** : Cette couche est souvent matérialisée par le **Repository Pattern**. On crée des fichiers `repositories.py` qui abstraient l'accès à la base de données. Par exemple, au lieu d'appeler `User.objects.create()` directement dans la couche Application, on appellerait `user_repository.create_user()`. Cela permet de découpler la logique métier de l'ORM de Django.

### Exemple d'un flux de requête

Imaginons une requête `POST /api/users/` pour créer un nouvel utilisateur :

1.  **Présentation (API)**
    -   `urls.py` dirige la requête vers `UserCreateAPIView`.
    -   `UserCreateAPIView` utilise `UserSerializer` pour valider les données JSON reçues (`request.data`).
    -   Si la validation réussit, la vue n'enregistre pas l'utilisateur directement. Elle appelle une fonction de la couche Application :
        ```python
        # views.py
        user_data = serializer.validated_data
        user = create_user_service(user_data) # Appel à la couche Application
        ```

2.  **Application (Service)**
    -   La fonction `create_user_service` dans `services.py` reçoit les données validées.
    -   Elle exécute la logique métier : peut-être vérifier si l'email n'est pas sur une liste noire, préparer des données par défaut, etc.
    -   Elle appelle ensuite la couche Infrastructure (Repository) pour persister les données :
        ```python
        # services.py
        def create_user_service(user_data):
            # ... logique métier ...
            new_user = user_repository.create(**user_data)
            # ... autre logique (ex: envoyer un email de bienvenue) ...
            return new_user
        ```

3.  **Infrastructure (Repository)**
    -   Le `user_repository` dans `repositories.py` contient la logique d'accès à la base de données, qui est spécifique à l'ORM de Django.
        ```python
        # repositories.py
        from .models import User

        class UserRepository:
            def create(self, **user_data):
                return User.objects.create_user(**user_data)
        ```

4.  **Domaine (Model)**
    -   L'ORM de Django utilise le modèle `User` (`models.py`) pour créer l'enregistrement en base de données, en respectant les contraintes définies dans le modèle.

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
