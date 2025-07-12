import streamlit as st
import ast
import time
import streamlit.components.v1 as components
import streamlit as st
from typing import List, Union, Tuple, Sequence
from testing_and_research.p4_alt_builder import alt_builder
import streamlit as st
import os
import streamlit.components.v1 as components


# Simulated "streaming" function
def stream_data(text):
    full_text = ""
    for word in text.split(" "):
        full_text += word + " "
        yield full_text
        time.sleep(0.01)

_component_func = components.declare_component(
    "annotated_text",
    url="http://localhost:3001",  # Make sure this matches your Vite dev server port!
)

def render_annotated(tokens: Sequence[Union[str, Tuple[str, str]]], alt_phrases: dict):
    # Format tokens for React component
    js_tokens = []
    for token in tokens:
        if isinstance(token, tuple):
            js_tokens.append([token[0], token[1]])
        else:
            js_tokens.append(token)
    
    component_value = _component_func(tokens=js_tokens, altPhrases=alt_phrases, key="annotated_text_component")


# Main output function
def Output_text_area(logprob_rows, oai_tokens: List[str], spcy_chunks: List[dict]):
    """
    logprob_rows : The log probabilities of each respective chatcompletion response that was gotten back from OpenAI API. It corresponds to each OpenAI Response Token

    oai_tokens: This is a list of just the tokens that was returned by OpenAI API in the chatcompletion response

    spcy_chunks: This is the list of chunks that have been created based on the main chatcompletion translation response from OpenAI
    """

    with st.container(border=False) as alter_area:
        # Build tokens and alt_phrases for all chunks
        tokens: List[Tuple[str, str]] = [(str(c["text"]), str(c["id"])) for c in spcy_chunks]
        alt_phrases = {}
        for c in spcy_chunks:
            chunk_text = c["text"]
            try:
                alt_list = alt_builder(chunk_text)
                # If alt_builder returns a string representation of a list, parse it
                if isinstance(alt_list, str):
                    alt_list = ast.literal_eval(alt_list)
                # Always include the original phrase as the first option
                if chunk_text not in alt_list:
                    alt_list = [chunk_text] + alt_list
                alt_phrases[chunk_text] = alt_list
            except Exception as e:
                alt_phrases[chunk_text] = [chunk_text]
        render_annotated(tokens, alt_phrases)
    return alter_area


# This will be used in dev mode


def annotated_text(tokens, alt_phrases, key=None):
    return _component_func(tokens=tokens, altPhrases=alt_phrases, key=key, default=None)



