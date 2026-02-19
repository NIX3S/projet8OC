```markdown
# CréditRisk ML API

![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green)
![Docker](https://img.shields.io/badge/Docker-20.10-blue)
![Coverage](https://img.shields.io/badge/coverage-92%25-yellow)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

API **FastAPI** pour prédire le risque de crédit, intégrant un modèle Machine Learning, avec pipeline CI/CD et déploiement via **Docker**.

---

## Table of Contents

- [About The Project](#about-the-project)
- [Project Structure](#project-structure)
- [Built With](#built-with)
- [CI/CD Pipeline](#cicd-pipeline)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Docker](#docker)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Testing](#testing)
- [Deployment](#deployment)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## About The Project

CréditRisk ML API est une API développée avec **FastAPI**, intégrant un modèle Machine Learning pour prédire le risque de défaut de crédit.

Fonctionnalités clés :

- Endpoint `/predict` pour prédire le risque de défaut  
- Validation des entrées avec **Pydantic**  
- Gestion des erreurs et types invalides  
- Tests automatisés avec **Pytest** et couverture  
- Dockerisation complète pour déploiement rapide  
- Chargement d’un modèle `.joblib` pour les prédictions  

---

## Project Structure

```

├── app/
│   ├── main.py
│   ├── exceptions.py
│   ├── api/
│   │   └── endpoints.py
│   ├── model/
│   │   └── credit_model.joblib
│   └── services/
│       └── prediction.py
├── tests/
│   ├── test_api.py
│   ├── test_endpoints.py
│   ├── test_predict.py
│   └── test_prediction.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .github/workflows/ci.yml

```

### Modèle Machine Learning

Le modèle est stocké localement dans :

```

app/model/credit_model.joblib

````

---

## Built With

- Python 3.12  
- FastAPI  
- Pytest  
- Docker & Docker Compose  
- Uvicorn  
- Pydantic  

---

## CI/CD Pipeline

Le pipeline GitHub Actions se déclenche sur :

- `push` vers `main`  
- `push` vers `feature/*`

### Étapes automatisées :

1. Construction et test du conteneur Docker  
2. Installation des dépendances Python  
3. Exécution des tests avec couverture  
4. Déploiement automatique du conteneur si tests réussis  

---

## Getting Started

### Prerequisites

- Python 3.12+  
- Docker & Docker Compose  
- Git  

Mettre à jour pip :

```bash
python -m pip install --upgrade pip
````

---

### Installation

1. Cloner le repository

```bash
git clone <URL_DU_DEPOT>
cd <NOM_DU_PROJET>
```

2. Installer les dépendances (optionnel si Docker)

```bash
pip install -r requirements.txt
```

---

### Docker

Construire et lancer le projet avec Docker Compose :

```bash
# Pull des dernières modifications
git pull origin main

# Construire et démarrer le conteneur
docker-compose up --build --force-recreate
```

API disponible sur : `http://127.0.0.1:8000`

---

## Environment Variables

Créer un fichier `.env` à la racine du projet (exemple) :

```env
MODEL_PATH=app/model/credit_model.joblib
PORT=8000
```

---

## Usage

Lancer le serveur FastAPI (local ou Docker) :

```bash
uvicorn app.main:app --reload
```

Documentation interactive Swagger :

```
http://127.0.0.1:8000/docs
```

Endpoint `/predict` :

* **POST**
* Body JSON : données client
* Retour : score de risque entre 0 et 1

Exemple :

```json
{
  "AMT_ANNUITY": 1000.0,
  "AMT_CREDIT": 50000.0,
  "CNT_CHILDREN": 2,
  "DAYS_BIRTH": -10000,
  "AMT_INSTALMENT_max": 2000
}
```

Réponse :

```json
{
  "prediction": 0.85
}
```

---

## Testing

Exécuter les tests :

```bash
pytest --cov=app tests/
```

Les tests couvrent :

* API
* Endpoints
* Service de prédiction
* Validation des entrées

---

## Deployment

Déploiement via Docker sur n’importe quel serveur ou cloud supportant Docker.

Étapes principales :

1. Pull du dépôt
2. Construire le conteneur Docker
3. Lancer avec Docker Compose
4. L’API est exposée sur le port configuré (`PORT`)

---

## Roadmap

* Authentification JWT
* Monitoring et alerting
* Documentation OpenAPI avancée
* CI/CD complet pour mise en production automatique

---

## Contributing

```bash
git checkout -b feature/NouvelleFeature
git commit -m "Ajout de NouvelleFeature"
git push origin feature/NouvelleFeature
```

Ouvrir ensuite une Pull Request.

---

## License

Distribué sous licence MIT.

---

## Contact

Ton Nom
GitHub: [https://github.com/tonusername](https://github.com/tonusername)
Project Link: [https://github.com/tonusername/nom_projet](https://github.com/tonusername/nom_projet)

```

---

