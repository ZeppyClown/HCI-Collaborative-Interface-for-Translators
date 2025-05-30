import streamlit as st

def render_top_form_selectors():
    """
    Renders the input/output language select boxes and the sync button.

    Returns:
        tuple: (input_language_selection, output_language_selection, sync_button_clicked_status).
    """
    # Initialize session state for button click status
    if "sync_button_clicked_status" not in st.session_state:
        st.session_state.sync_button_clicked_status = False

    input_lang_selected = None
    output_lang_selected = None
    button_was_clicked = False

    # Outer Container (as in your original app.py)
    
    un1, left, middle, right, un = st.columns([2, 3, 1, 3, 2], gap="small")

    with left:
        input_lang_selected = st.selectbox(
            "Input Language",
            ("English", "Spanish", "French", "German", "Chinese"),
            index=0,
            key="input_language_selector" # Unique key
        )

    with middle:
        # Removed the custom <div> with 'centered-button-container' as the CSS targets data-testid="stButton" directly
        if st.button("", icon=":material/sync_alt:", use_container_width=False, key="centered_sync_button_within_col_top"): # Unique key
            st.session_state.sync_button_clicked_status = True
            button_was_clicked = True
            st.success("Translation triggered!")

    with right:
        output_lang_selected = st.selectbox(
            "Output Language",
            ("English", "Spanish", "French", "German", "Chinese"),
            index=0,
            key="output_language_selector" # Unique key
        )
    st.divider() # Divider inside the container

    return input_lang_selected, output_lang_selected, button_was_clicked