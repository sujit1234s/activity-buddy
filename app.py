import streamlit as st
from ai import (
    AppError,
    get_activities,
    transcribe_audio,
    make_observation,
    write_parent_message,
)

st.set_page_config(page_title="Activity Buddy", page_icon="🧸", layout="centered")

# --- SpacECE PDF COLOR SCHEME & STYLING ---
st.markdown("""
<style>
    /* Main Cream-White Canvas & Navy Text */
    .stApp {
        background-color: #FFFDF8;
        color: #14365D;
    }

    /* SpacECE Navy Banner with Warm Gold Bottom Accent */
    .spacece-header {
        background-color: #14365D;
        color: #FFFFFF;
        padding: 20px 24px;
        border-radius: 12px;
        border-bottom: 5px solid #E8A825;
        margin-bottom: 18px;
        box-shadow: 0 4px 10px rgba(20, 54, 93, 0.12);
    }
    .spacece-header h1 {
        color: #FFFFFF !important;
        margin: 0;
        font-size: 1.85rem;
    }
    .spacece-header p {
        color: #FDF8EE;
        margin: 6px 0 0 0;
        font-size: 0.95rem;
    }

    /* Section Headings */
    h2, h3, h4 {
        color: #14365D !important;
    }

    /* Activity Cards (Soft Cream with Gold Left Accent) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FDF8EE;
        border: 1px solid #E2D5B5;
        border-left: 5px solid #E8A825;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 3px 8px rgba(20, 54, 93, 0.06);
    }

    /* Primary & Secondary Buttons */
    div.stButton > button[kind="primary"] {
        background-color: #14365D !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px;
        font-weight: 600;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #E8A825 !important;
        color: #14365D !important;
    }
    div.stButton > button[kind="secondary"] {
        background-color: #FDF8EE !important;
        color: #14365D !important;
        border: 1.5px solid #14365D !important;
        border-radius: 8px;
        font-weight: 600;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #E8A825 !important;
        border-color: #E8A825 !important;
        color: #14365D !important;
    }

    /* Tabs Styling */
    button[data-baseweb="tab"] {
        color: #14365D !important;
        font-weight: 600;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #14365D !important;
        border-bottom-color: #E8A825 !important;
        font-weight: 700;
    }

    /* Callout / Info Boxes (Soft Ice Blue) */
    div[data-testid="stAlert"] {
        background-color: #EBF3FA;
        color: #14365D;
        border-left: 4px solid #14365D;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="spacece-header">
    <h1>🧸 Activity Buddy</h1>
    <p>An AI helper for preschool teachers and parents (Use dummy names like Child A only) • SpacECE India Foundation</p>
</div>
""", unsafe_allow_html=True)

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