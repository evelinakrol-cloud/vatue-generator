import streamlit as st
import pandas as pd
from vatue import generuj_vatue
from vatuek import generuj_vatuek

st.title("📄 Generator VAT-UE / VAT-UEK")

typ = st.radio("Wybierz deklarację:", ["VAT-UE", "VAT-UEK"])

plik = st.file_uploader("Wgraj plik Excel", type=["xlsx"])

if plik:
    df = pd.read_excel(plik, header=None)
    st.success("Plik wczytany ✅")

    if st.button("Generuj XML"):

        if typ == "VAT-UE":
            xml = generuj_vatue(df, plik.name)
            nazwa = "VAT-UE.xml"
        else:
            xml = generuj_vatuek(df, plik.name)
            nazwa = "VAT-UEK.xml"

        st.download_button(
            label="📥 Pobierz XML",
            data=xml,
            file_name=nazwa,
            mime="application/xml"
        )