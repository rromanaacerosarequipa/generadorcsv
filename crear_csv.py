import streamlit as st
import pandas as pd

st.title("Conversor Excel → CSV CAASA")

st.write("Sube tu archivo Excel con columnas A = correo y F = PIN.")

archivo = st.file_uploader("📤 Cargar archivo Excel", type=["xlsx", "xls"])

if archivo:
    if st.button("Procesar Archivo"):
        # Leer Excel
        df = pd.read_excel(archivo, header=None)

        # Columna A = correo
        correo = df.iloc[:, 0]

        # Columna F = PIN
        pin = df.iloc[:, 5]

        # Crear formato final CSV
        df_final = pd.DataFrame({
            "correo": correo,
            "usuario": correo,
            "vacio1": "",
            "vacio2": "",
            "PIN": pin
        })

        st.write("### 📄 Vista previa del resultado:")
        st.dataframe(df_final)

        # Convertir a CSV
        csv_bytes = df_final.to_csv(index=False, header=False).encode("utf-8")

        # Descargar
        st.download_button(
            "📥 Descargar CSV Final",
            data=csv_bytes,
            file_name="formato_caasa.csv",
            mime="text/csv"
        )
