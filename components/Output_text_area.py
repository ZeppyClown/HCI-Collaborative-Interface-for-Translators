import streamlit as st
import time
from annotated_text import annotated_text

# Simulated "streaming" function
def stream_data(text):
    full_text = ""
    for word in text.split(" "):
        full_text += word + " "
        yield full_text
        time.sleep(0.01)

# Alt phrases for dynamic dropdowns
ALT_PHRASES = {
    "An 80-year-long study": [
        "An 80-year-long study",
        "A study of 80 years",
        "An 8-decade-long research"
    ],
    "good interpersonal relationships": [
        "good interpersonal relationships",
        "strong social bonds",
        "healthy personal connections"
    ]
}

def render_sentence_with_dropdowns(sentence, alt_phrases):
    output = []
    index = 0
    select_count = 0  # Used to ensure unique keys

    while index < len(sentence):
        matched = False
        for phrase in alt_phrases:
            if sentence[index:].startswith(phrase):
                key = f"select_{select_count}_{phrase[:10].strip().replace(' ', '_')}"
                selected = st.selectbox(
                    "",
                    alt_phrases[phrase],
                    index=0,
                    key=key,
                    label_visibility="collapsed"
                )
                output.append(selected)
                index += len(phrase)
                matched = True
                select_count += 1
                break
        if not matched:
            start = index
            while index < len(sentence) and all(not sentence[index:].startswith(p) for p in alt_phrases):
                index += 1
            output.append(sentence[start:index])
    return output


# Main output function
def Output_text_area(input_value=""):
    if "translation_output" not in st.session_state:
        st.session_state.translation_output = ""

    if st.session_state.get("sync_button_clicked_status", False):
        sentence = input_value
        placeholder = st.container()
        streamed_text = ""
        for partial in stream_data(sentence):
            streamed_text = partial
            placeholder.empty()
            with placeholder:
                # After each partial stream, rerender dropdown version of sentence
                rendered_output = render_sentence_with_dropdowns(streamed_text, ALT_PHRASES)
                st.markdown("**Rendered Sentence:**")
                st.write(*rendered_output)  # inline rendering

        st.session_state.sync_button_clicked_status = False
        st.success("Streaming completed!")
