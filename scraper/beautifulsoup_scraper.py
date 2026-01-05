"""
Module de scraping pour CoinAfrique avec BeautifulSoup
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from typing import List, Dict
import sys
import os

# Ajouter le chemin parent pour importer data_cleaner
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_cleaner import clean_beautifulsoup_data



# Catégories disponibles sur CoinAfrique
CATEGORIES = {
    "chiens": "https://sn.coinafrique.com/categorie/chiens",
    "moutons": "https://sn.coinafrique.com/categorie/moutons",
    "poules-lapins-et-pigeons": "https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons",
    "autres-animaux": "https://sn.coinafrique.com/categorie/autres-animaux"
}


def get_headers() -> Dict[str, str]:
    """
    Retourne des headers HTTP pour simuler un navigateur
    """
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]

    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'DNT': '1'
    }


def scrape_page(url: str, detail_delay: tuple = (1, 3)) -> List[Dict]:
    """
    Scrape une seule page de CoinAfrique avec extraction détaillée

    Cette fonction utilise une approche en deux étapes:
    1. Récupère les conteneurs d'annonces de la page de liste
    2. Scrape chaque page de détail individuellement pour des données précises

    Args:
        url: URL de la page à scraper
        detail_delay: Tuple (min, max) pour délai aléatoire entre pages de détail

    Returns:
        Liste de dictionnaires contenant les données scrapées (nom, prix, adresse, image_lien)
    """
    try:
        # Faire la requête HTTP pour la page de liste
        print(f"\n[SCRAPER] Requête: {url}")
        response = requests.get(url, headers=get_headers(), timeout=10)
        response.raise_for_status()
        print(f"[SCRAPER] Statut: {response.status_code}")

        # Parser le HTML de la page de liste
        soup = BeautifulSoup(response.content, 'html.parser')

        # Trouver tous les conteneurs d'annonces (approche spécifique Material Design)
        containers = soup.find_all('div', 'col s6 m4 l3')
        print(f"[SCRAPER] Conteneurs trouvés: {len(containers)}")

        if not containers:
            print("[SCRAPER] Aucun conteneur trouvé!")
            return []  # Aucun conteneur trouvé

        data = []

        for idx, container in enumerate(containers, 1):
            print(f"\n[SCRAPER] Traitement conteneur {idx}/{len(containers)}")
            try:
                # ÉTAPE 1: Extraire les informations de base depuis le conteneur
                link_tag = container.find('a')
                if not link_tag or 'href' not in link_tag.attrs:
                    continue

                # Construire l'URL de la page de détail
                url_container = 'https://sn.coinafrique.com' + link_tag['href']

                # Extraire l'image depuis la page de liste
                img_tag = container.find('img')
                image_lien = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None

                # Délai aléatoire avant de requêter la page de détail
                sleep_time = random.uniform(detail_delay[0], detail_delay[1])
                time.sleep(sleep_time)

                # ÉTAPE 2: Scraper la page de détail
                try:
                    detail_response = requests.get(url_container, headers=get_headers(), timeout=10)
                    detail_response.raise_for_status()
                    soup_container = BeautifulSoup(detail_response.content, 'html.parser')

                    # Extraire les données avec des sélecteurs CSS spécifiques
                    # Nom
                    nom_tag = soup_container.find('h1', 'title title-ad hide-on-large-and-down')
                    nom = nom_tag.text.strip() if nom_tag else None

                    # Prix
                    prix_tag = soup_container.find('p', 'price')
                    prix_text = prix_tag.text.strip() if prix_tag else None

                    # Adresse depuis l'attribut data-address
                    address_span = soup_container.find("span", attrs={"data-address": True})
                    adresse_text = address_span["data-address"] if address_span else None

                    # Ne conserver que si on a au moins un nom
                    if nom:
                        print(f"[SCRAPER]   Nom: {nom[:50]}...")
                        print(f"[SCRAPER]   Prix: {prix_text if prix_text else 'Non spécifié'}")
                        print(f"[SCRAPER]   Adresse: {adresse_text if adresse_text else 'Non spécifiée'}")

                        item = {
                            'nom': nom,
                            'prix': prix_text,
                            'adresse': adresse_text,
                            'image_lien': image_lien
                        }

                        data.append(item)
                        print(f"[SCRAPER]   Item ajouté! Total: {len(data)}")

                except Exception:
                    # Erreur silencieuse pour les pages de détail individuelles
                    pass

            except Exception:
                # Erreur silencieuse pour les conteneurs individuels
                pass

        print(f"\n[SCRAPER] Résumé: {len(data)} items récupérés sur cette page")
        return data

    except requests.exceptions.RequestException as e:
        print(f"[SCRAPER] ERREUR HTTP: {str(e)}")
        raise Exception(f"Erreur lors de la requête HTTP: {str(e)}")
    except Exception as e:
        print(f"[SCRAPER] ERREUR: {str(e)}")
        raise Exception(f"Erreur lors du scraping: {str(e)}")


def scrape_category(category: str, num_pages: int = 1, delay: tuple = (1, 3)) -> pd.DataFrame:
    """
    Scrape plusieurs pages d'une catégorie

    Args:
        category: Nom de la catégorie (ex: "chiens")
        num_pages: Nombre de pages à scraper
        delay: Tuple (min, max) pour délai aléatoire entre requêtes en secondes

    Returns:
        DataFrame pandas avec toutes les données scrapées
    """
    if category not in CATEGORIES:
        raise ValueError(f"Catégorie '{category}' non valide. Choisir parmi: {list(CATEGORIES.keys())}")

    base_url = CATEGORIES[category]
    all_data = []

    print(f"\n{'='*60}")
    print(f"[SCRAPER] Début scraping catégorie: {category}")
    print(f"[SCRAPER] Nombre de pages: {num_pages}")
    print(f"{'='*60}")

    for page_num in range(1, num_pages + 1):
        print(f"\n[SCRAPER] === PAGE {page_num}/{num_pages} ===")

        # Construire l'URL avec pagination
        if page_num == 1:
            url = base_url
        else:
            url = f"{base_url}?page={page_num}"

        # Scraper la page (avec délai pour les pages de détail)
        page_data = scrape_page(url, detail_delay=(1, 3))
        all_data.extend(page_data)

        # Délai aléatoire entre les requêtes (sauf pour la dernière page)
        if page_num < num_pages:
            sleep_time = random.uniform(delay[0], delay[1])
            print(f"[SCRAPER] Attente de {sleep_time:.1f}s avant la page suivante...")
            time.sleep(sleep_time)

    # Créer un DataFrame
    df = pd.DataFrame(all_data)

    print(f"\n{'='*60}")
    print(f"[SCRAPER] Scraping terminé: {len(df)} items bruts récupérés")
    print(f"{'='*60}")

    # Nettoyer les données
    df = clean_beautifulsoup_data(df)

    print(f"\n{'='*60}")
    print(f"[SCRAPER] TERMINÉ!")
    print(f"[SCRAPER] Total final après nettoyage: {len(df)} items")
    print(f"{'='*60}\n")

    return df





def save_to_csv(df: pd.DataFrame, filename: str) -> str:
    """
    Sauvegarde le DataFrame en CSV

    Args:
        df: DataFrame à sauvegarder
        filename: Nom du fichier (sans extension)

    Returns:
        Chemin complet du fichier sauvegardé
    """
    if df.empty:
        raise ValueError("Le DataFrame est vide, rien à sauvegarder")

    filepath = f"data/scraped/{filename}.csv"
    df.to_csv(filepath, index=False, encoding='utf-8')

    return filepath
