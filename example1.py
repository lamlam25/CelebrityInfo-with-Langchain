import streamlit as st
from langchain_classic.chains import LLMChain
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama


st.set_page_config(page_title="Celebrity Khobor")
st.title("Celebrity Khobor")
st.write("Discover celebrity profiles, birth details, and career milestones.")
st.caption("AI-generated information may be incomplete or out of date. Verify important facts.")

if "celebrity_memory" not in st.session_state:
    st.session_state["celebrity_memory"] = ConversationBufferMemory(
        memory_key="chat_history",
        input_key="profile",
        output_key="celebrity_news",
    )
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = []

if st.button("Clear chat"):
    st.session_state["celebrity_memory"].clear()
    st.session_state["chat_messages"].clear()
    st.rerun()

for message in st.session_state["chat_messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

llm = ChatOllama(model="llama3.2", temperature=0.2)

identify_prompt = PromptTemplate(
    input_variables=["celebrity_name"],
    template=(
        "Identify the celebrity named {celebrity_name}. Return their commonly "
        "known full name. If the name is ambiguous, briefly say more detail is needed."
    ),
)
identify_chain = LLMChain(
    llm=llm,
    prompt=identify_prompt,
    output_key="person",
)

birth_prompt = PromptTemplate(
    input_variables=["person"],
    template=(
        "For this celebrity, {person}, give their birth date and birthplace if known. "
        "Start with their name, and do not guess if the details are unknown."
    ),
)
birth_chain = LLMChain(
    llm=llm,
    prompt=birth_prompt,
    output_key="profile",
)

achievements_prompt = PromptTemplate(
    input_variables=["profile", "chat_history"],
    template=(
        "Previous chat:\n{chat_history}\n\n"
        "Create a Celebrity Khobor profile using this information:\n{profile}\n\n"
        "Include the celebrity's name and birth information, then list five major "
        "career milestones. Label completed milestones as 'Achieved'. Include a "
        "future item only if it is officially announced, label it 'Confirmed upcoming', "
        "and never describe it as already achieved. Do not predict or invent facts. "
        "If you cannot provide five reliable milestones, say so instead of making them up."
    ),
)
achievements_chain = LLMChain(
    llm=llm,
    prompt=achievements_prompt,
    output_key="celebrity_news",
    memory=st.session_state["celebrity_memory"],
)

celebrity_name = st.chat_input("Ask about a celebrity")
if celebrity_name and celebrity_name.strip():
    celebrity_name = celebrity_name.strip()
    st.session_state["chat_messages"].append(
        {"role": "user", "content": celebrity_name}
    )
    with st.chat_message("user"):
        st.markdown(celebrity_name)
    with st.chat_message("assistant"):
        with st.spinner("Preparing celebrity news..."):
            person = identify_chain.run(celebrity_name)
            birth_information = birth_chain.run(person)
            profile = (
                f"User request: {celebrity_name}\n\n"
                f"Celebrity profile: {birth_information}"
            )
            result = achievements_chain.run(profile)
        with st.expander("Celebrity Khobor response", expanded=True):
            st.markdown(result)
    st.session_state["chat_messages"].append(
        {"role": "assistant", "content": result}
    )
