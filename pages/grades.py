import streamlit as st
from groq import Groq
import json, os
import pandas as pd
import plotly.express as px
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

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f: json.dump(data, f, indent=2, default=str)

def get_ai_feedback(api_key, grades):
    client = Groq(api_key=api_key)
    summary = "\n".join([f"{g['subject']} — {g['exam']}: {g['grade']}%" for g in grades])
    prompt = f"""A student has these grades:
{summary}

Please:
1. Identify their strongest and weakest subjects
2. Spot any worrying trends
3. Give 3 specific, actionable improvement tips
Be encouraging, practical, and concise. Use emojis."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
    )
    return response.choices[0].message.content

def show(api_key, username):
    st.title("📈 AI Grades Tracker")
    path = f"data/{username}_grades.json"
    grades = load_json(path, [])

    with st.expander("➕ Add Grade", expanded=not grades):
        with st.form("add_grade", clear_on_submit=True):
            c1,c2 = st.columns(2)
            subject   = c1.text_input("Subject *")
            exam      = c2.text_input("Exam / Assignment")
            c3,c4     = st.columns(2)
            grade     = c3.number_input("Grade (%)", 0, 100, 75)
            exam_date = c4.date_input("Date", value=date.today())
            notes     = st.text_input("Notes (optional)")
            if st.form_submit_button("Add Grade 📊", use_container_width=True):
                if not subject: st.warning("Enter a subject!")
                else:
                    grades.append({"subject":subject,"exam":exam,"grade":grade,"date":str(exam_date),"notes":notes})
                    save_json(path, grades)
                    st.success(f"Added: {subject} — {grade}% ✅")
                    st.rerun()

    if not grades:
        st.info("Add your first grade above!")
        return

    df = pd.DataFrame(grades)
    st.markdown("### 📋 All Grades")
    st.dataframe(df[["date","subject","exam","grade","notes"]], use_container_width=True, hide_index=True)

    st.markdown("### 📊 Average by Subject")
    avg = df.groupby("subject")["grade"].mean().reset_index()
    avg.columns = ["Subject","Average (%)"]
    avg["Average (%)"] = avg["Average (%)"].round(1)
    avg["Status"] = avg["Average (%)"].apply(lambda x: "🟢 Good" if x>=75 else "🟡 Okay" if x>=60 else "🔴 Needs Work")
    col1,col2 = st.columns(2)
    with col1: st.dataframe(avg, use_container_width=True, hide_index=True)
    with col2:
        fig = px.bar(avg, x="Subject", y="Average (%)", color="Average (%)",
                     color_continuous_scale=["#e74c3c","#f39c12","#27ae60"], range_color=[0,100])
        fig.add_hline(y=75, line_dash="dash", line_color="green", annotation_text="Target 75%")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    if st.button("🤖 Get AI Feedback on My Grades", use_container_width=True):
        with st.spinner("AI is analysing your performance..."):
            feedback = get_ai_feedback(api_key, grades)
            st.session_state[f"{username}_grade_feedback"] = feedback

    if fb := st.session_state.get(f"{username}_grade_feedback"):
        st.markdown("### 🎯 AI Performance Analysis")
        st.markdown(f'<div class="tip-box">{fb}</div>', unsafe_allow_html=True)

    if st.button("🗑️ Clear All Grades", type="secondary"):
        save_json(path, [])
        st.rerun()
