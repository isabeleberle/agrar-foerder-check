import streamlit as st
import pandas as pd

# 1. Konfiguration der Seite
st.set_page_config(page_title="AgriFund Scout Bayern", page_icon="🌾")

# 2. Titel und Einleitung
st.title("🌾 AgriFund Scout Bayern")
st.write("Finde relevante KULAP-Fördermaßnahmen für deinen Betrieb (Testversion).")

# 3. Daten laden (Die CSV-Datei, die wir eben erstellt haben)
# Wir nutzen 'cache_data', damit die App schneller läuft
@st.cache_data
def load_data():
    try:
        # Versucht die Datei aus dem gleichen Ordner zu laden
        df = pd.read_csv("kulap_measures.csv")
        return df
    except FileNotFoundError:
        st.error("Fehler: Die Datei 'kulap_measures.csv' wurde nicht gefunden.")
        return pd.DataFrame()

df = load_data()

# 4. Sidebar: Hier kommen die Eingaben des Landwirts hin
st.sidebar.header("🚜 Dein Betrieb")

# Frage 1: Nutzung
betriebstyp = st.sidebar.multiselect(
    "Welche Flächen bewirtschaftest du?",
   ,
    default=["Acker", "Grünland"]
)

# Frage 2: Aufwand
max_aufwand = st.sidebar.slider(
    "Maximaler Arbeitsaufwand (1=gering, 10=sehr hoch)",
    1, 10, 8
)

# 5. Logik: Filtern der Maßnahmen
# Wir filtern die Tabelle basierend auf den Eingaben
filtered_df = df[
    (df['type'].isin(betriebstyp)) & 
    (df['effort_score'] <= max_aufwand)
]

# 6. Ergebnisse anzeigen
st.header(f"Wir haben {len(filtered_df)} passende Förderungen gefunden:")

if not filtered_df.empty:
    for index, row in filtered_df.iterrows():
        # Jede Maßnahme bekommt eine eigene "Karte"
        with st.expander(f"📍 {row['id']} - {row['name']} ({row['reward']})"):
            st.markdown(f"**Beschreibung:** {row['description']}")
            st.markdown(f"**Voraussetzung:** {row['requirements']}")
            
            # Farbige Anzeige für den Aufwand
            if row['effort_score'] <= 3:
                color = "green"
                text = "Niedrig"
            elif row['effort_score'] <= 6:
                color = "orange"
                text = "Mittel"
            else:
                color = "red"
                text = "Hoch"
            
            st.markdown(f"**Aufwand:** :{color}[{text} ({row['effort_score']}/10)]")
else:
    st.info("Keine Maßnahmen mit diesen Kriterien gefunden. Versuch, den Filter für den Aufwand zu erhöhen.")

# Fußzeile
st.markdown("---")
st.caption("Datenbasis: KULAP Bayern 2025. Angaben ohne Gewähr. Dies ist ein Prototyp.")
