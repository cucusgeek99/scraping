"""
Module de visualisations pour le dashboard CoinAfrique
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional


def _clean_price_column(df: pd.DataFrame, price_col: str = 'prix') -> pd.DataFrame:
    """
    Nettoie la colonne prix en enlevant les espaces et "CFA" puis convertit en numérique

    Args:
        df: DataFrame avec une colonne prix
        price_col: Nom de la colonne prix

    Returns:
        DataFrame avec prix nettoyé et converti
    """
    df_clean = df.copy()
    df_clean[price_col] = df_clean[price_col].astype(str).str.replace(' ', '').str.replace('CFA', '')
    df_clean[price_col] = pd.to_numeric(df_clean[price_col], errors='coerce')
    return df_clean


def plot_price_distribution(df: pd.DataFrame, category: Optional[str] = None) -> go.Figure:
    """
    Créé un histogramme de distribution des prix

    Args:
        df: DataFrame avec les données
        category: Filtre optionnel par catégorie

    Returns:
        Figure Plotly
    """
    # Filtrer par catégorie si spécifié
    if category and 'categorie' in df.columns:
        df = df[df['categorie'] == category]

    # Convertir les prix en numérique et filtrer les prix valides
    df_copy = _clean_price_column(df)
    df_prices = df_copy[df_copy['prix'].notna() & (df_copy['prix'] > 0)]

    if df_prices.empty:
        # Retourner un graphique vide avec message
        fig = go.Figure()
        fig.add_annotation(
            text="Aucune donnée de prix disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig

    # Créer l'histogramme
    fig = px.histogram(
        df_prices,
        x='prix',
        nbins=30,
        title='Distribution des prix',
        labels={'prix': 'Prix (FCFA)', 'count': 'Nombre d\'annonces'},
        color_discrete_sequence=['#FF6B35']
    )

    fig.update_layout(
        xaxis_title="Prix (FCFA)",
        yaxis_title="Nombre d'annonces",
        showlegend=False
    )

    return fig


def plot_price_boxplot(df: pd.DataFrame) -> go.Figure:
    """
    Créé un box plot des prix par catégorie

    Args:
        df: DataFrame avec les données

    Returns:
        Figure Plotly
    """
    # Convertir les prix en numérique et filtrer les prix valides
    df_copy = _clean_price_column(df)
    df_prices = df_copy[df_copy['prix'].notna() & (df_copy['prix'] > 0)]

    if df_prices.empty or 'categorie' not in df_prices.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucune donnée disponible pour la comparaison",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig

    # Créer le box plot
    fig = px.box(
        df_prices,
        x='categorie',
        y='prix',
        title='Comparaison des prix par catégorie',
        labels={'prix': 'Prix (FCFA)', 'categorie': 'Catégorie'},
        color='categorie'
    )

    fig.update_layout(
        xaxis_title="Catégorie",
        yaxis_title="Prix (FCFA)",
        showlegend=False
    )

    return fig


def plot_geographic_distribution(df: pd.DataFrame) -> go.Figure:
    """
    Créé un graphique en barres de la répartition géographique

    Args:
        df: DataFrame avec les données

    Returns:
        Figure Plotly
    """
    if 'ville' not in df.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucune donnée de localisation disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig

    # Compter les annonces par ville
    ville_counts = df['ville'].value_counts().head(10)

    if ville_counts.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucune donnée de ville disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig

    # Créer le graphique en barres
    fig = px.bar(
        x=ville_counts.index,
        y=ville_counts.values,
        title='Top 10 des villes avec le plus d\'annonces',
        labels={'x': 'Ville', 'y': 'Nombre d\'annonces'},
        color=ville_counts.values,
        color_continuous_scale='Oranges'
    )

    fig.update_layout(
        xaxis_title="Ville",
        yaxis_title="Nombre d'annonces",
        showlegend=False
    )

    return fig


def plot_category_analysis(df: pd.DataFrame) -> go.Figure:
    """
    Créé un pie chart de la répartition par catégorie

    Args:
        df: DataFrame avec les données

    Returns:
        Figure Plotly
    """
    if 'categorie' not in df.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucune donnée de catégorie disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig

    # Compter les annonces par catégorie
    category_counts = df['categorie'].value_counts()

    if category_counts.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucune donnée de catégorie disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig

    # Créer le pie chart
    fig = px.pie(
        values=category_counts.values,
        names=category_counts.index,
        title='Répartition des annonces par catégorie',
        color_discrete_sequence=px.colors.sequential.RdBu
    )

    return fig


def plot_average_price_by_category(df: pd.DataFrame) -> go.Figure:
    """
    Créé un graphique en barres des prix moyens par catégorie

    Args:
        df: DataFrame avec les données

    Returns:
        Figure Plotly
    """
    if 'categorie' not in df.columns or 'prix' not in df.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="Données insuffisantes pour l'analyse des prix",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig

    # Convertir les prix en numérique et filtrer les prix valides
    df_copy = _clean_price_column(df)
    df_prices = df_copy[df_copy['prix'].notna() & (df_copy['prix'] > 0)]
    avg_prices = df_prices.groupby('categorie')['prix'].mean().sort_values(ascending=False)

    if avg_prices.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucune donnée de prix disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig

    # Créer le graphique
    fig = px.bar(
        x=avg_prices.index,
        y=avg_prices.values,
        title='Prix moyen par catégorie',
        labels={'x': 'Catégorie', 'y': 'Prix moyen (FCFA)'},
        color=avg_prices.values,
        color_continuous_scale='Reds'
    )

    fig.update_layout(
        xaxis_title="Catégorie",
        yaxis_title="Prix moyen (FCFA)",
        showlegend=False
    )

    return fig


def plot_temporal_trends(df: pd.DataFrame) -> go.Figure:
    """
    Créé un graphique de tendances temporelles

    Args:
        df: DataFrame avec les données

    Returns:
        Figure Plotly
    """
    if 'date_scraping' not in df.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucune donnée temporelle disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig

    # Convertir la date en datetime
    df_temp = df.copy()
    df_temp['date_scraping'] = pd.to_datetime(df_temp['date_scraping'])
    df_temp['date'] = df_temp['date_scraping'].dt.date

    # Compter les annonces par date
    date_counts = df_temp.groupby('date').size().reset_index(name='count')

    if date_counts.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucune donnée temporelle disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig

    # Créer le graphique de ligne
    fig = px.line(
        date_counts,
        x='date',
        y='count',
        title='Évolution du nombre d\'annonces dans le temps',
        labels={'date': 'Date', 'count': 'Nombre d\'annonces'},
        markers=True
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Nombre d'annonces"
    )

    return fig


def plot_price_trends(df: pd.DataFrame) -> go.Figure:
    """
    Créé un graphique de l'évolution des prix moyens

    Args:
        df: DataFrame avec les données

    Returns:
        Figure Plotly
    """
    if 'date_scraping' not in df.columns or 'prix' not in df.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="Données insuffisantes pour l'analyse temporelle des prix",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig

    # Convertir la date et filtrer les prix valides
    df_temp = _clean_price_column(df)
    df_temp['date_scraping'] = pd.to_datetime(df_temp['date_scraping'])
    df_temp['date'] = df_temp['date_scraping'].dt.date
    df_temp = df_temp[df_temp['prix'].notna() & (df_temp['prix'] > 0)]

    # Calculer le prix moyen par date
    price_trends = df_temp.groupby('date')['prix'].mean().reset_index(name='prix_moyen')

    if price_trends.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucune donnée de prix temporelle disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig

    # Créer le graphique
    fig = px.line(
        price_trends,
        x='date',
        y='prix_moyen',
        title='Évolution du prix moyen dans le temps',
        labels={'date': 'Date', 'prix_moyen': 'Prix moyen (FCFA)'},
        markers=True
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Prix moyen (FCFA)"
    )

    return fig


def get_price_statistics(df: pd.DataFrame) -> dict:
    """
    Calcule les statistiques de prix

    Args:
        df: DataFrame avec les données

    Returns:
        Dict avec statistiques
    """
    stats = {
        'total_annonces': len(df),
        'annonces_avec_prix': 0,
        'prix_moyen': 0,
        'prix_median': 0,
        'prix_min': 0,
        'prix_max': 0
    }

    if 'prix' in df.columns:
        # Convertir les prix en numérique pour éviter les erreurs de comparaison
        df_copy = _clean_price_column(df)
        df_prices = df_copy[df_copy['prix'].notna() & (df_copy['prix'] > 0)]
        stats['annonces_avec_prix'] = len(df_prices)

        if not df_prices.empty:
            stats['prix_moyen'] = df_prices['prix'].mean()
            stats['prix_median'] = df_prices['prix'].median()
            stats['prix_min'] = df_prices['prix'].min()
            stats['prix_max'] = df_prices['prix'].max()

    return stats
