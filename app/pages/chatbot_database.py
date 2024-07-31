import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent
from langchain_core.messages import AIMessage, HumanMessage


@st.cache_resource
def chatbot():
    db_uri = "mysql+pymysql://myuser:mypassword@mysql:3306/mydatabase"
    db = SQLDatabase.from_uri(db_uri)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chatbot = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
    return chatbot


def build_history():
    return [
        HumanMessage(content=msg["content"])
        if msg["role"] == "user"
        else AIMessage(content=msg["content"])
        for msg in st.session_state.get("messages", [])
    ]


st.markdown('# Chatbot!!!!')


text = st.chat_input('Hola, ¿en qué puedo ayudarte?')

if "messages" not in st.session_state:
    st.session_state.messages = []

if text:
    st.session_state.messages.append({
        "role": "user",
        "content": text
    })
    response = chatbot().invoke({
        "input": text,
        "chat_history": build_history(),
    }
    )["output"]
    st.session_state.messages.append({
        "role": "🦄",
        "content": response
    })

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
