import os
import json
from dotenv import load_dotenv
from google import genai
from groq import Groq
from prompts import ACTIVITY_PROMPT, OBSERVATION_PROMPT, PARENT_MESSAGE_PROMPT

load_dotenv()

GEMINI_MODEL = "gemini-3.5-flash-lite"
GROQ_WHISPER_MODEL = "whisper-large-v3-turbo"
GROQ_CHAT_MODEL = "openai/gpt-oss-120b"


class AppError(Exception):
    pass


def _handle_api_error(e: Exception):
    msg = str(e).lower()
    if "api key" in msg or "401" in msg or "unauthorized" in msg:
        raise AppError("API key not found or invalid. Please check your .env file.")
    if "429" in msg or "quota" in msg or "rate limit" in msg:
        raise AppError("Free limit reached. Please wait a minute and try again.")
    if "connection" in msg or "network" in msg or "getaddrinfo" in msg:
        raise AppError("Could not reach the AI service. Check your internet and try again.")
    if "503" in msg or "unavailable" in msg or "high demand" in msg:
        raise AppError("AI service is temporarily busy. Please wait a few seconds and try again.")
    raise AppError(f"Something went wrong: {e}")


def get_activities(age: int, area: str, language: str) -> list[dict]:
    if not os.getenv("GEMINI_API_KEY"):
        raise AppError("API key not found. Please add GEMINI_API_KEY to the .env file.")
    try:
        client = genai.Client()
        prompt = ACTIVITY_PROMPT.format(age=age, area=area, language=language)
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )
        if not response.text:
            raise AppError("No answer received. Please try again.")
        return json.loads(response.text)
    except AppError:
        raise
    except Exception as e:
        _handle_api_error(e)


def transcribe_audio(audio_bytes: bytes, filename: str = "note.wav") -> str:
    if not os.getenv("GROQ_API_KEY"):
        raise AppError("API key not found. Please add GROQ_API_KEY to the .env file.")
    if not audio_bytes or len(audio_bytes) < 1000:
        raise AppError("The voice note is too short. Please record again.")
    try:
        client = Groq()
        transcript = client.audio.transcriptions.create(
            file=(filename, audio_bytes),
            model=GROQ_WHISPER_MODEL,
        ).text
        if not transcript or not transcript.strip():
            raise AppError("The voice note is too short or unclear. Please record again.")
        return transcript.strip()
    except AppError:
        raise
    except Exception as e:
        _handle_api_error(e)


def make_observation(transcript: str, language: str) -> str:
    if not os.getenv("GROQ_API_KEY"):
        raise AppError("API key not found. Please add GROQ_API_KEY to the .env file.")
    try:
        client = Groq()
        prompt = OBSERVATION_PROMPT.format(transcript=transcript, language=language)
        res = client.chat.completions.create(
            model=GROQ_CHAT_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        text = res.choices[0].message.content
        if not text:
            raise AppError("No answer received. Please try again.")
        return text.strip()
    except AppError:
        raise
    except Exception as e:
        _handle_api_error(e)


def write_parent_message(observation: str, language: str) -> str:
    if not os.getenv("GROQ_API_KEY"):
        raise AppError("API key not found. Please add GROQ_API_KEY to the .env file.")
    try:
        client = Groq()
        prompt = PARENT_MESSAGE_PROMPT.format(observation=observation, language=language)
        res = client.chat.completions.create(
            model=GROQ_CHAT_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        text = res.choices[0].message.content
        if not text:
            raise AppError("No answer received. Please try again.")
        return text.strip()
    except AppError:
        raise
    except Exception as e:
        _handle_api_error(e)