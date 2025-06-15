import streamlit as st
# Import functions from your custom modules
from components.app_styles import inject_global_styles
from components.Input_text_area import Input_text_area
from components.Output_text_area import Output_text_area
from components.top_form_selector import render_top_form_selectors
import streamlit.components.v1 as components

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

import streamlit as st
from typing import List, Union, Tuple

def render_annotated(tokens: List[Union[str, Tuple[str, str]]]):
    # Create the React component
    react_component = """
    <div id="root"></div>
    <script src="https://unpkg.com/react@17/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@17/umd/react-dom.production.min.js"></script>
    <script>
    const e = React.createElement;

    function AnnotatedText({ tokens }) {
        const [clickedWord, setClickedWord] = React.useState(null);
        
        const handleClick = (word) => {
            setClickedWord(word);
        };
        
        return e('div', null, [
            e('p', { key: 'text' },
                tokens.map((token, i) => {
                    if (Array.isArray(token)) {
                        const [word, label] = token;
                        return e('span', {
                            key: i,
                            className: 'clickable',
                            onClick: () => handleClick(word),
                            style: {
                                backgroundColor: '#d0e6f7',
                                padding: '2px 6px',
                                margin: '0 2px',
                                borderRadius: '5px',
                                cursor: 'pointer'
                            }
                        }, word);
                    }
                    return e('span', { key: i }, token);
                })
            ),
            clickedWord && e('p', {
                key: 'output',
                style: { marginTop: '1rem', fontWeight: 'bold' }
            }, `You clicked: ${clickedWord}`)
        ]);
    }

    const tokens = %s;
    
    ReactDOM.render(
        e(AnnotatedText, { tokens: tokens }),
        document.getElementById('root')
    );
    </script>
    """
    
    # Convert the tokens list to a JavaScript array representation
    js_tokens = []
    for token in tokens:
        if isinstance(token, tuple):
            js_tokens.append([token[0], token[1]])  # Convert tuple to list for JSON serialization
        else:
            js_tokens.append(token)
    
    import json
    component_html = react_component % json.dumps(js_tokens)
    
    # Render the React component with reduced height
    components.html(component_html, height=100)

# Render everything
render_annotated([
    "This ",
    ("is a man", "1"),
    " some ",
    ("annotated", "Adj"),
    ("text", "Noun"),
    " for those of ",
    ("you", "Pronoun"),
    " who ",
    ("like", "Verb"),
    " this sort of ",
    ("thing", "Noun"),
    ". ",
    "And here's a ",
    ("word", ""),
    " with a fancy background but no label.",
])

# --- 4. Render UI Components & Handle Logic ---
with st.container(border=True):
    input_language, output_language, sync_button_was_clicked = render_top_form_selectors()


# Render the translation text areas
# Update session state with the current content of the input text area
    st.session_state.input_text_content = Input_text_area(
        input_value=st.session_state.input_text_content
        
    )

with st.container(border=True):
    st.session_state.output_text_content = Output_text_area(
        input_value=st.session_state.input_text_content
    )

# --- 5. Handle Translation Trigger ---
# Check if the sync button was clicked (status is managed in session state by the component)


# --- 6. Final UI Elements ---
st.divider()

st.info("Translation will be processed here based on the selected languages and input text. ")



# import panel as pn
# pn.extension()

# sentence = "An 80-year-long study shows that good interpersonal relationships can make a person happier and healthier."

# ALT_PHRASES = {
#     "An 80-year-long study": [
#         "An 80-year-long study",
#         "A study of 80 years",
#         "An 8-decade-long research"
#     ],
#     "good interpersonal relationships": [
#         "good interpersonal relationships",
#         "strong social bonds",
#         "healthy personal connections"
#     ]
# }

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
