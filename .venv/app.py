import streamlit as st
# Import functions from your custom modules
from components.app_styles import inject_global_styles
from components.top_form_selector import render_top_form_selectors
from components.translation_text_area import render_translation_text_areas

# --- 1. App Configuration ---
st.set_page_config(layout="wide", page_title="Nested Containers")

# --- 2. Inject Global Styles ---
inject_global_styles()

# --- 3. Initialize Session State ---
# Initialize session state for text area content
if 'input_text_content' not in st.session_state:
    st.session_state.input_text_content = "Type here..."
if 'output_text_content' not in st.session_state:
    st.session_state.output_text_content = "Translation output will appear here..."

# The sync button clicked status is managed within top_form_selectors.py's session state

# --- 4. Render UI Components & Handle Logic ---
with st.container(border=True):
    input_language, output_language, sync_button_was_clicked = render_top_form_selectors()


# Render the translation text areas
# Update session state with the current content of the input text area
    st.session_state.input_text_content, st.session_state.output_text_content = render_translation_text_areas(
        input_value=st.session_state.input_text_content,
        output_value=st.session_state.output_text_content
    )

# --- 5. Handle Translation Trigger ---
# Check if the sync button was clicked (status is managed in session state by the component)


# --- 6. Final UI Elements ---
st.divider()

st.info("Translation will be processed here based on the selected languages and input text. ")