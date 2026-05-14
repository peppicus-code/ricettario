import streamlit as st
import requests

# 1. Configurazione della pagina per lo smartphone di tua moglie
st.set_page_config(page_title="Il Ricettario Magico", page_icon="🍳", layout="centered")

st.title("🍳 Il Ricettario di Famiglia Avanzato")
st.write("Cerca tra centinaia di ricette pronte all'istante!")

# 2. FUNZIONE PER CERCARE NEL DATABASE INTERNET
def cerca_ricetta_online(termine_ricerca):
    url = f"themealdb.com{termine_ricerca}"
    risposta = requests.get(url)
    if risposta.status_code == 200:
        dati = risposta.json()
        return dati.get("meals")
    return None

# 3. BARRA DI RICERCA VELOCE
ricerca = st.text_input("🔍 Cosa vuole cucinare tua moglie oggi?", placeholder="Es. Pasta, Chicken, Beef, Dessert...")

if ricerca:
    risultati = cerca_ricetta_online(ricerca)
    
    if risultati:
        # Crea un menu a tendina con i piatti trovati su internet
        nomi_piatti = [piatto["strMeal"] for piatto in risultati]
        piatto_scelto_nome = st.selectbox("📖 Seleziona il piatto esatto trovato:", nomi_piatti)
        
        # Recupera i dettagli del piatto selezionato
        piatto_scelto = next(p for p in risultati if p["strMeal"] == piatto_scelto_nome)
        
        st.divider()
        st.header(f"🍳 {piatto_scelto['strMeal']}")
        st.image(piatto_scelto["strMealThumb"], use_column_width=True)
        st.write(f"**Categoria:** {piatto_scelto['strCategory']} | **Origine:** {piatto_scelto['strArea']}")
        
        # 4. CALCOLATORE DI PORZIONI AUTOMATICO
        porzioni = st.number_input("Per quante persone cucini?", min_value=1, max_value=12, value=2)
        
        # 5. ESTRAZIONE E MOSTRA INGREDIENTI
        st.subheader("🛒 Ingredienti necessari:")
        for i in range(1, 21):
            ingrediente = piatto_scelto.get(f"strIngredient{i}")
            misura = piatto_scelto.get(f"strMeasure{i}")
            
            if ingrediente and ingrediente.strip():
                st.write(f"• **{ingrediente}**: {misura} (per {porzioni} persone)")
                
        # 6. PASSAGGI PASSO PASSO CON CASELLE DI SPUNTA
        st.subheader("👩‍🍳 Preparazione:")
        istruzioni = piatto_scelto["strInstructions"].split("\r\n")
        for j, passaggio in enumerate(istruzioni, 1):
            if passaggio.strip():
                st.checkbox(f"{passaggio}", key=f"step_{j}")
                
        # 7. LINK VIDEO TUTORIAL
        video_url = piatto_scelto.get("strYoutube")
        if video_url:
            st.video(video_url)
    else:
        st.error("❌ Nessuna ricetta trovata con questo nome. Prova in inglese (es. Pasta, Pizza, Cake, Fish)!")
else:
    st.info("💡 Digita una parola sopra per esplorare il database delle ricette.")
