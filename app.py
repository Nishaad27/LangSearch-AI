import os
import time
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain_community.tools import WikipediaQueryRun, ArxivQueryRun, DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from dotenv import load_dotenv
load_dotenv()
st.set_page_config(page_title="AI Chat Search", page_icon="🔍", layout="centered")


st.image("Logo.webp", width=250)


st.markdown(
    """
    <h1 style="text-align: center; color: var(--text-color, #4A90E2);">
        LangSearch - AI Search Assistant 🔍
    </h1>
    <hr style="border: 1px solid var(--border-color, #ddd);">
    """, 
    unsafe_allow_html=True
)



groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(api_key=groq_api_key, model="Llama3-8b-8192", streaming=True)


arxiv_api_wrapper = ArxivAPIWrapper(top_k_results=3, doc_content_chars_max=1000)
wiki_api_wrapper = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=1000)

arxiv = ArxivQueryRun(api_wrapper=arxiv_api_wrapper)
wiki = WikipediaQueryRun(api_wrapper=wiki_api_wrapper)
search = DuckDuckGoSearchRun(name="search")

tools = [arxiv, wiki, search]
search_agent = initialize_agent(
    llm=llm, tools=tools, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handling_parsing_errors=True
)


if "last_duckduckgo_query_time" not in st.session_state:
    st.session_state["last_duckduckgo_query_time"] = 0

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "Assistant", "content": "Hi! I am a chatbot and I can search the web. How can I help you? 😊"}
    ]


chat_container_style = """
    <style>
        .chat-container {
            max-width: 700px;
            margin: auto;
        }
        .user-msg {
            background-color: var(--user-bg, #d1e7fd);
            color: var(--user-text, #000);
            border-radius: 12px;
            padding: 10px;
            margin: 5px 0;
            text-align: left;
            max-width: 80%;
        }
        .assistant-msg {
            background-color: var(--assistant-bg, #ececec);
            color: var(--assistant-text, #000);
            border-radius: 12px;
            padding: 10px;
            margin: 5px 0;
            text-align: left;
            max-width: 80%;
        }
        @media (prefers-color-scheme: dark) {
            :root {
                --text-color: #ffffff;
                --border-color: #444;
                --user-bg: #3b5998;
                --user-text: #ffffff;
                --assistant-bg: #444;
                --assistant-text: #ffffff;
            }
        }
    </style>
"""
st.markdown(chat_container_style, unsafe_allow_html=True)

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg"><b>You:</b> {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-msg"><b>Assistant:</b> {msg["content"]}</div>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)


prompt = st.text_input("Ask me anything:", placeholder="What is your query?..", key="user_query")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Searching... Please wait."):
        try:
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
            search_query = (
    f"Provide a well-structured, informative, and detailed response to the following query. "
    f"Ensure clarity, use real-world examples, and explain step by step when necessary. "
    f"Whenever possible, ensure that the response is at least 250 words long to provide comprehensive insights. "
    f"If the topic is restricted, offer general knowledge with enough depth to reach the desired length: {prompt}"
)

            
            if "search" in tools:
                current_time = time.time()
                time_since_last_query = current_time - st.session_state["last_duckduckgo_query_time"]
                if time_since_last_query < 2:
                    wait_time = 2 - time_since_last_query
                    st.warning(f"⚠️ Rate limit for DuckDuckGo in place. Waiting for {wait_time:.2f} seconds...")
                    time.sleep(wait_time)
                st.session_state["last_duckduckgo_query_time"] = time.time()
            
            response = search_agent.run(search_query, callbacks=[st_cb])
            st.session_state.messages.append({"role": "Assistant", "content": response})
            st.markdown(f'<div class="assistant-msg"><b>Assistant:</b> {response}</div>', unsafe_allow_html=True)
        except ValueError as ve:
            error_msg = f"⚠️ Parsing Error: {ve}"
            st.error(error_msg)
            st.session_state.messages.append({"role": "Assistant", "content": error_msg})
        except Exception as e:
            error_msg = "🚨 Oops! Something went wrong. Please try again later."
            st.error(error_msg)
            st.session_state.messages.append({"role": "Assistant", "content": error_msg})

st.markdown(
    """
    <hr>
    <p style="text-align: center; color: grey;">Powered by <b>LangChain</b> | Built by Nishaad</p>
    """,
    unsafe_allow_html=True,
)
