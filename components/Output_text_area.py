import streamlit as st

def Output_text_area(output_value=""):

    
    current_output_text = st.text_area(
        "",
        # Use the native 'placeholder' argument
        placeholder="Translation output will appear here...",
        # No need for the 'value' argument unless you want initial content *and* a placeholder
        height=300,
        # max_chars=... (optional)
        label_visibility="collapsed",
        key="translation_output" # A unique key is good practice
    )

    return current_output_text