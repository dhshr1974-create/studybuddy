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

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f: json.dump(data, f, indent=2, default=str)

def urgency(deadline_str):
    try:
        days = (date.fromisoformat(deadline_str) - date.today()).days
        if days < 0:  return "🔴 Overdue"
        if days == 0: return "🔴 Due Today"
        if days <= 2: return f"🟠 {days}d left"
        if days <= 7: return f"🟡 {days}d left"
        return f"🟢 {days}d left"
    except: return "—"

def show(username):
    st.title("✅ Assignment Manager")
    path = f"data/{username}_tasks.json"
    if "tasks" not in st.session_state:
        st.session_state.tasks = load_json(path, [])

    with st.expander("➕ Add New Assignment", expanded=False):
        with st.form("add_task", clear_on_submit=True):
            c1,c2 = st.columns(2)
            title    = c1.text_input("Title *")
            subject  = c2.text_input("Subject")
            c3,c4   = st.columns(2)
            deadline = c3.date_input("Deadline", min_value=date.today())
            priority = c4.selectbox("Priority", ["High","Medium","Low"])
            notes    = st.text_area("Notes", height=70)
            if st.form_submit_button("Add Assignment 🚀", use_container_width=True):
                if not title: st.warning("Enter a title!")
                else:
                    st.session_state.tasks.append({
                        "id": len(st.session_state.tasks),
                        "title": title, "subject": subject,
                        "deadline": str(deadline), "priority": priority,
                        "notes": notes, "done": False, "created": str(date.today())
                    })
                    save_json(path, st.session_state.tasks)
                    st.success(f"Added: {title} ✅")

    st.markdown("---")
    fc1,fc2 = st.columns(2)
    f_status   = fc1.selectbox("Status", ["All","Pending","Completed"])
    f_priority = fc2.selectbox("Priority", ["All","High","Medium","Low"])

    tasks = st.session_state.tasks
    filtered = [t for t in tasks
                if (f_status=="All" or (f_status=="Pending" and not t["done"]) or (f_status=="Completed" and t["done"]))
                and (f_priority=="All" or t["priority"]==f_priority)]
    filtered = sorted(filtered, key=lambda x: (x["done"], x.get("deadline","9999")))

    if not filtered:
        st.info("No tasks found. Add one above! 📝")
    for task in filtered:
        idx = st.session_state.tasks.index(task)
        col1,col2,col3 = st.columns([0.05,0.8,0.15])
        with col1:
            done_now = st.checkbox("", value=task["done"], key=f"chk_{idx}")
            if done_now != task["done"]:
                st.session_state.tasks[idx]["done"] = done_now
                save_json(path, st.session_state.tasks)
                st.rerun()
        with col2:
            label = urgency(task["deadline"])
            pri_icon = {"High":"🔴","Medium":"🟡","Low":"🟢"}.get(task["priority"],"")
            style = "text-decoration:line-through;color:#aaa" if task["done"] else ""
            st.markdown(f'<span style="{style}"><b>{task["title"]}</b> &nbsp; <code>{task.get("subject","")}</code> &nbsp; {label} &nbsp; {pri_icon}</span>', unsafe_allow_html=True)
            if task.get("notes"): st.caption(task["notes"])
        with col3:
            if st.button("🗑️", key=f"del_{idx}"):
                st.session_state.tasks.pop(idx)
                save_json(path, st.session_state.tasks)
                st.rerun()
        st.markdown("<hr style='margin:4px 0;border-color:#f0f0f0'>", unsafe_allow_html=True)
