import streamlit as st
import time
from components.Output_text_area import Output_text_area
from testing_and_research.p1_translator import *
from testing_and_research.p2_chunking import chunk_sentence
from typing import List, Dict
from annotated_text import annotated_text


def OutputContainer(
    plaintext: str, logprobs, chunks: List[Dict], oai_tokens: List[str]
):
    with st.container(border=False) as OutputContainer:
        st.subheader("Translation", divider="gray")
        st.text(f"Original Translated Sentence: \n {plaintext}")
        Output_text_area(logprobs, oai_tokens, chunks)
        # if is_translating and len(transl_input) != 0:
        #     with st.spinner("Translating"):
        #         tokens, rows = translation(transl_input, source_lang)
        #         chunks , plaintext = chunk_sentence(tokens)

        #     st.session_state["tranlating"] = False
        # st.text("".join(tokens))
    return OutputContainer
