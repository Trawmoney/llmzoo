import openai
import streamlit as st

st.title("🎆Mistral Chat")

openai.api_base = "https://api.fireworks.ai/inference/v1"
openai.api_key = "ku9UYtzjSAATlcAstO8yrB89MzvDqJL3lGIkNgnVZ7URxPxK"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "accounts/fireworks/models/llama-v2-7b-chat"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("🪅"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
