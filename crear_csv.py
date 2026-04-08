import streamlit as st
import pandas as pd

st.title("🟦 Generador CSV CAASA")

st.write("Sube un archivo CSV con columnas **correo** y **PIN** y genera el formato final.")

# ----------------------------
# 1) BOTÓN PARA CARGAR CSV
# ----------------------------
archivo = st.file_uploader("📤 Cargar CSV", type=["csv"])

if archivo is not None:
    if st.button("Procesar CSV"):
        df = pd.read_csv(archivo)

        # Validar columnas
        if not {"correo", "PIN"}.issubset(df.columns):
            st.error("❌ El archivo debe tener las columnas: correo, PIN")
        else:
            st.success("✅ Archivo cargado y procesado correctamente")

            # Crear formato final
            df_final = pd.DataFrame()
            df_final["correo"] = df["correo"]
            df_final["usuario"] = df["correo"]
            df_final["col1"] = ""
            df_final["col2"] = ""
            df_final["PIN"] = df["PIN"]

            st.write("### 📄 Vista previa del CSV final:")
            st.dataframe(df_final)

            # Convertir a CSV
            csv_bytes = df_final.to_csv(index=False).encode("utf-8")

            # ----------------------------
            # 2) BOTÓN PARA DESCARGAR CSV
            # ----------------------------
            st.download_button(
                label="📥 Descargar CSV Formateado",
                data=csv_bytes,
                file_name="usuarios_formateado.csv",
                mime="text/csv"
            )