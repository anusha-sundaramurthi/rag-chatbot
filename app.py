"""
Streamlit Chat UI for the Everstorm Outfitters RAG chatbot.

Run from the project root:
    streamlit run app.py
"""

import streamlit as st
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="TempestTrial Support",
    page_icon="⛰️",
    layout="centered",
)
st.title("⛰️ TempestTrial Outfitters – Customer Support")
st.caption("Ask me anything about orders, shipping, returns, or products.")

# ── Load resources (cached so they only load once) ───────────
SYSTEM_TEMPLATE = """
You are a **Customer Support Chatbot** for Everstorm Outfitters.
Use ONLY the information in CONTEXT to answer.
If the answer is not there, say "I'm not sure from the docs."

Rules:
1) Use ONLY the provided <context>.
2) If not in context: "I don't know based on the retrieved documents."
3) Be concise. Quote key phrases when helpful.
4) Cite sources as [source: <filename>] when metadata is available.

CONTEXT:
{context}

USER:
{question}
"""

@st.cache_resource(show_spinner="Loading knowledge base …")
def load_chain():
    embedder  = SentenceTransformerEmbeddings(model_name="thenlper/gte-small")
    vectordb  = FAISS.load_local("faiss_index", embedder, allow_dangerous_deserialization=True)
    retriever = vectordb.as_retriever(search_kwargs={"k": 8})

    llm = Ollama(model="gemma3:1b", temperature=0.1)

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=SYSTEM_TEMPLATE,
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        combine_docs_chain_kwargs={"prompt": prompt},
        return_source_documents=True,
        verbose=False,
    )
    return chain

chain = load_chain()

# ── Session state ────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []          # [{role, content}, …]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []      # [(question, answer), …]

# ── Render existing messages ─────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Chat input ───────────────────────────────────────────────
if user_input := st.chat_input("Type your question here …"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Run RAG chain
    with st.chat_message("assistant"):
        with st.spinner("Thinking …"):
            result = chain({
                "question": user_input,
                "chat_history": st.session_state.chat_history,
            })
            answer = result["answer"]
            sources = result.get("source_documents", [])

        st.markdown(answer)

        # Show collapsed sources
        if sources:
            with st.expander("📄 Retrieved context chunks"):
                for doc in sources:
                    src = doc.metadata.get("source", "unknown")
                    st.markdown(f"**Source:** `{src}`")
                    st.markdown(doc.page_content)
                    st.divider()

    # Persist to session state
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.chat_history.append((user_input, answer))