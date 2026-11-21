import streamlit as st
from ai import (
    AppError,
    get_activities,
    transcribe_audio,
    make_observation,
    write_parent_message,
)

st.set_page_config(page_title="Activity Buddy", page_icon="🧸", layout="centered")
st.title("🧸 Activity Buddy")
st.caption("An AI helper for preschool teachers and parents (Use dummy names like Child A only)")

tab1, tab2 = st.tabs(["🎨 A. Activity Ideas", "🎙️ B & C. Voice Note & Parent Message"])

# --- FEATURE A: ACTIVITY IDEAS ---
with tab1:
    st.subheader("Home Activity Ideas")
    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("Child age (years)", min_value=2, max_value=8, value=4)
        language_a = st.radio("Language", ["English", "Hindi"], horizontal=True, key="lang_a")
    with col2:
        area = st.selectbox(
            "Development area",
            ["Physical", "Language", "Cognitive (thinking)", "Social-Emotional", "Creative"],
        )

    if st.button("Get activities", type="primary"):
        with st.spinner("Finding safe home activities..."):
            try:
                activities = get_activities(age, area, language_a)
                for act in activities:
                    with st.container(border=True):
                        st.markdown(f"### {act.get('icon', '✨')} {act.get('title', 'Activity')}")
                        st.markdown(f"**Materials:** {act.get('materials', '')}")
                        st.markdown("**Steps:**")
                        for i, step in enumerate(act.get("steps", []), 1):
                            st.write(f"{i}. {step}")
                        st.info(f"**What the child learns:** {act.get('learns', '')}")
            except AppError as e:
                st.error(str(e))

# --- FEATURES B & C: VOICE NOTE TO OBSERVATION & PARENT MESSAGE ---
with tab2:
    st.subheader("Voice Note to Observation")
    lang_bc = st.radio("Output Language", ["English", "Hindi"], horizontal=True, key="lang_bc")

    recorded_audio = st.audio_input("Record a voice note (15–30 sec, dummy names only)")
    uploaded_audio = st.file_uploader("Or upload an audio file", type=["mp3", "wav", "m4a"])

    audio_source = recorded_audio or uploaded_audio

    if audio_source and st.button("Transcribe Audio"):
        with st.spinner("Transcribing with Groq Whisper..."):
            try:
                audio_bytes = audio_source.read()
                filename = getattr(audio_source, "name", "note.wav")
                st.session_state["transcript"] = transcribe_audio(audio_bytes, filename)
            except AppError as e:
                st.error(str(e))

    if "transcript" in st.session_state:
        edited_transcript = st.text_area(
            "Transcript (edit any mistakes before making observation):",
            value=st.session_state["transcript"],
            height=100,
        )
        if st.button("Make observation", type="primary"):
            with st.spinner("Creating 3-line observation..."):
                try:
                    st.session_state["observation"] = make_observation(edited_transcript, lang_bc)
                    st.session_state.pop("parent_msg", None)
                except AppError as e:
                    st.error(str(e))

    if "observation" in st.session_state:
        st.markdown("#### 3-Line Observation")
        st.success(st.session_state["observation"])

        if st.button("Write message for parent"):
            with st.spinner("Writing friendly parent message..."):
                try:
                    st.session_state["parent_msg"] = write_parent_message(
                        st.session_state["observation"], lang_bc
                    )
                except AppError as e:
                    st.error(str(e))

    if "parent_msg" in st.session_state:
        st.markdown("#### Parent Message (Click copy icon on top-right to paste on WhatsApp)")
        st.code(st.session_state["parent_msg"], language=None)