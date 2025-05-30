import streamlit as st

def inject_global_styles():
    st.markdown(
    """
    <style>

    div[data-testid="stButton"] {
        padding-top: 25px; /* Optional: add some padding to the top */
        display: flex;
        justify-content: center; /* Horizontally center the button within this div */
        align-items: center;     /* Vertically center the button within this div */
        width: 100%;             /* Ensure this div takes the full width of its column */
        height: 100%;            /* Ensure this div takes the full height for vertical centering */
        /* background-color: #f0f0f0; /* For debugging: visualize its boundary */ */
        
    }
    </style>
    """,
    unsafe_allow_html=True
)