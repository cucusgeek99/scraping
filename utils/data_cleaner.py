"""
Module de nettoyage des données
"""

import pandas as pd
import re
from typing import Optional



# ============================================================================
# FONCTION Utilisée pour nettoyer les données BeautifulSoup
# ============================================================================


def clean_beautifulsoup_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie les données scrapées par BeautifulSoup

    Args:
        df: DataFrame brut avec colonnes: nom, prix, adresse, image_lien

    Returns:
        DataFrame nettoyé
    """
    if df.empty:
        return df

    # Créer une copie pour ne pas modifier l'original
    df_clean = df.copy()
    initial_count = len(df_clean)

    print(f"\n[NETTOYAGE] Début du nettoyage de {initial_count} annonces")

    # 1. Supprimer les lignes où le nom est vide
    if 'nom' in df_clean.columns:
        df_clean = df_clean[df_clean['nom'].notna() & (df_clean['nom'].str.len() > 0)]
        removed = initial_count - len(df_clean)
        if removed > 0:
            print(f"[NETTOYAGE] {removed} lignes sans nom supprimées")

    # 2. Supprimer les lignes "Prix sur demande"
    if 'prix' in df_clean.columns:
        before = len(df_clean)
        keywords = ['demande', 'négociable', 'contacter', 'appeler']
        mask = df_clean['prix'].astype(str).str.lower().apply(
            lambda x: not any(keyword in x for keyword in keywords)
        )
        df_clean = df_clean[mask]
        removed = before - len(df_clean)
        if removed > 0:
            print(f"[NETTOYAGE] {removed} lignes 'Prix sur demande' supprimées")

    # 3. Supprimer les prix aberrants (< moyenne/2)
    if 'prix' in df_clean.columns and len(df_clean) > 0:
        before = len(df_clean)

        # Convertir les prix en numérique temporairement
        df_clean['prix_num'] = df_clean['prix'].astype(str).str.replace(' ', '').str.replace('CFA', '').apply(
            lambda x: float(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else None
        )

        # Calculer la moyenne des prix valides
        prix_valides = df_clean['prix_num'].dropna()
        if len(prix_valides) > 0:
            prix_moyen = prix_valides.mean()
            seuil = prix_moyen / 2

            print(f"[NETTOYAGE] Prix moyen: {prix_moyen:,.0f} FCFA, Seuil: {seuil:,.0f} FCFA")

            # Supprimer les lignes avec prix aberrant
            df_clean = df_clean[
                (df_clean['prix_num'].isna()) | (df_clean['prix_num'] >= seuil)
            ]

            removed = before - len(df_clean)
            if removed > 0:
                print(f"[NETTOYAGE] {removed} lignes avec prix aberrant supprimées")

        # Supprimer la colonne temporaire
        df_clean = df_clean.drop('prix_num', axis=1)

    # 4. Gérer les doublons de noms en ajoutant des suffixes
    if 'nom' in df_clean.columns:
        nom_counts = {}
        new_noms = []

        for nom in df_clean['nom']:
            if nom in nom_counts:
                nom_counts[nom] += 1
                new_noms.append(f"{nom} {nom_counts[nom]}")
            else:
                nom_counts[nom] = 0
                new_noms.append(nom)

        df_clean['nom'] = new_noms

        duplicates_fixed = sum(1 for count in nom_counts.values() if count > 0)
        if duplicates_fixed > 0:
            print(f"[NETTOYAGE] {duplicates_fixed} noms dupliqués avec suffixes ajoutés")

    # 5. Garder uniquement les 4 colonnes requises
    columns_to_keep = ['nom', 'prix', 'adresse', 'image_lien']
    df_clean = df_clean[[col for col in columns_to_keep if col in df_clean.columns]]

    # Réinitialiser l'index
    df_clean = df_clean.reset_index(drop=True)

    final_count = len(df_clean)
    total_removed = initial_count - final_count
    print(f"[NETTOYAGE] Terminé: {final_count} annonces conservées ({total_removed} supprimées)\n")

    return df_clean
