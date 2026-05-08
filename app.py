import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="GDPR Audit Dashboard", page_icon="🛡️", layout="wide")

# Colori stile Excel (Blu/Verde)
COLOR_COMPLIANT = "#00b050"
COLOR_NON_COMPLIANT = "#c00000"
COLOR_IN_PROGRESS = "#ffc000"
COLOR_NA = "#d9d9d9"

# --- TITOLO ---
st.title("🛡️ Privacy & GDPR Governance Dashboard")
st.markdown("Monitoraggio Compliance, Audit e Intelligenza Artificiale per la compilazione dei Registri.")
st.markdown("---")

# --- CREAZIONE DELLE SCHEDE (TABS) ---
tab1, tab2, tab3 = st.tabs(["📊 Dashboard Generale", "📋 Checklist di Audit", "🤖 AI Copilot (Nuovi Trattamenti)"])

# ==========================================
# TAB 1: DASHBOARD (Come la prima pagina Excel)
# ==========================================
with tab1:
    st.subheader("Riepilogo Stato di Conformità (KPI)")
    
    # Metriche in alto
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Totale Requisiti", "124", "Audit 2026")
    col2.metric("Completati (Compliant)", "82", "66%", delta_color="normal")
    col3.metric("Da Sistemare (Non Compliant)", "15", "-12%", delta_color="inverse")
    col4.metric("Rischio Privacy Globale", "Basso", "Accettabile", delta_color="off")
    
    st.markdown("---")
    
    # Grafici
    col_grafico1, col_grafico2 = st.columns(2)
    
    with col_grafico1:
        st.markdown("**Distribuzione Stato Checklist**")
        dati_torta = pd.DataFrame({'Stato': ['Compliant', 'Non Compliant', 'In corso', 'N/A'], 'Valore':[82, 15, 20, 7]})
        fig_pie = px.pie(dati_torta, values='Valore', names='Stato', hole=0.5, 
                     color='Stato', color_discrete_map={
                         'Compliant': COLOR_COMPLIANT, 'Non Compliant': COLOR_NON_COMPLIANT, 
                         'In corso': COLOR_IN_PROGRESS, 'N/A': COLOR_NA})
        fig_pie.update_layout(margin=dict(t=20, b=20, l=0, r=0), height=350)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_grafico2:
        st.markdown("**Conformità per Area Aziendale**")
        dati_barre = pd.DataFrame({
            'Area':['HR', 'Marketing', 'IT & Sicurezza', 'Vendite', 'Fornitori'],
            'Completamento %': [90, 45, 85, 70, 50]
        })
        fig_bar = px.bar(dati_barre, x='Area', y='Completamento %', text='Completamento %',
                         color='Completamento %', color_continuous_scale='Teal')
        fig_bar.update_layout(margin=dict(t=20, b=20, l=0, r=0), height=350, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

# ==========================================
# TAB 2: CHECKLIST (Come i fogli interni Excel)
# ==========================================
with tab2:
    st.subheader("Dettaglio Audit e Piani di Rientro")
    
    # Dati finti che simulano le righe dell'Excel
    dati_audit =[
        {"Cod": "INF-01", "Requisito": "Informativa Sito Web aggiornata", "Area": "Marketing", "Stato": "Compliant", "Scadenza": "31/12/2026", "Note": "Verificata"},
        {"Cod": "INF-02", "Requisito": "Informativa Dipendenti", "Area": "HR", "Stato": "Compliant", "Scadenza": "31/12/2026", "Note": "Ok"},
        {"Cod": "CNS-01", "Requisito": "Raccolta consensi Newsletter", "Area": "Marketing", "Stato": "In corso", "Scadenza": "15/06/2026", "Note": "Da inserire double opt-in"},
        {"Cod": "DPA-01", "Requisito": "Nomina Resp. Esterno Aruba", "Area": "IT & Sicurezza", "Stato": "Compliant", "Scadenza": "31/12/2026", "Note": "Firmata"},
        {"Cod": "DPA-02", "Requisito": "Nomina Resp. Esterno Mailchimp", "Area": "Marketing", "Stato": "Non Compliant", "Scadenza": "URGENTE", "Note": "Manca accordo su SCC"},
        {"Cod": "SEC-01", "Requisito": "Policy Password Aziendale", "Area": "IT & Sicurezza", "Stato": "Compliant", "Scadenza": "31/12/2026", "Note": "Aggiornata a 12 caratteri"},
        {"Cod": "DPIA-01", "Requisito": "Valutazione d'impatto Videosorveglianza", "Area": "Sicurezza Fisica", "Stato": "Non Compliant", "Scadenza": "URGENTE", "Note": "Telecamere attive senza cartelli"}
    ]
    df_audit = pd.DataFrame(dati_audit)
    
    # Mostriamo la tabella con stile
    st.dataframe(
        df_audit, 
        use_container_width=True, 
        height=300,
        column_config={
            "Stato": st.column_config.SelectboxColumn("Status", options=["Compliant", "Non Compliant", "In corso"]),
        }
    )
    
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        st.button("💾 Salva Modifiche")
    with col_btn2:
        st.button("📩 Invia Solleciti via Email (Non Compliant)")

# ==========================================
# TAB 3: AI COPILOT (La magia dell'Automazione)
# ==========================================
with tab3:
    col_testo, col_risultato = st.columns([1, 1.2])
    
    with col_testo:
        st.subheader("🗣️ Nuovo Trattamento Dati")
        testo_utente = st.text_area(
            "Descrivi il nuovo processo in linguaggio naturale. L'AI estrarrà le voci per il Registro:", 
            height=150, 
            value="Abbiamo installato delle nuove telecamere nel piazzale esterno per evitare i furti di notte. Registrano h24 e le immagini vengono cancellate dopo 48 ore."
        )
        bottone_ai = st.button("🤖 Genera Analisi AI", type="primary", use_container_width=True)

    with col_risultato:
        if bottone_ai:
            with st.status("Elaborazione legale in corso...", expanded=True) as status:
                st.write("🧠 Estrazione Finalità e Base Giuridica...")
                time.sleep(1)
                st.write("⏱️ Calcolo tempi di conservazione...")
                time.sleep(1)
                status.update(label="Analisi Completata!", state="complete", expanded=False)
            
            st.success("**Analisi Inserita nel Registro Trattamenti**")
            st.markdown("""
            - **Finalità:** Sicurezza del patrimonio aziendale (Videosorveglianza)
            - **Base Giuridica:** Legittimo Interesse (Art. 6 lett. f)
            - **Dati Trattati:** Immagini, Riprese video
            - **Conservazione (Retention):** 48 Ore
            - **Rischio:** Richiesta DPIA Obbligatoria
            """)
            
            st.warning("⚠️ **Azione Automatica:** L'AI ha preparato il testo per i cartelli 'Area Videosorvegliata' e l'Informativa completa per i dipendenti.")
            st.download_button("📄 Scarica Informativa Generata (PDF)", "Testo finto PDF", file_name="informativa_video.txt")
