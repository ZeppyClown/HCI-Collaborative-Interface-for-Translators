import streamlit as st

def render_translation_text_areas(input_value="", output_value=""):

    col1, col2 = st.columns(2)


    if 'initial_text_area_value' not in st.session_state:
        st.session_state.initial_text_area_value = "Type here..."

    with col1:
        current_input_text = st.text_area(
            "Type to translate",
            # Use the native 'placeholder' argument
            placeholder="Type here...",
            # No need for the 'value' argument unless you want initial content *and* a placeholder
            height=300,
            # max_chars=... (optional)
            key="translation_input" # A unique key is good practice
        )

        # st.write(f"You wrote {len(txt)} characters.")

    with col2:
        current_output_text = st.text_area(
            "",
            # Use the native 'placeholder' argument
            placeholder="Translation output will appear here...",
            # No need for the 'value' argument unless you want initial content *and* a placeholder
            height=300,
            # max_chars=... (optional)
            key="translation_output" # A unique key is good practice
        )

    return current_input_text, current_output_text