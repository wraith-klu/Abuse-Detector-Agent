import streamlit as st

def add_to_history(text: str):
    if "history" not in st.session_state:
        st.session_state.history = []
    if text not in st.session_state.history:
        st.session_state.history.append(text)
