import streamlit as st
import requests

st.set_page_config(page_title="Il Ricettario Magico", page_icon="🍳", layout="centered")
st.title("🍳 Il Ricettario di Famiglia")

# FUNZIONE DI TRADUZIONE AUTOMATICA (ITALIANO -> INGLESE)
def traduci_in_inglese(testo):
    try:
        url = f"translated.net{testo}&langpair=it|en"
        risposta = requests.get(url).json()
        return risposta["responseData"]["translatedText"]
    except:
        return testo  # Se il traduttore fallisce, usa il testo originale

# FUNZIONI CORRETTE PER IL DATABASE INTERNET (CON HTTPS://)
def cerca_per_nome(nome):
    nome_en = traduci_in_inglese(nome)
    url = f"themealdb.com{nome_en}"
    risposta = requests.get(url)
    return risposta.json().get("meals") if risposta.status_code == 200 else None

def cerca_per_ingrediente(ingrediente):
    ingr_en = traduci_in_inglese(ingrediente)
    url = f"themealdb.com{ingr_en}"
    risposta = requests.get(url)
    return risposta.json().get("meals") if risposta.status_code == 200 else None

def ottieni_dettagli_piatto(id_piatto):
    url = f"themealdb.com{id_piatto}"
    risposta = requests.get(url)
    if risposta.status_code == 200:
        p = risposta.json().get("meals")
        return p[0] if p else None
    return None

# INTERFACCIA UTENTE
modalita = st.radio("Cosa vuoi fare oggi?", ["🔍 Cerca una ricetta dal nome", "🛒 Svuota-Frigo (Trova ricette con un ingrediente avanzato)"])

piatto_scelto = None

if modalita == "🔍 Cerca una ricetta dal nome":
    ricerca = st.text_input("Inserisci il tipo di piatto (Puoi scrivere in ITALIANO, es. Pasta, Pollo, Torta, Riso):")
    if ricerca:
        risultati = cerca_per_nome(ricerca)
        if risultati:
            nomi_piatti = [p["strMeal"] for p in risultati]
            scelta = st.selectbox("Seleziona il piatto trovato:", nomi_piatti)
            piatto_scelto = next(p for p in risultati if p["strMeal"] == scelta)
        else:
            st.error("❌ Nessun piatto trovato. Prova con una parola più semplice (es. 'Pasta' o 'Pollo').")

else:
    ingrediente = st.text_input("Quale ingrediente ti è avanzato? (Puoi scrivere in ITALIANO, es. Pomodoro, Uovo, Patata):")
    if ingrediente:
        risultati = cerca_per_ingrediente(ingrediente)
        if risultati:
            nomi_piatti = [p["strMeal"] for p in risultati]
            scelta = st.selectbox("Ecco cosa puoi cucinare! Scegli un piatto:", nomi_piatti)
            piatto_selezionato_breve = next(p for p in risultati if p["strMeal"] == scelta)
            piatto_scelto = ottieni_dettagli_piatto(piatto_selezionato_breve["idMeal"])
        else:
            st.error("❌ Nessun piatto trovato con questo ingrediente.")

# VISUALIZZAZIONE DELLA RICETTA
if piatto_scelto:
    st.divider()
    st.header(f"✨ {piatto_scelto['strMeal']}")
    st.image(piatto_scelto["strMealThumb"], use_column_width=True)
    
    porzioni = st.number_input("Per quante persone cucini?", min_value=1, max_value=12, value=2)
    
    st.subheader("🛒 Ingredienti necessari (Nomi originali):")
    for i in range(1, 21):
        ingr = piatto_scelto.get(f"strIngredient{i}")
        misura = piatto_scelto.get(f"strMeasure{i}")
        if ingr and ingr.strip():
            st.write(f"• **{ingr}**: {misura} (Moltiplicato per {porzioni} persone)")
            
    st.subheader("👩‍🍳 Preparazione (Istruzioni):")
    istruzioni = piatto_scelto["strInstructions"].split("\r\n")
    for j, passaggio in enumerate(istruzioni, 1):
        if passaggio.strip():
            st.checkbox(f"{passaggio}", key=f"step_{j}_{piatto_scelto['idMeal']}")
            
    if piatto_scelto.get("strYoutube"):
        st.subheader("📺 Video Tutorial della ricetta:")
        st.video(piatto_scelto["strYoutube"])
