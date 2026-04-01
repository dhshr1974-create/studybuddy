import streamlit as st

TRACKS = [
    {"name": "☕ Coffee Shop",       "url": "https://www.youtube.com/embed/DVrqMGFMaVY?autoplay=0"},
    {"name": "🌧️ Rainy Day",         "url": "https://www.youtube.com/embed/mPZkdNFkNps?autoplay=0"},
    {"name": "🌊 Ocean Waves",        "url": "https://www.youtube.com/embed/bn9F19Hi1Lk?autoplay=0"},
    {"name": "🌲 Forest Sounds",      "url": "https://www.youtube.com/embed/xNN7iTA57jM?autoplay=0"},
    {"name": "🎵 Lo-fi Hip Hop",      "url": "https://www.youtube.com/embed/jfKfPfyJRdk?autoplay=0"},
    {"name": "🔥 Fireplace",          "url": "https://www.youtube.com/embed/L_LUpnjgPso?autoplay=0"},
    {"name": "🌌 Deep Focus",         "url": "https://www.youtube.com/embed/5qap5aO4i9A?autoplay=0"},
    {"name": "📚 Library Ambience",   "url": "https://www.youtube.com/embed/FjHGZj2IjBk?autoplay=0"},
]

def show():
    st.title("🎵 Study Ambient Music")
    st.markdown("Pick a soundscape to boost your focus. Opens in an embedded player!")

    cols = st.columns(4)
    selected = st.session_state.get("ambient_track", None)

    for i, track in enumerate(TRACKS):
        with cols[i % 4]:
            if st.button(track["name"], use_container_width=True, key=f"track_{i}"):
                st.session_state["ambient_track"] = track

    if selected := st.session_state.get("ambient_track"):
        st.markdown("---")
        st.markdown(f"### Now Playing: {selected['name']}")
        st.components.v1.iframe(selected["url"], height=200)
        st.caption("▶ Press play on the video above. Minimize the page and keep studying!")

    st.markdown("---")
    st.markdown("""
    **💡 Focus Tips:**
    - Use **Lo-fi Hip Hop** for steady, long study sessions
    - Use **Rain / Ocean / Forest** when you need to de-stress
    - Use **Deep Focus** for intense problem-solving
    - Avoid music with lyrics for reading/writing tasks
    """)
