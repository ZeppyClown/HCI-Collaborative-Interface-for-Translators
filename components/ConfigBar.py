import streamlit as st

def reset():
    st.session_state["input_text_content"] = ""
    st.session_state["processing"] = False

def ConfigBar():
    col1, col2 = st.columns(2)
    with st.container() as config_bar:
        with col1:
            options = st.selectbox(
                "Translate from:",
                ("Chinese(Simplified)", "Japanese", "Korean"),
                key="source_lang",
                placeholder="Select a language you want to translate to",
                on_change= reset
            )
            if not options:
                pass
            # else:
            # # st.write(f"Selected : **{options.upper()}**")
            #     print("SELECTED SOURCE LANGUAGE: ", st.session_state['source_lang'])

        with col2:
            option = st.selectbox(
                "Translate to:",
                ("English"),
                index=0,
                key="dest_lang",
                placeholder="Select a language you want to translate to",
                on_change=reset
            )
            if not option:
                pass
            # else:
            # #     st.write(f"Selected : **{option.upper()}**")
            #     print("SELECTED DEST LANGUAGE: ", st.session_state['dest_lang'])

    return config_bar
