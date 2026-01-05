# Data Scraper

Application Streamlit pour scraper et analyser les annonces d'animaux sur CoinAfrique Sénégal.

## Description

Cette application permet de:
- **Scraper** les annonces directement depuis CoinAfrique avec BeautifulSoup
- **Afficher** et telecharger des données exportées depuis WebScraper
- **Visualiser** les données avec des dashboards interactifs
- **Evaluer** l'application avec un formulaire kobo et google form

## Installation

### Prérequis
- Python 3.8 ou supérieur
- pip

### Étapes d'installation

1. Cloner ou télécharger le projet

2. Créer un environnement virtuel (recommandé):
```bash
python -m venv .venv
source .venv/bin/activate  # Sur Mac/Linux
# ou
.venv\Scripts\activate  # Sur Windows
```

3. Installer les dépendances:
```bash
pip install -r requirements.txt
```

## Utilisation

### Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvrira dans votre navigateur par défaut à l'adresse `http://localhost:8501`


