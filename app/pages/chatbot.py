import streamlit as st
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_community.agent_toolkits import create_sql_agent
from langchain.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@st.cache_resource
def chatbot_DB():
    db_uri = "mysql+pymysql://myuser:mypassword@mysql:3306/mydatabase"
    db = SQLDatabase.from_uri(db_uri)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chatbot = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
    return chatbot


@tool
def database_tool(query: str) -> str:
    """Query the database. Use this tool to call an AI that will query the database for you.

    Args:
        query (str): The query to run in natural language form.
    """
    return chatbot_DB().invoke({"input": query, })["output"]


@st.cache_resource
def chatbot():
    instructions = """You are an assistant."""
    base_prompt = hub.pull("langchain-ai/openai-functions-template")
    prompt = base_prompt.partial(instructions=instructions)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tavily_tool = TavilySearchResults()
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(lang="es"))
    tools = [tavily_tool, multiply, database_tool,wikipedia]
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
