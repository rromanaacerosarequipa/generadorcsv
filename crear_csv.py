import streamlit as st
import pandas as pd
import re

# ---- ESTILO MODERNO ----
st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

body {
    background: linear-gradient(135deg, #0d0d0d, #1a1a1a);
}

.container {
    max-width: 900px;
    margin: auto;
}

.card {
    background: rgba(255,255,255,0.06);
    padding: 25px 35px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.12);
    margin-top: 20px;
}

h1 {
    text-align: center;
    font-size: 3rem !important;
    font-weight: 700 !important;
    color: white;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 1.2rem !important;
    color: #cfcfcf;
    margin-top: -10px;
}

.stButton>button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    border-radius: 10px;
    padding: 10px 22px;
    border: none;
    font-size: 1rem;
    transition: 0.2s ease;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #6366f1, #9333ea);
    transform: scale(1.03);
}

</style>
""", unsafe_allow_html=True)

# ---- UI ----
st.markdown("<h1>Conversor Excel → CSV CAASA</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Convierte tu Excel al formato empresarial: correo,correo,,,PIN</p>", unsafe_allow_html=True)

st.markdown("<div class='container'>", unsafe_allow_html=True)
st.markdown("<div class='card'>", unsafe_allow_html=True)

archivo = st.file_uploader("Cargar Excel", type=["xlsx", "xls"])

# --- Detectar correo ---
def detectar_columna_correo(df):
    for col in df.columns:
        if df[col].astype(str).str.contains("@", na=False).any():
            return col
    return None

# --- Detectar PIN ---
def detectar_columna_pin(df):
    for col in df.columns:
        if df[col].astype(str).str.match(r"^\d{6,12}$", na=False).any():
            return col
    return None

if archivo:
    if st.button("Procesar Archivo"):

        df = pd.read_excel(archivo)

        col_correo = detectar_columna_correo(df)
        col_pin = detectar_columna_pin(df)

        if col_correo is None:
            st.error("❌ No se encontró ninguna columna con correos.")
            st.stop()

        if col_pin is None:
            st.error("❌ No se encontró ninguna columna con PIN numérico.")
            st.stop()

        correos = df[col_correo].dropna().astype(str).reset_index(drop=True)
        pines = df[col_pin].dropna().astype(str).reset_index(drop=True)

        max_len = max(len(correos), len(pines))

        df_final = pd.DataFrame({
            "A": correos,
            "B": correos,
            "C": "",
            "D": "",
            "E": "",
            "F": pines
        })

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader("Vista Previa")
        st.dataframe(df_final, use_container_width=True)

        csv_bytes = df_final.to_csv(index=False, header=False).encode("utf-8")

        st.download_button(
            "Descargar CSV",
            csv_bytes,
            "formato_caasa.csv",
            "text/csv"
        )

st.markdown("</div></div>", unsafe_allow_html=True)
