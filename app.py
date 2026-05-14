import streamlit as st
import requests

st.set_page_config(page_title="Il Ricettario Magico", page_icon="🍳", layout="centered")
st.title("🍳 Il Ricettario di Famiglia")

# FUNZIONI PER COLLEGARSI AL DATABASE INTERNET
def cerca_per_nome(nome):
    url = f"themealdb.com{nome}"
    risposta = requests.get(url)
    return risposta.json().get("meals") if risposta.status_code == 200 else None

def cerca_per_ingrediente(ingrediente):
    url = f"themealdb.com{ingrediente}"
    risposta = requests.get(url)
    return risposta.json().get("meals") if risposta.status_code == 200 else None

def ottieni_dettagli_piatto(id_piatto):
    url = f"themealdb.com{id_piatto}"
    risposta = requests.get(url)
    return risposta.json().get("meals")[0] if risposta.status_code == 200 else None

# CREAZIONE DELLE DUE FUNZIONALITÀ NELL'APP
modalita = st.radio("Cosa vuoi fare oggi?", ["🔍 Cerca una ricetta dal nome", "🛒 Svuota-Frigo (Trova ricette con un ingrediente avanzato)"])

piatto_scelto = None

if modalita == "🔍 Cerca una ricetta dal nome":
    ricerca = st.text_input("Inserisci il tipo di piatto (es. Pasta, Chicken, Pizza, Rice):")
    if ricerca:
        risultati = cerca_per_nome(ricerca)
        if risultati:
            nomi_piatti = [p["strMeal"] for p in risultati]
            scelta = st.selectbox("Seleziona il piatto:", nomi_piatti)
            piatto_scelto = next(p for p in risultati if p["strMeal"] == scelta)
        else:
            st.error("Nessun piatto trovato. Prova in inglese!")

else:
    ingrediente = st.text_input("Quale ingrediente ti è avanzato? (es. Tomato, Egg, Chicken, Potato):")
    if ingrediente:
        risultati = cerca_per_ingrediente(ingrediente)
        if risultati:
            nomi_piatti = [p["strMeal"] for p in risultati]
            scelta = st.selectbox("Ecco cosa puoi cucinare! Scegli un piatto:", nomi_piatti)
            piatto_selezionato_breve = next(p for p in risultati if p["strMeal"] == scelta)
            # Recupera la ricetta completa (ingredienti e passaggi) partendo dal piatto trovato
            piatto_scelto = ottieni_dettagli_piatto(piatto_selezionato_breve["idMeal"])
        else:
            st.error("Nessun piatto trovato con questo ingrediente. Prova in inglese!")

# SEZIONE VISUALIZZAZIONE DELLA RICETTA SELEZIONATA
if piatto_scelto:
    st.divider()
    st.header(f"✨ {piatto_scelto['strMeal']}")
    st.image(piatto_scelto["strMealThumb"], use_column_width=True)
    
    porzioni = st.number_input("Per quante persone cucini?", min_value=1, max_value=12, value=2)
    
    st.subheader("🛒 Ingredienti necessari:")
    for i in range(1, 21):
        ingr = piatto_scelto.get(f"strIngredient{i}")
        misura = piatto_scelto.get(f"strMeasure{i}")
        if ingr and ingr.strip():
            st.write(f"• **{ingr}**: {misura} (adattato per {porzioni} persone)")
            
    st.subheader("👩‍🍳 Preparazione passo passo:")
    istruzioni = piatto_scelto["strInstructions"].split("\r\n")
    for j, passaggio in enumerate(istruzioni, 1):
        if passaggio.strip():
            st.checkbox(f"{passaggio}", key=f"step_{j}_{piatto_scelto['idMeal']}")
            
    if piatto_scelto.get("strYoutube"):
        st.video(piatto_scelto["strYoutube"])
