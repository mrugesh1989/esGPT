import json
import os
import streamlit as st
import os.path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    ServiceContext,
    set_global_service_context

)
# from llama_index.embeddings.gradient import GradientEmbedding
# from llama_index.llms.gradient import GradientBaseModelLLM
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

os.environ['GRADIENT_ACCESS_TOKEN'] = 'ks1oZKzE7ogn1FmedMA37hvZbeI7DCbN'
os.environ['GRADIENT_WORKSPACE_ID'] =  '79558bfb-06a6-4ba1-93f5-56d16c9b0db6_workspace'
os.environ['OPENAI_API_KEY'] = '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'

st.set_page_config(page_title="HACKATHON@2024 pdf Q&A ", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)

st.title("WELCOME TO HACKATHON@2024 - Chat with the pdf docs using LlamaIndex")

if "conversation" not in st.session_state:
    st.session_state.conversation = None

if "activate_chat" not in st.session_state:
    st.session_state.activate_chat = True

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar = message['avatar']):
        st.markdown(message["content"])

# st.session_state.activate_chat == True

# check if storage already exists
PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    documents = SimpleDirectoryReader("./data/").load_data()
    # llm = GradientBaseModelLLM(
    # base_model_slug="llama2-7b-chat",
    # max_tokens=400,)
    llm = OpenAI(model="text-davinci-003")
    
    # embed_model = GradientEmbedding(
    #     gradient_access_token = os.environ["GRADIENT_ACCESS_TOKEN"],
    #     gradient_workspace_id = os.environ["GRADIENT_WORKSPACE_ID"],
    #     gradient_model_slug="bge-large",
    #     )
    embed_model = OpenAIEmbedding(model="text-embedding-3-large")
    # Settings.embed_model = embed_model
    # Settings.llm = llm
    # Settings.chunk_size = 512
    service_context = ServiceContext.from_defaults(
    llm = llm,
    embed_model = embed_model,
    chunk_size=256)

    set_global_service_context(service_context)
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)
    # index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
if "query_engine" not in st.session_state:
    st.session_state.query_engine = index.as_query_engine()
if st.session_state.activate_chat == True:
    if prompt := st.chat_input("Ask your question from the PDF?"):
        with st.chat_message("user", avatar = '👨🏻'):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", 
                                            "avatar" :'👨🏻',
                                            "content": prompt})

        query_index_placeholder = st.session_state.query_engine
        pdf_response = query_index_placeholder.query(prompt)
        cleaned_response = pdf_response.response
        with st.chat_message("assistant", avatar='🤖'):
            st.markdown(cleaned_response)
        st.session_state.messages.append({"role": "assistant", 
                                            "avatar" :'🤖',
                                            "content": cleaned_response})