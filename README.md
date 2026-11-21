# Activity Buddy

An AI-powered preschool classroom and parent communication assistant built with **Streamlit**, **Google Gemini**, and **Groq**. Activity Buddy helps early childhood educators generate screen-free home learning activities, convert classroom voice notes into structured developmental observations, and draft warm parent updates in English and Hindi.

---

## Features

### Feature A — Home Activity Ideas
- Generates **3 practical, screen-free home activities** tailored to a child's age, developmental area (*Physical, Cognitive, Language, Social-Emotional, Creative*), and language (**English** or **Hindi**).
- Uses only safe, everyday household items with clear step-by-step instructions and an encouraging parent tip.

### Feature B — Voice Note to 3-Line Observation
- Transcribes teacher voice recordings (supporting English and Hindi) using **Groq Whisper (`whisper-large-v3-turbo`)**.
- Converts raw transcripts into a concise, privacy-safe **3-line structured observation**:
  1. **What the child did**
  2. **Skill it shows**
  3. **Next step**

### Feature C — Parent WhatsApp Message
- Transforms the 3-line observation into a **warm, jargon-free 2-line parent update** ready to copy and send, including a simple 5-minute activity parents can try at home.

---

## Tech Stack
- **Frontend:** Python, Streamlit
- **Text & Structured JSON Generation:** Google Gemini (`gemini-3.5-flash-lite`) & Groq LLM
- **Speech-to-Text Transcription:** Groq Whisper (`whisper-large-v3-turbo`)
- **Environment Management:** `python-dotenv`

---

## Project Structure
```text
activity-buddy/
├── app.py              # Streamlit UI and user workflow
├── ai.py               # Gemini and Groq API integrations & error handling
├── prompts.py          # Prompt templates for activities, observations, and parent messages
├── requirements.txt    # Python dependencies
├── screenshot/         # Application screenshots
│   ├── feature_a1.png
│   ├── feature_a2.png
│   └── feature_bc.png
└── README.md           # Project documentation