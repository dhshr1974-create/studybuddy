import streamlit as st
from groq import Groq
import fitz

def extract_text(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "\n".join(page.get_text() for page in doc)

def ask_question(api_key, context, history, question):
    client = Groq(api_key=api_key)
    messages = [{"role": "system", "content": f"""You are a helpful study assistant. Answer questions based on the following study material only.
Be clear, concise, and educational. If the answer isn't in the material, say so honestly.

STUDY MATERIAL:
{context[:5000]}"""}]
    messages += history
    messages.append({"role": "user", "content": question})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=1000,
    )
    return response.choices[0].message.content

def show(api_key, username):
    st.title("🧠 AI Study Q&A")
    st.markdown("Upload your notes or paste text, then ask any question about it!")

    with st.expander("📄 Load Study Material", expanded=not st.session_state.get(f"{username}_qa_context")):
        method = st.radio("How to load?", ["Upload PDF", "Paste Text"], horizontal=True)
        if method == "Upload PDF":
            pdf = st.file_uploader("Upload PDF", type=["pdf"])
            if pdf and st.button("Load PDF"):
                st.session_state[f"{username}_qa_context"] = extract_text(pdf)
                st.success("PDF loaded! Start asking questions below.")
        else:
            text = st.text_area("Paste your notes", height=150)
            if st.button("Load Text") and text:
                st.session_state[f"{username}_qa_context"] = text
                st.success("Text loaded!")

    context = st.session_state.get(f"{username}_qa_context", "")
    if not context:
        st.info("Load your study material above to begin.")
        return

    st.success(f"✅ Study material loaded ({len(context)} chars). Ask anything!")

    if f"{username}_qa_history" not in st.session_state:
        st.session_state[f"{username}_qa_history"] = []

    for msg in st.session_state[f"{username}_qa_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Ask a question about your notes...")
    if question:
        st.session_state[f"{username}_qa_history"].append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_question(api_key, context, st.session_state[f"{username}_qa_history"][:-1], question)
                st.markdown(answer)
        st.session_state[f"{username}_qa_history"].append({"role": "assistant", "content": answer})

    if st.session_state[f"{username}_qa_history"] and st.button("🗑️ Clear Chat"):
        st.session_state[f"{username}_qa_history"] = []
        st.rerun()
