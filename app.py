import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path
from datetime import date

st.set_page_config(page_title="GDPR Governance Dashboard", page_icon="🛡️", layout="wide")

APP_DIR = Path(__file__).parent
DEFAULT_FILE = APP_DIR / "Governance_GDPR_Autoghinzani_Dashboard.xlsx"

SHEETS = {
    "checklist": "Checklist_GDPR",
    "azioni": "Azioni",
    "evidenze": "Registro_Evidenze",
    "raci": "Governance_RACI",
}

@st.cache_data(show_spinner=False)
def read_excel(file):
    return {
        "checklist": pd.read_excel(file, sheet_name=SHEETS["checklist"], header=5),
        "azioni": pd.read_excel(file, sheet_name=SHEETS["azioni"], header=3),
        "evidenze": pd.read_excel(file, sheet_name=SHEETS["evidenze"], header=3),
        "raci": pd.read_excel(file, sheet_name=SHEETS["raci"], header=3),
    }

def clean(df):
    df = df.copy().dropna(how="all")
    df.columns = [str(c).strip() for c in df.columns]
    return df

def filter_multiselect(df, column, label):
    if column not in df.columns:
        return df
    values = sorted([x for x in df[column].dropna().unique()])
    selected = st.sidebar.multiselect(label, values, default=values)
    return df[df[column].isin(selected)] if selected else df

st.title("🛡️ GDPR / Privacy Governance Dashboard")
st.caption("App Streamlit generata dal workbook Excel: checklist, azioni, evidenze e matrice RACI.")

uploaded = st.sidebar.file_uploader("Carica un file Excel aggiornato", type=["xlsx"])

if uploaded is not None:
    source = uploaded
elif DEFAULT_FILE.exists():
    source = DEFAULT_FILE
else:
    st.error("File Excel non trovato nella cartella dell'app.")
    st.markdown(
        """
        Per risolvere su Streamlit Cloud/GitHub, fai una di queste due cose:

        1. carica il file Excel dalla barra laterale; oppure  
        2. aggiungi nel repository GitHub il file `Governance_GDPR_Autoghinzani_Dashboard.xlsx` nella stessa cartella di `app.py`.
        """
    )
    with st.expander("File presenti nella cartella dell'app"):
        st.write([p.name for p in APP_DIR.iterdir()])
    st.stop()

try:
    data = read_excel(source)
except FileNotFoundError:
    st.error("Il file Excel indicato non esiste. Verifica che sia stato caricato su GitHub insieme ad app.py.")
    st.stop()
except ValueError as e:
    st.error("Il file Excel è stato trovato, ma uno o più fogli non hanno il nome atteso.")
    st.code(str(e))
    st.stop()

checklist = clean(data["checklist"])
azioni = clean(data["azioni"])
evidenze = clean(data["evidenze"])
raci = clean(data["raci"])

for col in ["Stato", "Priorità", "Sezione", "Owner"]:
    if col in checklist.columns:
        checklist[col] = checklist[col].fillna("Da compilare")

if "Stato Azione" in azioni.columns:
    azioni["Stato Azione"] = azioni["Stato Azione"].fillna("Da avviare")
if "Priorità" in azioni.columns:
    azioni["Priorità"] = azioni["Priorità"].fillna("Non assegnata")
def normalize_date_column(df, column):
    if column in df.columns:
        df[column] = pd.to_datetime(df[column], errors="coerce", dayfirst=True)
    return df

azioni = normalize_date_column(azioni, "Scadenza")

st.sidebar.header("Filtri")
filtered_checklist = checklist.copy()
filtered_checklist = filter_multiselect(filtered_checklist, "Sezione", "Sezioni checklist")
filtered_checklist = filter_multiselect(filtered_checklist, "Stato", "Stato checklist")
filtered_checklist = filter_multiselect(filtered_checklist, "Priorità", "Priorità checklist")

ok = int((checklist.get("Stato", pd.Series(dtype=str)) == "OK").sum())
ko = int((checklist.get("Stato", pd.Series(dtype=str)) == "KO").sum())
den = ok + ko
compliance = (ok / den * 100) if den else 0
azioni_tot = int(azioni.get("Azione correttiva", pd.Series(dtype=str)).notna().sum())
azioni_compl = int((azioni.get("Stato Azione", pd.Series(dtype=str)) == "Completata").sum())
if "Scadenza" in azioni.columns and "Stato Azione" in azioni.columns:
    oggi = pd.Timestamp.today().normalize()
    scadenze = pd.to_datetime(azioni["Scadenza"], errors="coerce", dayfirst=True)
    scadute = int(((azioni["Stato Azione"].astype(str) != "Completata") & scadenze.notna() & (scadenze < oggi)).sum())
else:
    scadute = 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Compliance", f"{compliance:.1f}%", help="OK / (OK + KO)")
c2.metric("Controlli OK", ok)
c3.metric("Controlli KO", ko)
c4.metric("Azioni aperte", max(azioni_tot - azioni_compl, 0))
c5.metric("Azioni scadute", scadute)

g1, g2 = st.columns(2)
with g1:
    st.subheader("Stato checklist")
    if "Stato" in checklist.columns:
        chart_df = checklist["Stato"].value_counts(dropna=False).reset_index()
        chart_df.columns = ["Stato", "Conteggio"]
        st.plotly_chart(px.pie(chart_df, names="Stato", values="Conteggio", hole=0.45), use_container_width=True)
with g2:
    st.subheader("Compliance per sezione")
    if {"Sezione", "Stato"}.issubset(checklist.columns):
        sec = checklist.groupby("Sezione").agg(
            OK=("Stato", lambda s: (s == "OK").sum()),
            KO=("Stato", lambda s: (s == "KO").sum()),
        ).reset_index()
        sec["Compliance %"] = (sec["OK"] / (sec["OK"] + sec["KO"]).replace(0, pd.NA) * 100).fillna(0)
        st.plotly_chart(px.bar(sec, x="Sezione", y="Compliance %", text="Compliance %"), use_container_width=True)

tab1, tab2, tab3, tab4 = st.tabs(["Checklist", "Azioni", "Evidenze", "Governance RACI"])

with tab1:
    st.subheader("Checklist GDPR")
    st.dataframe(filtered_checklist, use_container_width=True, hide_index=True)
    st.download_button("Scarica checklist filtrata CSV", filtered_checklist.to_csv(index=False).encode("utf-8-sig"), "checklist_gdpr_filtrata.csv", "text/csv")

with tab2:
    st.subheader("Registro azioni / remediation")
    az_view = azioni.copy()
    if "Scadenza" in az_view.columns:
        az_view["Scadenza"] = pd.to_datetime(az_view["Scadenza"], errors="coerce", dayfirst=True).dt.strftime("%d/%m/%Y").fillna("")
    st.dataframe(az_view, use_container_width=True, hide_index=True)
    if "Stato Azione" in azioni.columns:
        az_count = azioni["Stato Azione"].value_counts().reset_index()
        az_count.columns = ["Stato Azione", "Conteggio"]
        st.plotly_chart(px.bar(az_count, x="Stato Azione", y="Conteggio", text="Conteggio"), use_container_width=True)

with tab3:
    st.subheader("Registro evidenze documentali")
    st.dataframe(evidenze, use_container_width=True, hide_index=True)
    if "Stato Evidenza" in evidenze.columns:
        ev = evidenze["Stato Evidenza"].fillna("Da compilare").value_counts().reset_index()
        ev.columns = ["Stato Evidenza", "Conteggio"]
        st.plotly_chart(px.pie(ev, names="Stato Evidenza", values="Conteggio"), use_container_width=True)

with tab4:
    st.subheader("Matrice Governance / RACI")
    st.dataframe(raci, use_container_width=True, hide_index=True)

st.divider()
st.info("Per aggiornare i dati: modifica il file Excel, ricaricalo dalla sidebar oppure sostituisci il file nella cartella dell’app su GitHub.")
