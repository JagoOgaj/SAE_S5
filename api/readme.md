
# Guide de Configuration et d'Utilisation de l'API de Prédiction de Genre avec FastAPI

Ce guide vous aide à configurer et utiliser l'API de prédiction de genre avec FastAPI et Redis pour la gestion de quotas.

## Prérequis

- Docker et Docker Compose doivent être installés sur votre machine.

## Guide d'Installation

### Étape 1 : Cloner le Répertoire

Clonez le répertoire du projet sur votre machine locale.

```bash
git clone <URL_du_répertoire>
cd <dossier_du_projet>
```

### Étape 2 : Ajouter le Fichier du Modèle

Assurez-vous que votre fichier de modèle TensorFlow nommé `model.h5` se trouve dans le dossier racine du projet.

### Étape 3 : Configuration de l'Environnement

- L'API utilise Docker et Docker Compose pour exécuter FastAPI et Redis.
- Les fichiers nécessaires incluent :
  - `Dockerfile` pour le conteneur de l'API.
  - `docker-compose.yml` pour configurer Redis et l'API.

### Étape 4 : Construire et Démarrer les Conteneurs

Utilisez Docker Compose pour construire et démarrer les conteneurs.

```bash
docker-compose up --build
```

Cette commande construira les conteneurs FastAPI et Redis et démarrera l'API à `http://localhost:8000`.

## Utilisation de l'API

### Authentification

- L'API utilise une authentification basique.
- Identifiants par défaut pour les prédictions : `nom_utilisateur: pinpin`, `mot_de_passe: azerty`
- Identifiants administrateur pour la gestion des quotas : `nom_utilisateur: admin`, `mot_de_passe: admin_password`

### Endpoints

1. **Prédiction du Genre depuis une Image**

   - Endpoint : `/predict/`
   - Méthode : `POST`
   - Auth : Authentification basique (nom_utilisateur: pinpin, mot_de_passe: azerty)
   - Paramètres :
     - `file` (requis) : Fichier image à envoyer.
   - Exemple de commande `cURL` :

     ```bash
     curl -X POST "http://localhost:8000/predict/" -u "pinpin:azerty" -F "file=@/chemin/vers/votre/image.jpg"
     ```

2. **Obtenir les Quotas de Tous les Utilisateurs (Admin)**

   - Endpoint : `/users/quotas/`
   - Méthode : `GET`
   - Auth : Authentification basique (nom_utilisateur: admin, mot_de_passe: admin_password)
   - Exemple de commande `cURL` :

     ```bash
     curl -X GET "http://localhost:8000/users/quotas/" -u "admin:admin_password"
     ```

3. **Obtenir le Quota d’un Utilisateur Spécifique (Admin)**

   - Endpoint : `/user/{username}/quota`
   - Méthode : `GET`
   - Auth : Authentification basique (nom_utilisateur: admin, mot_de_passe: admin_password)
   - Paramètres : 
     - `username` : Le nom d'utilisateur dont vous voulez vérifier le quota.
   - Exemple de commande `cURL` :

     ```bash
     curl -X GET "http://localhost:8000/user/pinpin/quota" -u "admin:admin_password"
     ```

4. **Réinitialiser le Quota d'un Utilisateur (Admin)**

   - Endpoint : `/user/{username}/reset_quota`
   - Méthode : `POST`
   - Auth : Authentification basique (nom_utilisateur: admin, mot_de_passe: admin_password)
   - Paramètres : 
     - `username` : Le nom d'utilisateur dont vous voulez réinitialiser le quota.
   - Exemple de commande `cURL` :

     ```bash
     curl -X POST "http://localhost:8000/user/pinpin/reset_quota" -u "admin:admin_password"
     ```

## Remarques

- **Gestion des Quotas** : Chaque utilisateur dispose d'une limite quotidienne de 50 requêtes, gérée par Redis.
- **Format de l'Image** : Assurez-vous que le fichier image est dans un format compatible (par ex., JPG ou PNG).

## Dépannage

- Si vous rencontrez des problèmes avec les avertissements de mémoire de Redis, vous pouvez ajuster la configuration d'overcommit de mémoire sur votre système hôte :
  ```bash
  sudo sysctl vm.overcommit_memory=1
  ```

Cette API vous permet de classifier le genre en fonction des images avec une gestion de quota pour chaque utilisateur. 
