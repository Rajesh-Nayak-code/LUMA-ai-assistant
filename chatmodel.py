import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

st.set_page_config(
    page_title="Luma AI",
    layout="centered"
)

st.title("LUMA AI",text_alignment="center")
st.caption("YOUR AI ASSISTANT")

model = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0.9,
    max_tokens=300
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(
            content="You are an AI assistant that summarizes the user's content."
        )
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Type your message...")

if prompt:

    st.session_state.chat_history.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(HumanMessage(content=prompt))

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            response = model.invoke(st.session_state.messages)

            st.markdown(response.content)

    st.session_state.messages.append(
        AIMessage(content=response.content)
    )

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": response.content,
        }
    )
