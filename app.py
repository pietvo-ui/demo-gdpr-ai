import streamlit as st
import time
import pandas as pd
import plotly.express as px

# Impostazioni della pagina
st.set_page_config(page_title="AI GDPR Governance", page_icon="🔒", layout="wide")

# Intestazione
st.title("🔒 AI GDPR Governance & Audit Readiness")
st.markdown("Trasforma il linguaggio naturale nel tuo **Registro dei Trattamenti** e aggiorna la Compliance aziendale in tempo reale.")
st.markdown("---")

# Layout a due colonne per la parte superiore
col_input, col_dash = st.columns([1.5, 1])

with col_input:
    st.subheader("🗣️ 1. Descrivi il processo aziendale")
    testo_utente = st.text_area(
        "Cosa fa l'azienda? (L'AI estrarrà finalità, base giuridica, rischi e documenti necessari)", 
        height=120, 
        value="Raccogliamo le email e i nomi sul nostro sito web per mandare una newsletter mensile con le offerte. Usiamo Mailchimp per l'invio. I dati li teniamo finché l'utente non si disiscrive."
    )
    bottone_elabora = st.button("🤖 Compila Registro GDPR con AI", type="primary", use_container_width=True)

with col_dash:
    st.subheader("📊 Stato Compliance Attuale")
    # Grafico a torta che simula la dashboard del tuo Excel
    dati_torta = pd.DataFrame({'Stato':['Compliant', 'Non Compliant', 'In corso'], 'Valore': [65, 15, 20]})
    fig = px.pie(dati_torta, values='Valore', names='Stato', hole=0.4, color='Stato',
                 color_discrete_map={'Compliant':'#00cc96', 'Non Compliant':'#ef553b', 'In corso':'#636efa'})
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=200)
    st.plotly_chart(fig, use_container_width=True)

# Azione del bottone
if bottone_elabora:
    st.markdown("---")
    
    # --- EFFETTO ELABORAZIONE WOW ---
    with st.status("Analisi Legale e Privacy in corso...", expanded=True) as status:
        st.write("🧠 Estrazione categorie di dati personali e interessati...")
        time.sleep(1)
        st.write("⚖️ Individuazione Base Giuridica (Art. 6 GDPR)...")
        time.sleep(1)
        st.write("🔍 Valutazione fornitori esterni e trasferimenti Extra-UE...")
        time.sleep(1)
        st.write("📑 Aggiornamento Registro Trattamenti e Checklist Evidenze...")
        time.sleep(1)
        status.update(label="Analisi Completata! Registro Aggiornato.", state="complete", expanded=False)
    
    st.write(" ")
    
    # --- RISULTATI: REGISTRO TRATTAMENTI ---
    st.subheader("📁 2. Registro dei Trattamenti Aggiornato (Art. 30 GDPR)")
    
    # Dati generati dall'AI basati sull'input
    dati_registro = {
        "Cod.":["TR-042"],
        "Nome Trattamento":["Invio Newsletter Promozionale"],
        "Categorie Interessati":["Clienti / Prospect web"],
        "Dati Raccolti":["Nome, Cognome, Indirizzo Email"],
        "Base Giuridica": ["Consenso Esplicito (Art. 6 lett. a)"],
        "Fornitori (Responsabili)": ["Mailchimp (USA - SCC attive)"],
        "Scadenza (Retention)":["Fino a revoca (Opt-out)"]
    }
    df_registro = pd.DataFrame(dati_registro)
    st.dataframe(df_registro, use_container_width=True, hide_index=True)
    
    st.write(" ")
    
    # --- RISULTATI: CHECKLIST & DOCUMENTI ---
    st.subheader("📋 3. Task di Audit & Evidenze Documentali")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Azioni richieste (To-Do List):**")
        st.error("⚠️ **Manca Nomina:** Generare nomina a Responsabile Esterno (DPA) per Mailchimp.")
        st.warning("🔄 **Aggiornamento Policy:** Inserire la finalità 'Marketing' nell'Informativa Web principale.")
        st.success("✅ **Checklist Sicurezza:** Misure tecniche minime ok (Crittografia in transito).")
        
    with col2:
        st.markdown("**Bozza Informativa Privacy (Generata dall'AI):**")
        informativa = """Informativa Newsletter (Art. 13 GDPR)
I Suoi dati personali (Nome, Email) saranno trattati per l'invio di comunicazioni commerciali. 
La base giuridica del trattamento è il Suo consenso esplicito. 
I dati saranno comunicati a Mailchimp (USA), il trasferimento è garantito da Clausole Contrattuali Standard. 
Potrà revocare il consenso in qualsiasi momento tramite il link in calce alle email.
"""
        st.text_area("Testo da approvare:", value=informativa, height=130)
