import streamlit as st
from components.input.InputText import InputText


def InputForm():
    with st.form("input_form") as inputform:
        st.write("Translate Sentence: ")
        text_input = InputText("input_text_content")

        submitted = st.form_submit_button("Translate")
        if submitted:
            st.session_state['processing'] = submitted
            return text_input

    return inputform
