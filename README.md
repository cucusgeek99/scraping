# CoinAfrique Scraper & Analytics

Application Streamlit pour scraper et analyser les annonces d'animaux sur CoinAfrique Sénégal.

## Description

Cette application permet de:
- **Scraper** les annonces directement depuis CoinAfrique avec BeautifulSoup
- **Uploader** et nettoyer des données exportées depuis WebScraper
- **Visualiser** les données avec des dashboards interactifs
- **Analyser** les tendances de prix et la répartition géographique

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

### Modules disponibles

#### 1. Scraper avec BeautifulSoup
- Sélectionnez une catégorie (chiens, moutons, poules/lapins/pigeons, autres animaux)
- Définissez le nombre de pages à scraper (1-20)
- Lancez le scraping
- Téléchargez les données en CSV

#### 2. Télécharger données WebScraper
- Uploadez un fichier CSV exporté depuis WebScraper
- Visualisez les données
- Consultez les statistiques basiques
- Téléchargez les données

#### 3. Dashboard
- Visualisez les données avec des graphiques interactifs
- Filtrez par catégorie, ville, et fourchette de prix
- Analysez:
  - Distribution des prix
  - Répartition géographique
  - Analyse par catégorie
  - Tendances temporelles

#### 4. Évaluation
- Accédez aux formulaires d'évaluation (Kobo ou Google Forms)

## Structure du projet

```
Coinafrique_App/
├── app.py                          # Application principale
├── scraper/
│   ├── __init__.py
│   └── beautifulsoup_scraper.py    # Module de scraping
├── utils/
│   ├── __init__.py
│   ├── data_cleaner.py             # Nettoyage des données
│   └── visualizations.py           # Fonctions de visualisation
├── data/
│   ├── scraped/                    # Données scrapées (nettoyées)
│   └── webscraper/                 # Données WebScraper (uploadées)
├── .streamlit/
│   └── config.toml                 # Configuration Streamlit
├── requirements.txt                # Dépendances Python
└── README.md                       # Ce fichier
```

## Fonctionnalités

### Scraping avec BeautifulSoup
- Scraping multi-pages avec BeautifulSoup
- Extraction automatique de: nom, prix, adresse, image
- Nettoyage automatique des données scrapées
- Normalisation des prix (extraction numérique)
- Extraction des informations de localisation (quartier, ville, pays)
- Suppression des doublons
- Gestion des erreurs et délais entre requêtes
- Sauvegarde automatique en CSV

### Upload de données WebScraper
- Upload de fichiers CSV exportés depuis WebScraper
- Visualisation des données uploadées
- Statistiques basiques (nombre d'annonces, colonnes, etc.)
- Téléchargement des données

### Visualisations
- Histogrammes de distribution des prix
- Box plots pour comparaison entre catégories
- Graphiques de répartition géographique
- Pie charts d'analyse par catégorie
- Graphiques de tendances temporelles
- KPIs et statistiques descriptives

## Catégories disponibles

1. **Chiens** (`/categorie/chiens`)
2. **Moutons** (`/categorie/moutons`)
3. **Poules, Lapins et Pigeons** (`/categorie/poules-lapins-et-pigeons`)
4. **Autres Animaux** (`/categorie/autres-animaux`)

## Configuration

### Nombre de pages
Utilisez le slider dans la sidebar pour définir le nombre de pages à scraper (1-20).

### Thème
Le thème peut être personnalisé dans `.streamlit/config.toml`:
```toml
[theme]
primaryColor="#FF6B35"
backgroundColor="#F7F7F7"
secondaryBackgroundColor="#E8F4F8"
textColor="#262730"
font="sans serif"
```

## Technologies utilisées

- **Streamlit**: Interface utilisateur
- **BeautifulSoup4**: Web scraping
- **Pandas**: Manipulation de données
- **Plotly**: Visualisations interactives
- **Matplotlib/Seaborn**: Graphiques statiques
- **Requests**: Requêtes HTTP

## Notes importantes

### Scraping responsable
- L'application utilise des délais aléatoires entre les requêtes (1-3 secondes)
- User-Agent personnalisé pour simuler un navigateur
- Gestion des erreurs réseau et timeouts

### Limitations
- Le site CoinAfrique peut utiliser du JavaScript pour le rendu
- Respectez les conditions d'utilisation du site

## Dépannage

### Le scraping ne fonctionne pas
- Vérifiez votre connexion internet
- Réduisez le nombre de pages
- Le site peut avoir changé sa structure HTML

### Erreur lors de l'upload
- Vérifiez que le fichier est bien au format CSV
- Assurez-vous que les colonnes requises sont présentes (nom, prix, adresse, image_lien)

### Les graphiques ne s'affichent pas
- Assurez-vous que les données contiennent les colonnes nécessaires
- Vérifiez qu'il y a suffisamment de données pour générer les graphiques

## Support

Pour toute question ou suggestion, veuillez ouvrir une issue sur le dépôt du projet.

## Licence

Ce projet est à usage éducatif et de démonstration.

## Contributeurs

Développé dans le cadre du Projet 3 - CoinAfrique Scraper

---

**Bon scraping!**
# scraping
