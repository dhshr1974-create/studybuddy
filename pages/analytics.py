import streamlit as st
import json, os
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta, date

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
    st.title("📊 Analytics")
    tasks  = load_json(f"data/{username}_tasks.json", [])
    moods  = load_json(f"data/{username}_moods.json", [])
    grades = load_json(f"data/{username}_grades.json", [])

    if not tasks:
        st.info("Add tasks to see analytics!")
        return

    df = pd.DataFrame(tasks)
    done    = df[df["done"]==True]
    pending = df[df["done"]==False]

    # Top metrics
    c1,c2,c3,c4 = st.columns(4)
    pct = int(len(done)/len(df)*100) if len(df) else 0
    with c1: st.metric("Total Tasks",    len(df))
    with c2: st.metric("Completed",      len(done))
    with c3: st.metric("Pending",        len(pending))
    with c4: st.metric("Completion Rate", f"{pct}%")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Tasks by Subject")
        if "subject" in df.columns:
            subj = df.groupby("subject").agg(Total=("title","count"), Done=("done","sum")).reset_index()
            subj["Pending"] = subj["Total"] - subj["Done"]
            fig = px.bar(subj, x="subject", y=["Done","Pending"], barmode="stack",
                         color_discrete_map={"Done":"#27ae60","Pending":"#e74c3c"})
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Priority Breakdown")
        if "priority" in df.columns:
            pri = df["priority"].value_counts().reset_index()
            pri.columns = ["Priority","Count"]
            fig2 = px.pie(pri, names="Priority", values="Count",
                          color_discrete_sequence=["#e74c3c","#f39c12","#27ae60"])
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig2, use_container_width=True)

    # Grades chart
    if grades:
        st.markdown("### 📈 Grade Trends")
        df_g = pd.DataFrame(grades)
        fig3 = px.line(df_g, x="date", y="grade", color="subject", markers=True,
                       labels={"grade":"Grade (%)","date":"Date"})
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig3, use_container_width=True)

    # Mood distribution
    if moods:
        st.markdown("### 😊 Mood Distribution")
        df_m = pd.DataFrame(moods)
        mc = df_m["mood"].value_counts().reset_index()
        mc.columns = ["Mood","Count"]
        fig4 = px.bar(mc, x="Mood", y="Count", color="Mood",
                      color_discrete_map={"Happy":"#27ae60","Stressed":"#e74c3c","Tired":"#f39c12"})
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig4, use_container_width=True)
