"""
Application Streamlit pour le scraping et l'analyse de données CoinAfrique
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
import glob

# Import des modules personnalisés
from scraper.beautifulsoup_scraper import (
    CATEGORIES, scrape_category, save_to_csv
)
from utils.visualizations import (
    plot_price_distribution, plot_price_boxplot, plot_geographic_distribution,
    plot_category_analysis, plot_average_price_by_category, plot_temporal_trends,
    plot_price_trends, get_price_statistics
)


# Configuration de la page
st.set_page_config(
    page_title="Data Scraper",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)


# Titre principal
st.markdown("<h1 style='text-align: center; color: #FF6B35;'>Projet Data scraping</h1>",
            unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Application de scraping et d'analyse des annonces d'animaux sur CoinAfrique</p>",
            unsafe_allow_html=True)
st.markdown("---")


# Sidebar
st.sidebar.title("Configuration")
st.sidebar.markdown("---")

# Sélecteur de nombre de pages
num_pages = st.sidebar.slider(
    "Nombre de pages à scraper",
    min_value=1,
    max_value=100,
    value=2,
    help="Sélectionnez le nombre de pages à scraper par catégorie (Note: le scraping détaillé prend environ 2-3 minutes par page)"
)

st.sidebar.markdown("---")

# Menu de navigation
menu = st.sidebar.radio(
    "Navigation",
    ["Scraper avec BeautifulSoup", "Télécharger données WebScraper", "Dashboard", "Évaluation"],
    help="Sélectionnez le module que vous souhaitez utiliser"
)

st.sidebar.markdown("---")


# =======================
# MODULE 1: SCRAPER BEAUTIFULSOUP
# =======================
if menu == "Scraper avec BeautifulSoup":
    st.header("Scraper les données avec BeautifulSoup")
    st.markdown("Ce module permet de scraper les annonces directement depuis CoinAfrique en utilisant BeautifulSoup.")

    # Section: Données déjà scrapées
    st.subheader("Données déjà scrapées")
    scraped_files = glob.glob("data/scraped/*.csv")

    if scraped_files:
        st.success(f"{len(scraped_files)} fichier(s) de données disponible(s)")

        # Sélection du fichier à afficher
        file_options = {os.path.basename(f): f for f in scraped_files}
        selected_file_name = st.selectbox(
            "Sélectionnez un fichier à visualiser",
            options=list(file_options.keys())
        )

        selected_file = file_options[selected_file_name]

        try:
            df_existing = pd.read_csv(selected_file)

            # Statistiques rapides
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Annonces", len(df_existing))
            with col2:
                st.metric("Avec prix", len(df_existing[df_existing['prix'].notna()]))
            with col3:
                st.metric("Avec image", len(df_existing[df_existing['image_lien'].notna()]))

            # Afficher aperçu
            with st.expander("Voir les données"):
                st.dataframe(df_existing, width="stretch")

            # Téléchargement
            csv = df_existing.to_csv(index=False, encoding='utf-8')
            st.download_button(
                label="Télécharger ce fichier",
                data=csv,
                file_name=selected_file_name,
                mime="text/csv",
                width="stretch"
            )

        except Exception as e:
            st.error(f"Erreur lors du chargement: {str(e)}")
    else:
        st.info("Aucune donnée scrapée disponible. Lancez un scraping ci-dessous pour commencer.")

    st.markdown("---")

    # Section: Nouveau scraping
    st.subheader("Lancer un nouveau scraping")

    # Sélection de la catégorie
    col1, col2 = st.columns([2, 1])

    with col1:
        category_display = {
            "chiens": "Chiens",
            "moutons": "Moutons",
            "poules-lapins-et-pigeons": "Poules, Lapins et Pigeons",
            "autres-animaux": "Autres Animaux"
        }

        selected_category = st.selectbox(
            "Sélectionnez une catégorie",
            options=list(CATEGORIES.keys()),
            format_func=lambda x: category_display.get(x, x)
        )

    with col2:
        st.metric("Pages à scraper", num_pages)

    st.markdown("---")

    # Bouton de scraping
    if st.button("Lancer le scraping", type="primary", width="stretch"):
       
        with st.spinner(f"Scraping en cours de {num_pages} page(s) de la catégorie '{selected_category}'..."):
            try:
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Simuler le progrès (approximatif)
                for i in range(num_pages):
                    status_text.text(f"Scraping de la page {i+1}/{num_pages}...")
                    progress_bar.progress((i + 1) / num_pages)

                # Lancer le scraping
                df_scraped = scrape_category(selected_category, num_pages)

                progress_bar.progress(100)
                status_text.text("Scraping terminé!")

                if not df_scraped.empty:
                    st.success(f"Scraping réussi! {len(df_scraped)} annonces récupérées.")

                    # Sauvegarder les données
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{selected_category}_{timestamp}"
                    filepath = save_to_csv(df_scraped, filename)

                    st.info(f"Données sauvegardées dans: `{filepath}`")

                    # Afficher les données
                    st.subheader("Aperçu des données scrapées")
                    st.dataframe(df_scraped, width="stretch")

                    # Statistiques
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total annonces", len(df_scraped))
                    with col2:
                        with_price = len(df_scraped[df_scraped['prix'].notna()])
                        st.metric("Avec prix", with_price)
                    with col3:
                        with_image = len(df_scraped[df_scraped['image_lien'].notna()])
                        st.metric("Avec image", with_image)

                    # Bouton de téléchargement
                    csv = df_scraped.to_csv(index=False, encoding='utf-8')
                    st.download_button(
                        label="Télécharger les données en CSV",
                        data=csv,
                        file_name=f"{filename}.csv",
                        mime="text/csv",
                        width="stretch"
                    )
                else:
                    st.warning("Aucune donnée récupérée. Veuillez réessayer.")

            except Exception as e:
                st.error(f"Erreur lors du scraping: {str(e)}")


# =======================
# MODULE 2: TÉLÉCHARGER DONNÉES WEBSCRAPER
# =======================
elif menu == "Télécharger données WebScraper":
    st.header("Données WebScraper")
    st.markdown("Consultez et téléchargez les données scrapées depuis WebScraper.")

    # Charger les fichiers disponibles
    webscraper_files = glob.glob("data/webscraper/*.csv")

    if not webscraper_files:
        st.warning("Aucune donnée WebScraper disponible.")
        st.info("Placez vos fichiers CSV exportés depuis WebScraper dans le dossier `data/webscraper/`")
    else:
        # Sélection du fichier
        file_options = {os.path.basename(f): f for f in webscraper_files}
        selected_file_name = st.selectbox(
            "Sélectionnez un fichier de données",
            options=list(file_options.keys())
        )

        selected_file = file_options[selected_file_name]

        try:
            # Charger les données
            df = pd.read_csv(selected_file)

            if df.empty:
                st.warning("Le fichier sélectionné est vide.")
            else:
                st.success(f"Données chargées: {len(df)} annonces")

                # Afficher les données
                st.subheader("Aperçu des données")
                st.dataframe(df, width="stretch")

                # Statistiques basiques
                st.subheader("Statistiques")
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Total annonces", len(df))

                with col2:
                    if 'prix' in df.columns:
                        prix_valides = df[df['prix'].notna()]
                        st.metric("Avec prix", len(prix_valides))
                    else:
                        st.metric("Avec prix", "N/A")

                with col3:
                    st.metric("Colonnes", len(df.columns))

                with col4:
                    if 'ville' in df.columns:
                        st.metric("Villes uniques", df['ville'].nunique())
                    else:
                        st.metric("Villes uniques", "N/A")

                # Informations sur les colonnes
                st.subheader("Colonnes disponibles")
                st.write(", ".join(df.columns.tolist()))

                # Bouton de téléchargement
                st.markdown("---")
                csv = df.to_csv(index=False, encoding='utf-8')
                st.download_button(
                    label="Télécharger les données",
                    data=csv,
                    file_name=selected_file_name,
                    mime="text/csv",
                    width="stretch"
                )

        except Exception as e:
            st.error(f"Erreur lors du chargement des données: {str(e)}")


# =======================
# MODULE 3: DASHBOARD
# =======================
elif menu == "Dashboard":
    st.header("Dashboard d'analyse des données")
    st.markdown("Visualisez et analysez les données scrapées avec des graphiques interactifs.")

    # Charger les données disponibles
    scraped_files = glob.glob("data/scraped/*.csv")
    webscraper_files = glob.glob("data/webscraper/*.csv")

    all_files = scraped_files + webscraper_files

    if not all_files:
        st.warning("Aucune donnée disponible. Veuillez d'abord scraper des données ou uploader un fichier.")
        st.info("Utilisez le module 'Scraper avec BeautifulSoup' ou 'Télécharger données WebScraper' pour obtenir des données.")
    else:
        # Sélection du fichier
        file_options = {os.path.basename(f): f for f in all_files}
        selected_file_name = st.selectbox(
            "Sélectionnez un fichier de données",
            options=list(file_options.keys())
        )

        selected_file = file_options[selected_file_name]

        try:
            # Charger les données
            df = pd.read_csv(selected_file)

            if df.empty:
                st.warning("Le fichier sélectionné est vide.")
            else:
                st.success(f"Données chargées: {len(df)} annonces")

                # KPIs
                st.subheader("Indicateurs clés")
                stats = get_price_statistics(df)

                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("Total annonces", stats['total_annonces'])
                with col2:
                    st.metric("Avec prix", stats['annonces_avec_prix'])
                with col3:
                    st.metric("Prix moyen", f"{stats['prix_moyen']:,.0f} FCFA" if stats['prix_moyen'] > 0 else "N/A")
                with col4:
                    st.metric("Prix min", f"{stats['prix_min']:,.0f} FCFA" if stats['prix_min'] > 0 else "N/A")
                with col5:
                    st.metric("Prix max", f"{stats['prix_max']:,.0f} FCFA" if stats['prix_max'] > 0 else "N/A")

                st.markdown("---")

                # Filtres
                st.subheader("Filtres")
                col1, col2, col3 = st.columns(3)

                with col1:
                    # Filtre par catégorie
                    if 'categorie' in df.columns:
                        categories = ['Toutes'] + list(df['categorie'].unique())
                        selected_cat = st.selectbox("Catégorie", categories)
                        if selected_cat != 'Toutes':
                            df = df[df['categorie'] == selected_cat]

                with col2:
                    # Filtre par ville
                    if 'ville' in df.columns:
                        villes = ['Toutes'] + sorted([v for v in df['ville'].unique() if pd.notna(v)])
                        selected_ville = st.selectbox("Ville", villes)
                        if selected_ville != 'Toutes':
                            df = df[df['ville'] == selected_ville]

                with col3:
                    # Filtre par fourchette de prix
                    if 'prix' in df.columns:
                        # Convertir les prix en numérique
                        df_copy = df.copy()
                        # Nettoyer les prix avant conversion
                        df_copy['prix'] = df_copy['prix'].astype(str).str.replace(' ', '').str.replace('CFA', '')
                        df_copy['prix'] = pd.to_numeric(df_copy['prix'], errors='coerce')
                        df_prices = df_copy[df_copy['prix'].notna() & (df_copy['prix'] > 0)]
                        if not df_prices.empty:
                            min_price = float(df_prices['prix'].min())
                            max_price = float(df_prices['prix'].max())
                            price_range = st.slider(
                                "Fourchette de prix (FCFA)",
                                min_value=min_price,
                                max_value=max_price,
                                value=(min_price, max_price)
                            )
                            # Filtrer le dataframe original avec conversion
                            df['prix_num'] = df['prix'].astype(str).str.replace(' ', '').str.replace('CFA', '')
                            df['prix_num'] = pd.to_numeric(df['prix_num'], errors='coerce')
                            df = df[(df['prix_num'] >= price_range[0]) & (df['prix_num'] <= price_range[1])]
                            df = df.drop('prix_num', axis=1)

                st.markdown("---")

                # Visualisations
                st.subheader("Visualisations")

                # Tabs pour organiser les graphiques
                tab1, tab2, tab3, tab4 = st.tabs([
                    "Distribution des prix",
                    "Répartition géographique",
                    "Analyse par catégorie",
                    "Tendances temporelles"
                ])

                with tab1:
                    st.markdown("### Distribution des prix")
                    col1, col2 = st.columns(2)

                    with col1:
                        fig_hist = plot_price_distribution(df)
                        st.plotly_chart(fig_hist, use_container_width=True)

                    with col2:
                        fig_box = plot_price_boxplot(df)
                        st.plotly_chart(fig_box, use_container_width=True)

                    # Tableau des prix extrêmes
                    st.markdown("#### Top 10 des annonces les plus chères")
                    # Nettoyer les prix pour le tri
                    df_top_copy = df.copy()
                    df_top_copy['prix_num'] = df_top_copy['prix'].astype(str).str.replace(' ', '').str.replace('CFA', '')
                    df_top_copy['prix_num'] = pd.to_numeric(df_top_copy['prix_num'], errors='coerce')
                    df_top_prices = df_top_copy[df_top_copy['prix_num'].notna()].nlargest(10, 'prix_num')[['nom', 'prix', 'adresse']]
                    st.dataframe(df_top_prices, width="stretch")

                with tab2:
                    st.markdown("### Répartition géographique")
                    fig_geo = plot_geographic_distribution(df)
                    st.plotly_chart(fig_geo, use_container_width=True)

                    # Tableau des villes
                    if 'ville' in df.columns:
                        st.markdown("#### Statistiques par ville")
                        # Nettoyer les prix pour les agrégations
                        df_ville = df.copy()
                        df_ville['prix_num'] = df_ville['prix'].astype(str).str.replace(' ', '').str.replace('CFA', '')
                        df_ville['prix_num'] = pd.to_numeric(df_ville['prix_num'], errors='coerce')

                        ville_stats = df_ville.groupby('ville').agg({
                            'nom': 'count',
                            'prix_num': ['mean', 'min', 'max']
                        }).round(0)
                        ville_stats.columns = ['Nombre annonces', 'Prix moyen', 'Prix min', 'Prix max']
                        ville_stats = ville_stats.sort_values('Nombre annonces', ascending=False)
                        st.dataframe(ville_stats, width="stretch")

                with tab3:
                    st.markdown("### Analyse par catégorie")
                    col1, col2 = st.columns(2)

                    with col1:
                        fig_cat = plot_category_analysis(df)
                        st.plotly_chart(fig_cat, use_container_width=True)

                    with col2:
                        fig_avg = plot_average_price_by_category(df)
                        st.plotly_chart(fig_avg, use_container_width=True)

                    # Tableau récapitulatif
                    if 'categorie' in df.columns:
                        st.markdown("#### Tableau récapitulatif par catégorie")
                        # Nettoyer les prix pour les agrégations
                        df_cat = df.copy()
                        df_cat['prix_num'] = df_cat['prix'].astype(str).str.replace(' ', '').str.replace('CFA', '')
                        df_cat['prix_num'] = pd.to_numeric(df_cat['prix_num'], errors='coerce')

                        cat_stats = df_cat.groupby('categorie').agg({
                            'nom': 'count',
                            'prix_num': ['mean', 'median', 'min', 'max']
                        }).round(0)
                        cat_stats.columns = ['Nombre', 'Prix moyen', 'Prix médian', 'Prix min', 'Prix max']
                        st.dataframe(cat_stats, width="stretch")

                with tab4:
                    st.markdown("### Tendances temporelles")

                    if 'date_scraping' in df.columns:
                        col1, col2 = st.columns(2)

                        with col1:
                            fig_trends = plot_temporal_trends(df)
                            st.plotly_chart(fig_trends, use_container_width=True)

                        with col2:
                            fig_price_trends = plot_price_trends(df)
                            st.plotly_chart(fig_price_trends, use_container_width=True)
                    else:
                        st.info("Les données temporelles ne sont pas disponibles pour ce fichier.")

        except Exception as e:
            st.error(f"Erreur lors du chargement des données: {str(e)}")


# =======================
# MODULE 4: ÉVALUATION
# =======================
elif menu == "Évaluation":
    st.header("Évaluation de l'application")

  

    st.markdown("---")

    # Liens vers les formulaires 
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Formulaire Kobo")
        st.markdown("""
        Utilisez notre formulaire Kobo pour une expérience mobile optimisée.
        """)

        # Bouton pour Kobo
        kobo_url = "https://ee.kobotoolbox.org/x/sZj0338r"
        st.link_button(
            "Ouvrir le formulaire Kobo",
            kobo_url,
            width="stretch"
        )

    with col2:
        st.markdown("### Formulaire Google Forms")
        st.markdown("""
        Préférez-vous Google Forms? Utilisez ce lien.
        """)

        # Bouton pour Google Forms 
        google_forms_url = "https://docs.google.com/forms/d/e/1FAIpQLSffsU8eR5n78eJGN3GRXG_GA-ClLup1fEOHbgT8yZ-xN0aJ-Q/viewform?usp=preview"
        st.link_button(
            "Ouvrir Google Forms",
            google_forms_url,
            width="stretch"
        )

    st.markdown("---")

    st.success("Merci pour votre précieux retour ! Vos commentaires nous aideront à améliorer l’application. ")



