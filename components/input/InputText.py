import streamlit as st


def InputText(key:str):
    text_input = st.text_input(
        "Provide sentence to translate",
        key=key,
        placeholder="Input sentence",
        label_visibility="collapsed",
        value=st.session_state['input_text_content']
    )

    return text_input
