# pip install streamlit langchain-core langgraph>0.2.27 langchain-groq
import os
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq

st.title('Chat Bot App')

os.environ["GROQ_API_KEY"] = st.secrets['my_cool_secrets']['GROQ_API_KEY']


model = ChatGroq(model='llama3-8b-8192')

# Steps for Deployment
## 1. requirements.txt
## 2. Taking care of secrets (Api Keys)
## 3. Make a Github Repo


# 1. Chat History -> List (Human, Ai)
# 2. User and LLM input inserted in Chat history
# 3. Invoke for the Model
# 4. Output message


# key (role) : value (user) | key(content) : value (content)

if "msgs" not in st.session_state:
    st.session_state.msgs = []

placeholder = "Typer Your message here."
prompt = "You are a helpful Assistant that knows alot about cars"


for message in st.session_state.msgs:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if query := st.chat_input(placeholder):
    st.session_state.msgs.append({'role': 'user', 'content' : query})


    with st.chat_message(query):
        st.markdown(query)

    full_msgs = [
        {'role': 'system', 'content': prompt},
    ] + [{'role': m['role'], 'content': m['content']} for m in st.session_state.msgs]

    with st.chat_message('assistant'):
        messages_for_groq = [
            HumanMessage(content=msg['content']) if msg['role'] == 'user'
            else AIMessage(content=msg['content']) for msg in full_msgs
        ]

        response = model.invoke(messages_for_groq)


        st.markdown(response.content)

    st.session_state.msgs.append({'role': 'assistant', 'content': response.content})