import streamlit as st
from groq import Groq
import json, os
from datetime import date, datetime
import pandas as pd
import plotly.express as px

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

def get_ai_tip(api_key, mood, energy, note):
    client = Groq(api_key=api_key)
    prompt = f"""A student is feeling {mood} with energy level {energy}/10. They said: "{note or 'nothing extra'}".
Give them 3 specific, actionable study tips for right now. Be warm, brief, and practical. Use emojis."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
    )
    return response.choices[0].message.content

def show(api_key, username):
    st.title("😊 Mood & Stress Tracker")
    path = f"data/{username}_moods.json"
    moods = load_json(path, [])

    with st.form("mood_form", clear_on_submit=True):
        c1,c2 = st.columns(2)
        mood_choice  = c1.selectbox("Current Mood", ["😊 Happy","😰 Stressed","😴 Tired"])
        energy_level = c2.slider("Energy Level (1-10)", 1, 10, 5)
        note = st.text_input("Anything on your mind? (optional)")
        submitted = st.form_submit_button("💾 Log Mood + Get AI Tips", use_container_width=True)

        if submitted:
            entry = {
                "date":   str(date.today()),
                "time":   datetime.now().strftime("%H:%M"),
                "mood":   mood_choice.split()[1],
                "emoji":  mood_choice.split()[0],
                "energy": energy_level,
                "note":   note,
            }
            moods.append(entry)
            save_json(path, moods)
            with st.spinner("AI is generating personalised tips..."):
                tip = get_ai_tip(api_key, entry["mood"], energy_level, note)
                st.session_state[f"{username}_mood_tip"] = tip
            st.success("Mood logged! 🎉")

    if tip := st.session_state.get(f"{username}_mood_tip"):
        st.markdown("---")
        st.markdown("### 💡 AI Study Tips For You Right Now")
        st.markdown(f'<div class="tip-box">{tip}</div>', unsafe_allow_html=True)

    moods = load_json(path, [])
    if not moods:
        st.info("Log your first mood above!")
        return

    st.markdown("---")
    st.markdown("### 📋 Mood History")
    df = pd.DataFrame(moods[-20:][::-1])
    st.dataframe(df[["date","time","emoji","mood","energy"]], use_container_width=True, hide_index=True)

    if len(moods) >= 3:
        st.markdown("### 📈 Mood Trend")
        df_all = pd.DataFrame(moods)
        df_all["score"] = df_all["mood"].map({"Happy":3,"Stressed":1,"Tired":2})
        fig = px.line(df_all, x="date", y="score", markers=True,
                      color_discrete_sequence=["#667eea"],
                      labels={"score":"Mood (1=Stressed,2=Tired,3=Happy)","date":"Date"})
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
