import streamlit as st

def Input_text_area(input_value=""):

    
    if 'initial_text_area_value' not in st.session_state:
        st.session_state.initial_text_area_value = "Type here..."

    current_input_text = st.text_area(
        "Type to translate",
        # Use the native 'placeholder' argument
        placeholder="Type here...",
        # No need for the 'value' argument unless you want initial content *and* a placeholder
        height=300,
        label_visibility="collapsed",
        # max_chars=... (optional)
        key="translation_input" # A unique key is good practice
    )

        # st.write(f"You wrote {len(txt)} characters.")

    return current_input_text