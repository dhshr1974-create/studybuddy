import streamlit as st
from groq import Groq
import json, os
from datetime import date

def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path) as f:
                content = f.read().strip()
                if not content: return default
                return json.loads(content)
        except: return default
    return default

def prioritize_tasks(api_key, tasks):
    client = Groq(api_key=api_key)
    task_list = "\n".join([
        f"- {t['title']} | Subject: {t.get('subject','?')} | Deadline: {t.get('deadline','?')} | Priority: {t.get('priority','?')}"
        for t in tasks
    ])
    prompt = f"""You are a study productivity coach. A student has these pending assignments:

{task_list}

Today is {date.today()}.

Please:
1. Re-rank them from most to least urgent
2. Give a short reason for each ranking
3. Suggest a practical study schedule for today

Be encouraging, practical, and concise. Use emojis."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
    )
    return response.choices[0].message.content

def show(api_key, username):
    st.title("📝 AI Task Prioritizer")
    st.markdown("AI analyzes your assignments and tells you exactly what to work on first!")

    tasks = load_json(f"data/{username}_tasks.json", [])
    pending = [t for t in tasks if not t.get("done")]

    if not pending:
        st.success("No pending tasks — you're all caught up! 🎉")
        return

    st.markdown(f"### You have **{len(pending)}** pending tasks:")
    for t in pending:
        try:
            days = (date.fromisoformat(t["deadline"]) - date.today()).days
            icon = "🔴" if days <= 2 else "🟡" if days <= 7 else "🟢"
        except: icon = "⚪"
        st.markdown(f"{icon} **{t['title']}** — {t.get('subject','')} — `{t.get('deadline','?')}`")

    st.markdown("---")
    if st.button("🤖 Let AI Prioritize My Tasks", use_container_width=True):
        with st.spinner("AI is analysing your workload..."):
            result = prioritize_tasks(api_key, pending)
            st.session_state[f"{username}_priority_result"] = result

    if result := st.session_state.get(f"{username}_priority_result"):
        st.markdown("---")
        st.markdown("### 🎯 AI Study Plan")
        st.markdown(f'<div class="tip-box">{result}</div>', unsafe_allow_html=True)
