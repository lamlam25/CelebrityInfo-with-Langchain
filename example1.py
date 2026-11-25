from langchain_ollama import ChatOllama
import streamlit as st
from langchain import PromptTemplate
from langchain_classic.chains import LLMChain


st.title("LangChain with Ollama")
input_text = st.text_input("Search the topic you want")

llm = ChatOllama(model="llama3.2", temperature=0.8)
prompt = PromptTemplate(
    input_variables=["input_text"],
    template="You are a helpful assistant. Answer the following question: {input_text}"
)
chain = LLMChain(llm=llm, prompt=prompt,verbose=True)


if input_text:
    st.write(llm.invoke(prompt.format(input_text=input_text) ).content)