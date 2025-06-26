import streamlit as st
import time

# Import functions from your custom modules
from components.app_styles import inject_global_styles
from components.Input_text_area import Input_text_area
from components.Output_text_area import Output_text_area
from components.top_form_selector import render_top_form_selectors

# Leo's Components
from components.output.OutputContainer import OutputContainer
from components.ConfigBar import ConfigBar
from components.input.InputForm import InputForm

# Translation Backend (TESTING STAGE)
from testing_and_research.p1_translator import translate
from testing_and_research.p2_chunking import chunk_sentence


# --- 1. App Configuration ---
st.set_page_config(layout="centered", page_title="Nested Containers")

# --- 2. Inject Global Styles ---
inject_global_styles()

# --- 3. Initialize Session State ---
# Initialize session state for text area content
if "input_text_content" not in st.session_state:
    st.session_state.input_text_content = ""
if "output_text_content" not in st.session_state:
    st.session_state.output_text_content = ""

if "translating" not in st.session_state:
    st.session_state["translating"] = False
if "processing" not in st.session_state:
    st.session_state["processing"] = False
if "source_lang" not in st.session_state:
    st.session_state["source_lang"] = "Chinese(Simplified)"
if "dest_lang" not in st.session_state:
    st.session_state["dest_lang"] = "English"

# Reset Button. Does what is named. Wipes the entire input and get the user to start all over.
def reset():
    st.session_state["input_text_content"] = ""
    st.session_state["processing"] = False


# --- 4. Render UI Components & Handle Logic ---
st.title("Human Computer Interaction (HCI) Translator")

with st.container(border=True):
    ConfigBar()

# Translation Input
tin = InputForm()

# UI logic upon submitting text
if not st.session_state["input_text_content"]:
    with st.container(border=True):
        st.info("Type in a sentence to begin")
else:
    with st.container(border=True):
        t_from = st.session_state["source_lang"]
        if st.session_state["processing"]:
            with st.spinner("Translating"):

                # @ZeppyClown Comments to get you up to speed with how I "tied the backend" for now.

                # Translator - I imported the *translate* function from the p1_translator.py as a python module (see line 16 of this file) situated in testing_and_research folder in the essence of time
                    #  tokens: The OpenAI Tokens from the Original Translation Response
                    # logrows: The Log Probabilities of each Token that has been broken down by OpenAI in which there are alternative Tokens suggested but with lower logprob score
                tokens, logrows = translate(tin, transl_frm=t_from)
                
                # For this one I imported the *chunk_sentence* function from p2_chunking.py as a python module (see line 17 of this file)
                    # Implement Chunking to get the different semantic chunks according to our customised spaCy shallow parser
                chunks, plaintext = chunk_sentence(tokens)
            
            OutputContainer(plaintext, logrows, chunks, tokens)


st.button("Reset", on_click=reset)


# --- 5. Handle Translation Trigger ---
# Check if the sync button was clicked (status is managed in session state by the component)


# st.info("Translation will be processed here based on the selected languages and input text. ")


# import panel as pn
# pn.extension()
# sentence = "An 80-year-long study shows that good interpersonal relationships can make a person happier and healthier."


# def build_dynamic_sentence(sentence, alt_phrases):
#     components = []
#     i = 0
#     while i < len(sentence):
#         matched = None
#         for phrase in alt_phrases:
#             if sentence[i:].startswith(phrase):
#                 matched = phrase
#                 break
#         if matched:
#             select = pn.widgets.Select(options=alt_phrases[matched], value=matched, width=250)
#             components.append(select)
#             i += len(matched)
#         else:
#             # Add plain text until next phrase
#             start = i
#             while i < len(sentence) and all(not sentence[i:].startswith(p) for p in alt_phrases):
#                 i += 1
#             components.append(pn.pane.Markdown(sentence[start:i], margin=(0,5)))
#     return pn.Row(*components)

# dynamic_sentence = build_dynamic_sentence(sentence, ALT_PHRASES)
# dynamic_sentence.servable()
