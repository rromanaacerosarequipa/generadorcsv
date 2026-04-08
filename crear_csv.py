import streamlit as st
import pandas as pd
import re

st.title("Conversor Excel → CSV CAASA")
st.write("Convierte tu Excel al formato: correo,correo,,,PIN")

archivo = st.file_uploader("📤 Cargar archivo Excel", type=["xlsx", "xls"])

# --- Función para detectar correos ---
def detectar_columna_correo(df):
    for col in df.columns:
        if df[col].astype(str).str.contains("@", na=False).any():
            return col
    return None

# --- Función para detectar el PIN ---
def detectar_columna_pin(df):
    for col in df.columns:
        if df[col].astype(str).str.match(r"^\d{6,12}$", na=False).any():
            return col
    return None

if archivo:
    if st.button("Procesar Archivo"):

        df = pd.read_excel(archivo)

        # Detectar columnas
        col_correo = detectar_columna_correo(df)
        col_pin = detectar_columna_pin(df)

        if col_correo is None:
            st.error("❌ No se encontró ninguna columna con correos.")
            st.stop()

        if col_pin is None:
            st.error("❌ No se encontró ninguna columna con PIN numérico.")
            st.stop()

        # Extraer datos (saltamos la fila 0 si es encabezado)
        correos = df[col_correo].dropna().astype(str)
        pines = df[col_pin].dropna().astype(str)

        # Igualar longitud (si difiere)
        max_len = max(len(correos), len(pines))
        correos = correos.reset_index(drop=True)
        pines = pines.reset_index(drop=True)

        # Construir el CSV final EXACTO
        df_final = pd.DataFrame({
            "A": correos,
            "B": correos,
            "C": "",
            "D": "",
            "E": "",
            "F": pines
        })

        st.write("### 📄 Vista previa del CSV final")
        st.dataframe(df_final)

        # Exportar CSV sin encabezados
        csv_bytes = df_final.to_csv(index=False, header=False).encode("utf-8")

        st.download_button(
            "📥 Descargar CSV Final",
            csv_bytes,
            "formato_caasa.csv",
            "text/csv"
        )
