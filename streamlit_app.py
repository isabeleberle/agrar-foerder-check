import streamlit as st
import pandas as pd

# 1. Konfiguration der Seite
st.set_page_config(page_title="AgriFund Scout Bayern", page_icon="🌾")

# 2. Titel und Einleitung
st.title("🌾 AgriFund Scout Bayern")
st.write("Finde relevante KULAP-Fördermaßnahmen für deinen Betrieb (Testversion).")

# 3. Daten laden
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("kulap_measures.csv")
        return df
    except FileNotFoundError:
        return pd.DataFrame()

df = load_data()

# Check: Wenn keine Daten da sind, zeige Fehler
if df.empty:
    st.error("Die Datenbank 'kulap_measures.csv' wurde nicht gefunden oder ist leer.")
else:
    # 4. Sidebar: Eingaben
    st.sidebar.header("🚜 Dein Betrieb")

    # Wir holen uns alle möglichen Typen (Acker, Grünland etc.) direkt aus der CSV
    alle_typen = df['type'].unique().tolist() if 'type' in df.columns else ["Acker", "Grünland"]

    # Frage 1: Nutzung
    # HIER LAG DER FEHLER: Die Liste der Optionen 'alle_typen' fehlte
    betriebstyp = st.sidebar.multiselect(
        "Welche Flächen bewirtschaftest du?",
        options=alle_typen,
        default=["Acker", "Grünland"]
    )

    # Frage 2: Aufwand
    max_aufwand = st.sidebar.slider(
        "Maximaler Arbeitsaufwand (1=gering, 10=sehr hoch)",
        1, 10, 8
    )

    # 5. Logik: Filtern
    # Wir filtern nur, wenn die Spalten auch existieren
    if 'type' in df.columns and 'effort_score' in df.columns:
        filtered_df = df[
            (df['type'].isin(betriebstyp)) & 
            (df['effort_score'] <= max_aufwand)
        ]

        # 6. Ergebnisse anzeigen
        st.header(f"Wir haben {len(filtered_df)} passende Förderungen gefunden:")

        if not filtered_df.empty:
            for index, row in filtered_df.iterrows():
                with st.expander(f"📍 {row['id']} - {row['name']} ({row['reward']})"):
                    st.markdown(f"**Beschreibung:** {row['description']}")
                    st.markdown(f"**Voraussetzung:** {row['requirements']}")
                    
                    # Farbige Anzeige für den Aufwand
                    score = row['effort_score']
                    if score <= 3:
                        color = "green"
                        text = "Niedrig"
                    elif score <= 6:
                        color = "orange"
                        text = "Mittel"
                    else:
                        color = "red"
                        text = "Hoch"
                    
                    st.markdown(f"**Aufwand:** :{color}[{text} ({score}/10)]")
        else:
            st.info("Keine Maßnahmen mit diesen Kriterien gefunden.")
    else:
        st.error("Fehler in der CSV-Struktur: Spalten 'type' oder 'effort_score' fehlen.")

# Fußzeile
st.markdown("---")
st.caption("Datenbasis: KULAP Bayern 2025. Angaben ohne Gewähr.")
