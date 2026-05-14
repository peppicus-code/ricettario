import streamlit as st

st.set_page_config(page_title="Il Ricettario di Casa", page_icon="🍳", layout="centered")
st.title("🍳 Il Ricettario di Famiglia")

# Selezione porzioni touch-friendly
porzioni = st.number_input("Per quante persone cucini oggi?", min_value=1, max_value=12, value=2)

st.header("🍝 Ricetta: Carbonara Perfetta")

# Ingredienti proporzionati in automatico
st.subheader("Ingredienti necessari:")
st.write(f"• Spaghetti: {80 * porzioni}g")
st.write(f"• Guanciale: {60 * porzioni}g")
st.write(f"• Tuorli d'uovo: {1 * porzioni}")
st.write(f"• Pecorino Romano: {30 * porzioni}g")

# Passaggi interattivi con spunta
st.subheader("Preparazione:")
st.checkbox("1. Taglia il guanciale a striscioline e rosolalo in padella.")
st.checkbox("2. Cala la pasta in acqua bollente poco salata.")
st.checkbox("3. Sbatti i tuorli con il pecorino e un goccio d'acqua di cottura.")
st.checkbox("4. Scola la pasta, unisci tutto a fuoco spento e salta.")
