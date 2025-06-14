import streamlit as st
import requests

st.set_page_config(page_title="PDF QA Assistant")

st.title("📄 PDF Q&A with AI")

BACKEND_URL = "http://localhost:8000"

uploaded = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded:
    with st.spinner("Uploading and processing PDF..."):
        res = requests.post(f"{BACKEND_URL}/upload", files={"pdf": uploaded.getvalue()})
        if res.status_code == 200:
            st.success(f"✅ PDF processed into {res.json()['chunks']} chunks!")
        else:
            st.error("❌ Failed to process PDF")

q = st.text_input("Ask a question about the PDF")
if st.button("Ask") and q:
    with st.spinner("Getting answer from AI..."):
        res = requests.get(f"{BACKEND_URL}/ask", params={"q": q})
        st.write("📦 Raw backend response:", res.text)
        try:
            data = res.json()
            if "answer" in data:
                st.success("✅ Here's the answer:")
                st.write(data["answer"])
            else:
                st.error(f"⚠️ Error from backend: {data.get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Failed to parse backend response: {e}")
