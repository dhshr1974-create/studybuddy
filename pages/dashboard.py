import streamlit as st
import json, os
from datetime import date

def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path) as f:
                content = f.read().strip()
                if not content:
                    return default
                return json.loads(content)
        except Exception:
            return default
    return default

def show(username):
    st.title("🏠 Dashboard")
    tasks = load_json(f"data/{username}_tasks.json", [])
    moods = load_json(f"data/{username}_moods.json", [])
    grades = load_json(f"data/{username}_grades.json", [])

    done    = [t for t in tasks if t.get("done")]
    pending = [t for t in tasks if not t.get("done")]
    pct     = int(len(done)/len(tasks)*100) if tasks else 0

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(f'<div class="metric-card"><h2>{len(tasks)}</h2><p>Total Tasks</p></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-card" style="background:linear-gradient(135deg,#11998e,#38ef7d)"><h2>{len(done)}</h2><p>Completed</p></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-card" style="background:linear-gradient(135deg,#f7971e,#ffd200)"><h2>{len(pending)}</h2><p>Pending</p></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="metric-card" style="background:linear-gradient(135deg,#e96c6c,#b06ab3)"><h2>{pct}%</h2><p>Completion</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ⏰ Upcoming Deadlines")
        upcoming = sorted([t for t in pending if t.get("deadline")], key=lambda x: x["deadline"])[:5]
        if upcoming:
            for t in upcoming:
                days = (date.fromisoformat(t["deadline"]) - date.today()).days
                icon = "🔴" if days <= 1 else "🟡" if days <= 7 else "🟢"
                st.markdown(f"{icon} **{t['title']}** — `{t['deadline']}`")
        else:
            st.success("No upcoming deadlines! 🎉")

    with col2:
        st.markdown("### 📈 Recent Grades")
        if grades:
            for g in grades[-5:][::-1]:
                st.markdown(f"📘 **{g['subject']}** — {g['grade']}% `{g.get('exam','')}`")
        else:
            st.info("No grades logged yet.")

    if moods:
        latest = moods[-1]
        tips = {
            "Happy":   ["🚀 Tackle your hardest subject first!", "🎯 Set a stretch goal today."],
            "Stressed":["🌬️ Try box breathing: 4s in, 4s hold, 4s out.", "✂️ Break your task into 3 tiny steps."],
            "Tired":   ["💧 Drink water before anything else.", "😴 A 20-min power nap beats 2hrs of drowsy study."],
        }
        import random
        mood_tips = tips.get(latest["mood"], tips["Happy"])
        st.markdown("---")
        st.markdown("### 💡 Today's Study Tip")
        st.markdown(f'<div class="tip-box">{random.choice(mood_tips)}</div>', unsafe_allow_html=True)
        st.caption(f"Based on your mood: {latest.get('emoji','')} {latest['mood']}")
