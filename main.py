import streamlit as st
from backend.core import run_llm
from streamlit_chat import message

st.set_page_config(page_title="Labour Harassment Chatbot", page_icon="🤖")

st.header("Labour Harassment Chatbot")

prompt = st.text_input("Prompt", placeholder="Hi! I'm KIM, how can i help you?")

if (
        "chat_answers_history" not in st.session_state
        and "user_prompt_history" not in st.session_state
        and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []


def create_sources_string(source_urls: set[str]) -> str:
    if not source_urls:
        return ""

    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"

    for i, source in enumerate(sources_list):
        sources_string += f"{i + 1}. {source}\n"

    return sources_string


if prompt:
    with st.spinner("Generating response.."):
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )

    sources = set([doc.metadata["source"] for doc in generated_response["source"]])
    formatted_response = (
        f"{generated_response['result']}\n\n{create_sources_string(sources)}"
    )

    st.session_state["user_prompt_history"].append(prompt)
    st.session_state["chat_answers_history"].append(formatted_response)
    st.session_state["chat_history"].append(("human", prompt))
    st.session_state["chat_history"].append(("ai", generated_response["result"]))

if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(st.session_state["chat_answers_history"],
                                              st.session_state["user_prompt_history"]):
        # Mensajes del usuario
        st.markdown(f'<div style="background-color: #f1f1f1; padding: 10px; border-radius: 5px;">'
                    f'<strong>Me:</strong> {user_query}</div>', unsafe_allow_html=True)

        # Mensajes del AI
        st.markdown(f'<div style="background-color: #d9f9d9; padding: 10px; border-radius: 5px;">'
                    f'<strong>KIM:</strong> {generated_response}</div>', unsafe_allow_html=True)
