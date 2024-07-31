import streamlit as st
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@st.cache_resource
def chatbot():
    instructions = """You are an assistant."""
    base_prompt = hub.pull("langchain-ai/openai-functions-template")
    prompt = base_prompt.partial(instructions=instructions)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tavily_tool = TavilySearchResults()
    tools = [tavily_tool, multiply]
    agent = create_openai_functions_agent(llm, tools, prompt)
    chatbot = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
    )
    return chatbot


def build_history():
    return [
        HumanMessage(content=msg["content"])
        if msg["role"] == "user"
        else AIMessage(content=msg["content"])
        for msg in st.session_state.get("messages", [])
    ]


st.markdown('# Chatbot con acceso a buscador!!!!')


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
