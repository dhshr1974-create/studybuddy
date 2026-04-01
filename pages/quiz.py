import streamlit as st
from groq import Groq
import fitz
import json

def extract_text(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "\n".join(page.get_text() for page in doc)

def generate_quiz(api_key, text, num_questions):
    client = Groq(api_key=api_key)
    prompt = f"""Generate {num_questions} multiple choice quiz questions from this text.
Respond ONLY with a valid JSON array. No markdown, no explanation. Format:
[
  {{
    "question": "...",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "correct": "A",
    "explanation": "Brief explanation why A is correct"
  }}
]

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
    st.title("❓ AI Quiz Generator")
    st.markdown("Upload your notes and AI will test your knowledge!")

    method = st.radio("Input method", ["Upload PDF", "Paste Text"], horizontal=True)
    text = ""
    if method == "Upload PDF":
        pdf = st.file_uploader("Upload PDF", type=["pdf"])
        if pdf:
            text = extract_text(pdf)
            st.success("PDF loaded!")
    else:
        text = st.text_area("Paste your notes", height=200)

    num_q = st.slider("Number of questions", 3, 15, 5)

    if st.button("🎯 Generate Quiz", use_container_width=True, disabled=not text):
        with st.spinner("Generating your quiz..."):
            try:
                quiz = generate_quiz(api_key, text, num_q)
                st.session_state[f"{username}_quiz"] = quiz
                st.session_state[f"{username}_answers"] = {}
                st.session_state[f"{username}_submitted"] = False
                st.success(f"Quiz ready! {len(quiz)} questions generated.")
            except Exception as e:
                st.error(f"Error: {e}")

    quiz = st.session_state.get(f"{username}_quiz", [])
    if not quiz: return

    st.markdown("---")
    st.markdown("### 📝 Answer the Questions")
    answers  = st.session_state.get(f"{username}_answers", {})
    submitted = st.session_state.get(f"{username}_submitted", False)

    for i, q in enumerate(quiz):
        st.markdown(f"**Q{i+1}. {q['question']}**")
        selected = st.radio("", q.get("options",[]), key=f"q_{i}", index=None, disabled=submitted)
        if selected: answers[i] = selected[0]
        st.session_state[f"{username}_answers"] = answers
        if submitted:
            correct = q.get("correct","")
            if answers.get(i,"") == correct:
                st.success(f"✅ Correct! {q.get('explanation','')}")
            else:
                st.error(f"❌ Wrong. Correct: {correct}. {q.get('explanation','')}")
        st.markdown("---")

    if not submitted:
        if st.button("📊 Submit Quiz", use_container_width=True):
            st.session_state[f"{username}_submitted"] = True
            st.rerun()
    else:
        correct_count = sum(1 for i,q in enumerate(quiz) if answers.get(i,"") == q.get("correct",""))
        pct = int(correct_count/len(quiz)*100)
        emoji = "🏆" if pct>=80 else "👍" if pct>=60 else "📚"
        st.markdown(f"## {emoji} Score: {correct_count}/{len(quiz)} ({pct}%)")
        if st.button("🔄 Retake Quiz"):
            st.session_state[f"{username}_answers"] = {}
            st.session_state[f"{username}_submitted"] = False
            st.rerun()
