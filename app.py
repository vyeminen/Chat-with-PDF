import streamlit as st
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from htmlTemplates import css, bot_template, user_template




def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_content = PdfReader(pdf)
        for page in pdf_content.pages:
            text += page.extract_text()

    return text

def get_text_chunks(raw_pdf_text):
    text_spliter = CharacterTextSplitter(
        separator= "\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )

    chunks = text_spliter.split_text(raw_pdf_text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name = 'hkunlp/instructor-xl')
    vectorstore = FAISS.from_texts(texts = text_chunks, embedding = embeddings)
    return vectorstore

def get_conversation_chain(vector_store):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory= memory
    )
    return conversation_chain

def handle_user_input(user_question):
    response = st.session_state.conversation({'question':user_question})
    st.session_state.chat_history = response['chat_history']
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            usr = st.chat_message("user")
            usr.write(message.content)
        else:
            robot = st.chat_message("assistant")
            robot.write(message.content)
            


def main():
    st.set_page_config(page_title="Chat with PDF", page_icon=":books:")
    header = st.container()
    header.title("Chat with PDF :books:")
    header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)
    st.write(css, unsafe_allow_html= True)
    user_question = st.chat_input()


    if user_question:
        handle_user_input(user_question)

    

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = None

    with st.sidebar:
        st.sidebar.title("Chat with PDF :books:")
        OPENAI_API_KEY = st.text_input("Enter your OPENAI_API_KEY:")
        if st.button("Enter"):
            os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
        
        st.subheader("Your Documents")
        pdf_docs = st.file_uploader("Upload your PDF here...", accept_multiple_files=True)

        if st.button("Process"):
            with st.spinner("Processing...."):
                #get text from the pdf
                raw_pdf_text = get_pdf_text(pdf_docs)

                #get text chunks
                text_chunks = get_text_chunks(raw_pdf_text)
                

                #create vector store
                vector_store = get_vectorstore(text_chunks)

                #conversation chain creation
                st.session_state.conversation = get_conversation_chain(vector_store)
if __name__ == "__main__":
    main()