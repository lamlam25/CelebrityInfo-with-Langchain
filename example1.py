from langchain_ollama import ChatOllama
import streamlit as st

st.title("LangChain with Ollama")
input_text = st.text_input("Search the topic you want")

llm = ChatOllama(model="llama3.2", temperature=0.8)

if input_text:
    st.write(llm.invoke(input_text).content)