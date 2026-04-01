import streamlit as st
from groq import Groq
import fitz
import json

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "\n".join(page.get_text() for page in doc)

def generate_flashcards(api_key, text, num_cards):
    client = Groq(api_key=api_key)
    prompt = f"""You are a study assistant. Based on the following text, generate exactly {num_cards} flashcards.
Respond ONLY with a valid JSON array like this:
[
  {{"question": "What is X?", "answer": "X is ..."}},
  ...
]
No explanation, no markdown, just the JSON array.

TEXT:
{text[:4000]}"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
    )
    raw = response.choices[0].message.content.strip().replace("```json","").replace("```","").strip()
    return json.loads(raw)

def show(api_key, username):
    st.title("📄 AI Flashcard Generator")
    st.markdown("Upload a PDF or paste your notes — AI will generate flashcards instantly!")

    input_method = st.radio("Input method", ["📄 Upload PDF", "📝 Paste Text"], horizontal=True)
    text = ""
    if input_method == "📄 Upload PDF":
        pdf = st.file_uploader("Upload your PDF", type=["pdf"])
        if pdf:
            with st.spinner("Reading PDF..."):
                text = extract_text_from_pdf(pdf)
            st.success(f"PDF loaded! ({len(text)} characters extracted)")
    else:
        text = st.text_area("Paste your notes here", height=200)

    num_cards = st.slider("Number of flashcards", 5, 20, 10)

    if st.button("✨ Generate Flashcards", use_container_width=True, disabled=not text):
        with st.spinner("AI is generating your flashcards..."):
            try:
                cards = generate_flashcards(api_key, text, num_cards)
                st.session_state[f"{username}_flashcards"] = cards
                st.success(f"Generated {len(cards)} flashcards! 🎉")
            except Exception as e:
                st.error(f"Error: {e}")

    cards = st.session_state.get(f"{username}_flashcards", [])
    if cards:
        st.markdown("---")
        st.markdown("### 🃏 Your Flashcards")
        st.caption("Click a card to reveal the answer!")
        for i, card in enumerate(cards):
            with st.expander(f"Card {i+1}: {card['question']}"):
                st.markdown(f"**Answer:** {card['answer']}")
        flashcard_text = "\n\n".join([f"Q: {c['question']}\nA: {c['answer']}" for c in cards])
        st.download_button("📥 Download Flashcards", flashcard_text, file_name="flashcards.txt")
