"""
Software Gestione Pagamenti - App Streamlit
Avvia con: streamlit run pagamenti.py
"""
import streamlit as st

st.set_page_config(page_title="Gestione Pagamenti", layout="wide")

st.title("Gestione Pagamenti")
st.write("Benvenuto. Modifica questo file per aggiungere le tue funzionalità.")

if st.button("Clicca qui"):
    st.success("Funziona!")
