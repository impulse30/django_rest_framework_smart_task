# Guide de Configuration et d'Architecture du Projet Django

Ce document sert de guide complet pour l'installation, la configuration et la compréhension de l'architecture de ce projet Django.

## Table des matières
1. [Gestion de l'Environnement](#1-gestion-de-lenvironnement)
2. [Configuration de Django](#2-configuration-de-django)
3. [Architecture du Projet](#3-architecture-du-projet)
4. [Workflow de Démarrage Rapide](#4-workflow-de-démarrage-rapide)
5. [Fonctionnalités de l'API](#5-fonctionnalités-de-lapi)
6. [Guide d'implémentation : Ajouter une fonctionnalité](#6-guide-dimplémentation--ajouter-une-fonctionnalité)

---

## 1. Gestion de l'Environnement
... (contenu inchangé)

---

## 2. Configuration de Django
... (contenu inchangé)

---

## 3. Architecture du Projet

Pour garantir scalabilité et maintenabilité, ce projet adopte une architecture inspirée de la **Clean Architecture**, adaptée à l'écosystème Django. L'idée maîtresse est une **séparation stricte des responsabilités** entre la couche de données et les couches fonctionnelles.

### La Structure en Applications

Le projet est divisé en deux types d'applications Django :

1.  **Une Application de Données (`data`)**
    *   **Rôle** : C'est le **cœur de la base de données**. Cette application a la responsabilité unique de définir tous les modèles de données Django (`models.py`) et de contenir toutes les migrations.
    *   **Dépendances** : Elle ne dépend d'**aucune autre application** du projet.

2.  **Des Applications Fonctionnelles (`users`, `projects`, `tasks`, etc.)**
    *   **Rôle** : Chaque application représente une **unité logique de fonctionnalités** (un domaine métier). Elle contient toute la logique pour une fonctionnalité donnée.
    *   **Dépendances** : Elles peuvent dépendre de l'application `data` pour accéder aux modèles, mais **jamais les unes des autres**.

### L'Architecture Interne d'une Application Fonctionnelle

Chaque application fonctionnelle (ex: `users`) est elle-même divisée en 4 couches :

#### 1. `domain/` (Logique Métier Pure)
- **Rôle** : Contient les **entités** métier (ex: une classe `User` simple) qui sont indépendantes de tout framework.

#### 2. `application/` (Cas d'Utilisation)
- **Rôle** : Orchestre les actions. Contient les **services applicatifs** (ex: `AuthService`) et les **interfaces** pour les dépendances externes (ex: `ITokenService`).

#### 3. `infrastructure/` (Détails Techniques)
- **Rôle** : Contient le code qui implémente les détails techniques.
- **Contenu** :
    - `repositories/` : Le **Repository Pattern**, qui abstrait l'accès à la base de données.
    - `mappers/` : Les classes qui convertissent les entités du `domain` en modèles de `data`.
    - `services/` : Les **implémentations concrètes** des interfaces définies dans la couche `application` (ex: `JWTTokenService`).

#### 4. `presentation/` (Interface API)
- **Rôle** : Gère les requêtes HTTP et expose l'application au monde extérieur.

### Le Flux d'une Requête (Exemple: Login)

1.  Une requête `POST /api/users/login/` arrive à la `LoginView` (`presentation`).
2.  La vue valide les données et appelle l'`AuthService` (`application`).
3.  L'`AuthService` demande au `UserRepository` (`infrastructure`) de trouver l'utilisateur.
4.  Le `UserRepository` importe le `UserModel` de `data` et fait la requête en base de données.
5.  Une fois l'utilisateur validé, l'`AuthService` appelle la méthode `generate_tokens` de son `ITokenService` (`application`).
6.  L'implémentation concrète, `JWTTokenService` (`infrastructure`), est exécutée. Elle récupère le `UserModel` de `data` et génère un token JWT.
7.  Le flux remonte les couches jusqu'à la vue qui renvoie le token à l'utilisateur.

---

## 4. Workflow de Démarrage Rapide
... (contenu inchangé)

---

## 5. Fonctionnalités de l'API
... (contenu inchangé)

---

## 6. Guide d'implémentation : Ajouter une fonctionnalité (Exemple: les Tâches)
... (contenu inchangé)
