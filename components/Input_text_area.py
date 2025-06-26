import streamlit as st

def Input_text_area(input_value=""):

    
    if 'initial_text_area_value' not in st.session_state:
        st.session_state.initial_text_area_value = "Type here..."

    current_input_text = st.text_area(
        "Enter source language text",
        # Use the native 'placeholder' argument
        placeholder="Type here...",
        # No need for the 'value' argument unless you want initial content *and* a placeholder
        height=200,
        label_visibility="collapsed",
        # max_chars=... (optional)
        key="translation_input", # A unique key is good practice
    )

    st.write(f"You wrote {len(current_input_text)} characters.")

    return current_input_text