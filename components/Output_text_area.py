import streamlit as st
import ast
import time
from annotated_text import annotated_text
import streamlit.components.v1 as components
import streamlit as st
from typing import List, Union, Tuple, Sequence

from testing_and_research.p4_alt_builder import alt_builder


from testing_and_research.p4_alt_builder import alt_builder


# Simulated "streaming" function
def stream_data(text):
    full_text = ""
    for word in text.split(" "):
        full_text += word + " "
        yield full_text
        time.sleep(0.01)


def render_annotated(tokens: Sequence[Union[str, Tuple[str, str]]], alt_phrases: dict):
    import json
    js_tokens = []
    for token in tokens:
        if isinstance(token, tuple):
            js_tokens.append([token[0], token[1]])
        else:
            js_tokens.append(token)
    tokens_json = json.dumps(js_tokens)
    alt_phrases_json = json.dumps(alt_phrases)

    react_component = f"""
    <div id=\"root\"></div>
    <script src=\"https://unpkg.com/react@17/umd/react.production.min.js\"></script>
    <script src=\"https://unpkg.com/react-dom@17/umd/react-dom.production.min.js\"></script>
    <script>
    const e = React.createElement;

    function AnnotatedText({{ tokens: initialTokens, altPhrases: initialAltPhrases }}) {{
        const [tokens, setTokens] = React.useState(initialTokens);
        const [altPhrases, setAltPhrases] = React.useState(initialAltPhrases);
        const [selectedChunkIndex, setSelectedChunkIndex] = React.useState(0);

        const handleAlternativeClick = (newWord) => {{
            const newTokens = tokens.map((token, i) =>
                i === selectedChunkIndex ? [newWord, token[1]] : token
            );
            setTokens(newTokens);
            // Advance to next chunk, or stay on current if it's the last one
            if (selectedChunkIndex < tokens.length - 1) {{
                setSelectedChunkIndex(selectedChunkIndex + 1);
            }}
            setTimeout(() => {{
                window.parent.postMessage({{
                    type: 'setFrameHeight',
                    height: document.body.scrollHeight
                }}, '*');
            }}, 0);
        }};

        const handleChunkClick = (index) => {{
            setSelectedChunkIndex(selectedChunkIndex === index ? null : index);
            setTimeout(() => {{
                window.parent.postMessage({{
                    type: 'setFrameHeight',
                    height: document.body.scrollHeight
                }}, '*');
            }}, 0);
        }};

        const renderAlternatives = () => {{
            if (selectedChunkIndex === null) return null;
            const chunkText = tokens[selectedChunkIndex][0];
            if (!altPhrases || !altPhrases[chunkText]) return null;
            return e('div', {{
                style: {{
                    marginTop: '0.5rem',
                    padding: '8px',
                    backgroundColor: '#f0f7ff',
                    borderRadius: '5px'
                }}
            }}, [
                e('div', {{ style: {{ fontWeight: 'bold', marginBottom: '4px' }} }}, 'Alternative phrases:'),
                ...altPhrases[chunkText].map((alt, i) =>
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
                height: 'auto',
                padding: '5px 0px 20px 0px',
                width: '100%',
                backgroundColor: '#ffffff',
                borderRadius: '8px'
            }}
        }}, [
            e('p', {{
                key: 'text',
                style: {{
                    fontSize: '18px',
                    lineHeight: '2.0',
                    margin: '0 0 20px 0'
                }}
            }},
                tokens.map((token, i) => {{
                    if (Array.isArray(token)) {{
                        const [word, label] = token;
                        const isSelected = selectedChunkIndex === i;
                        const bgColor = isSelected ? '#ffe066' : '#d0e6f7'; // yellow if selected, blue otherwise
                        return e('span', {{
                            key: i,
                            className: 'clickable',
                            onClick: () => handleChunkClick(i),
                            style: {{
                                backgroundColor: bgColor,
                                padding: '4px 8px',
                                margin: '0 4px',
                                borderRadius: '5px',
                                cursor: 'pointer',
                                fontWeight: isSelected ? 'bold' : 'normal',
                                transition: 'background-color 0.2s'
                            }}
                        }}, word);
                    }}
                    return e('span', {{ key: i }}, token);
                }})
            ),
            renderAlternatives()
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

    components.html(react_component, height=250, scrolling=True)


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
