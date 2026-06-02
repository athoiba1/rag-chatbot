import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 RAG Chatbot")

# Sidebar
with st.sidebar:
    st.header("📄 Document Upload")
    uploaded_file = st.file_uploader("Upload a document", type=["pdf", "txt", "md"])

    if uploaded_file and st.button("Process Document"):
        with st.spinner("Processing..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            resp = requests.post(f"{API_URL}/upload", files=files)
            if resp.status_code == 200:
                data = resp.json()
                st.success(f"✅ Processed {data['chunks']} chunks from {data['filename']}")
            else:
                st.error(f"Error: {resp.json().get('detail', 'Unknown error')}")

    st.divider()
    stats = requests.get(f"{API_URL}/stats").json()
    st.metric("Total Chunks", stats.get("total_chunks", 0))

# Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "sources" in msg and msg["sources"]:
            with st.expander("📎 Sources"):
                for src in msg["sources"]:
                    st.write(f"**{src['source']}** (Page {src.get('page', 'N/A')})")
                    st.caption(src["preview"])

if query := st.chat_input("Ask a question about your documents"):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            history = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages[:-1]
            ]
            resp = requests.post(
                f"{API_URL}/chat",
                json={"query": query, "chat_history": history},
            )

            if resp.status_code == 200:
                data = resp.json()
                st.write(data["answer"])

                if data["sources"]:
                    with st.expander("📎 Sources"):
                        for src in data["sources"]:
                            st.write(f"**{src['source']}** (Page {src.get('page', 'N/A')})")
                            st.caption(src["preview"])

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data["answer"],
                    "sources": data["sources"],
                })
            else:
                error = resp.json().get("detail", "Unknown error")
                st.error(f"Error: {error}")
