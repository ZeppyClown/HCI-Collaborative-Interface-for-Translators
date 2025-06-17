import streamlit as st
import time
from annotated_text import annotated_text
import streamlit.components.v1 as components
import streamlit as st
from typing import List, Union, Tuple

# Simulated "streaming" function
def stream_data(text):
    full_text = ""
    for word in text.split(" "):
        full_text += word + " "
        yield full_text
        time.sleep(0.01)

def render_annotated(tokens: List[Union[str, Tuple[str, str]]], alt_phrases: dict):
    # Convert the tokens list to a JavaScript array representation
    js_tokens = []
    for token in tokens:
        if isinstance(token, tuple):
            js_tokens.append([token[0], token[1]])
        else:
            js_tokens.append(token)
    
    import json
    tokens_json = json.dumps(js_tokens)
    alt_phrases_json = json.dumps(alt_phrases)
    
    # Create the React component with safe string formatting
    react_component = f"""
    <div id="root"></div>
    <script src="https://unpkg.com/react@17/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@17/umd/react-dom.production.min.js"></script>
    <script>
    const e = React.createElement;

    function AnnotatedText({{ tokens: initialTokens, altPhrases: initialAltPhrases }}) {{
        const [tokens, setTokens] = React.useState(initialTokens);
        const [altPhrases, setAltPhrases] = React.useState(initialAltPhrases);
        const [clickedWord, setClickedWord] = React.useState(null);
        
        const handleClick = (word, index) => {{
            if (clickedWord === word) {{
                setClickedWord(word);
            }} else {{
                setClickedWord(word);
            }}
            setTimeout(() => {{
                window.parent.postMessage({{
                    type: 'setFrameHeight',
                    height: document.body.scrollHeight
                }}, '*');
            }}, 0);
        }};

        const handleAlternativeClick = (newWord) => {{
            const currentAlts = altPhrases[clickedWord];
            setAltPhrases(prev => ({{
                ...prev,
                [newWord]: currentAlts
            }}));
            const newTokens = tokens.map(token => {{
                if (Array.isArray(token) && token[0] === clickedWord) {{
                    return [newWord, token[1]];
                }}
                return token;
            }});
            setTokens(newTokens);
            setClickedWord(null);
        }};
        
        const renderAlternatives = (word) => {{
            if (!altPhrases || !altPhrases[word]) return null;
            return e('div', {{
                style: {{ 
                    marginTop: '0.5rem',
                    padding: '8px',
                    backgroundColor: '#f0f7ff',
                    borderRadius: '5px'
                }}
            }}, [
                e('div', {{ style: {{ fontWeight: 'bold', marginBottom: '4px' }} }}, 'Alternative phrases:'),
                ...altPhrases[word].map((alt, i) => 
                    e('div', {{ 
                        key: i,
                        onClick: () => handleAlternativeClick(alt),
                        style: {{ 
                            padding: '4px 8px',
                            margin: '2px 0',
                            backgroundColor: '#ffffff',
                            borderRadius: '3px',
                            cursor: 'pointer',
                            transition: 'background-color 0.2s'
                        }}
                    }}, alt)
                )
            ]);
        }};
        
        return e('div', {{
            style: {{
                padding: '20px',
                width: '100%',
                backgroundColor: '#ffffff',
                borderRadius: '8px',
                boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
            }}
        }}, [
            e('p', {{ 
                key: 'text',
                style: {{
                    fontSize: '18px',
                    lineHeight: '1.6',
                    margin: '0 0 20px 0'
                }}
            }},
                tokens.map((token, i) => {{
                    if (Array.isArray(token)) {{
                        const [word, label] = token;
                        return e('span', {{
                            key: i,
                            className: 'clickable',
                            onClick: () => handleClick(word, i),
                            style: {{
                                backgroundColor: '#d0e6f7',
                                padding: '4px 8px',
                                margin: '0 4px',
                                borderRadius: '5px',
                                cursor: 'pointer'
                            }}
                        }}, word);
                    }}
                    return e('span', {{ key: i }}, token);
                }})
            ),
            clickedWord && e('div', {{
                key: 'output',
                style: {{ 
                    marginTop: '1.5rem',
                    width: '100%',
                    maxHeight: '500px',
                    overflowY: 'auto'
                }}
            }}, [
                renderAlternatives(clickedWord)
            ])
        ]);
    }}

    const tokens = {tokens_json};
    const altPhrases = {alt_phrases_json};
    
    ReactDOM.render(
        e(AnnotatedText, {{ tokens: tokens, altPhrases: altPhrases }}),
        document.getElementById('root')
    );

    setTimeout(() => {{
        window.parent.postMessage({{
            type: 'setFrameHeight',
            height: document.body.scrollHeight
        }}, '*');
    }}, 0);
    </script>

    <style>
    .clickable:hover {{
        background-color: #a3d0f0 !important;
    }}
    </style>
    """
    
    # Start with minimum height and let it adjust dynamically
    components.html(react_component, height=250, scrolling=True)

# Main output function
def Output_text_area(input_value=""):
    if "translation_output" not in st.session_state:
        st.session_state.translation_output = ""

    if st.session_state.get("sync_button_clicked_status", False):
        sentence = input_value # value user typed in
        
        # Define the tokens and their alternatives together
        tokens = [
            "",
            ("An 80-year-long study", "1"),
            ("shows that good interpersonal relationships ", "2"),
            "can make a person ",
            ("happier", "3"),
            " and ",
            ("healthier", "4")
        ]
        
        alt_phrases = {
            "An 80-year-long study": [
                "An 80-year-long study",
                "A study of 80 years",
                "An 8-decade-long research"
            ],
            "shows that good interpersonal relationships ": [
                "shows that good interpersonal relationships ",
                "demonstrates that strong social bonds ",
                "reveals that healthy personal connections "
            ],
            "happier": [
                "happier",
                "more joyful",
                "more content"
            ],
            "healthier": [
                "healthier",
                "more healthy",
                "in better health"
            ]
        }
        
        # Pass both tokens and alt_phrases to render_annotated
        render_annotated(tokens, alt_phrases)

        st.session_state.sync_button_clicked_status = False
        # st.success("Translation completed!")
    
    return input_value
