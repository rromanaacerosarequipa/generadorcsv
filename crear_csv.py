import streamlit as st
import pandas as pd

st.title("Conversor Excel → CSV CAASA")

st.write("Convierte tu Excel al formato: correo,correo,,,PIN")

archivo = st.file_uploader("📤 Cargar archivo Excel", type=["xlsx", "xls"])

if archivo:
    if st.button("Procesar Archivo"):
        # Leer Excel con encabezados
        df = pd.read_excel(archivo)

        # Saltar encabezados (fila 0), tomar desde fila 1 hacia abajo
        correo = df.iloc[1:, 0]   # Columna A
        pin = df.iloc[1:, 5]      # Columna F

        # Construir formato final EXACTO
        df_final = pd.DataFrame({
            "correo": correo,
            "usuario": correo,
            "vacio1": "",
            "vacio2": "",
            "vacio3": "",
            "PIN": pin
        })

        # Eliminar filas totalmente vacías (opcional)
        df_final = df_final.dropna(subset=["correo", "PIN"])

        st.write("### 📄 Vista previa del CSV final")
        st.dataframe(df_final)

        # Exportar a CSV sin encabezados
        csv_bytes = df_final.to_csv(index=False, header=False).encode("utf-8")

        st.download_button(
            "📥 Descargar CSV Final",
            csv_bytes,
            "formato_caasa.csv",
            "text/csv"
        )
