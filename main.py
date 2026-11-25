import os

from constants import openai_key
from langchain_openai import ChatOpenAI
import streamlit as st

os.environ["OPENAI_API_KEY"] = openai_key

st.title("LangChain with OpenAI API Key Integration")
input_text = st.text_input("Search the topic you want")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)

if input_text:
    st.write(llm.invoke(input_text).content)
    
