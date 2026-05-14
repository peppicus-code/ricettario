import streamlit as st

st.set_page_config(page_title="Il Ricettario di Casa", page_icon="🍳", layout="centered")
st.title("🍳 Il Ricettario di Famiglia")

# DATABASE DELLE RICETTE
ricette = {
    "🍝 Carbonara Perfetta": {
        "ingredienti": {
            "Spaghetti": (80, "g"),
            "Guanciale": (60, "g"),
            "Tuorli d'uovo": (1, "pz"),
            "Pecorino Romano": (30, "g")
        },
        "preparazione": [
            "Taglia il guanciale a striscioline e rosolalo in padella senza olio.",
            "Cala la pasta in acqua bollente poco salata.",
            "Sbatti i tuorli con il pecorino e un goccio d'acqua di cottura della pasta per creare la crema.",
            "Scola la pasta al dente, unisci tutto a fuoco spento nella padella col guanciale e salta finché è cremosa."
        ]
    },
    "🍕 Margherita fatta in casa": {
        "ingredienti": {
            "Farina tipo 0": (150, "g"),
            "Acqua tiepida": (90, "ml"),
            "Lievito di birra fresco": (1, "g"),
            "Passata di pomodoro": (80, "g"),
            "Mozzarella fior di latte": (100, "g")
        },
        "preparazione": [
            "Sciogli il lievito nell'acqua e impasta gradualmente con la farina e un pizzico di sale.",
            "Lascia lievitare il panetto coperto per almeno 4-6 ore a temperatura ambiente.",
            "Stendi l'impasto in una teglia unta d'olio, condisci con pomodoro salato e un filo d'orlo.",
            "Inforna al massimo della temperatura per 10... (ricetta continua)"
        ]
    },
    "🥩 Scaloppine al Limone": {
        "ingredienti": {
            "Fettine di carne": (1.5, "pz"),
            "Farina": (20, "g"),
            "Burro": (15, "g"),
            "Succo di limone": (0.5, "pz"),
            "Brodo vegetale": (30, "ml")
        },
        "preparazione": [
            "Infarina leggermente le fettine di carne, scrollando la farina in eccesso.",
            "Sciogli il burro in padella e scotta la carne 1-2 minuti per lato, poi toglila.",
            "Nella stessa padella versa il succo di limone e il brodo, facendo stringere la salsa.",
            "Rimetti la carne in padella per qualche istante per nappare bene con la cremina."
        ]
    }
}

# MENU DI SELEZIONE
scelta = st.selectbox("📖 Scegli cosa cucinare oggi:", list(ricette.keys()))
porzioni = st.number_input("Per quante persone cucini?", min_value=1, max_value=12, value=2)

st.divider()

ricetta_scelta = ricette[scelta]
st.header(scelta)
st.subheader("🛒 Ingredienti necessari:")

for ingrediente, dati in ricetta_scelta["ingredienti"].items():
    quantita_base = dati[0]
    unita = dati[1]
    quantita_totale = quantita_base * porzioni
    if isinstance(quantita_totale, float) and quantita_totale.is_integer():
        quantita_totale = int(quantita_totale)
    st.write(f"• **{ingrediente}**: {quantita_totale}{unita}")

st.subheader("👩‍🍳 Preparazione passo passo:")
for i, passaggio in enumerate(ricetta_scelta["preparazione"], 1):
    st.checkbox(f"{i}. {passaggio}", key=f"step_{i}_{scelta}")
