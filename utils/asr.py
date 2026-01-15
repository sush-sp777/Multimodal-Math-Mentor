import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def transcribe_audio(audio_file):
    """
    Uses Groq Whisper API
    Streamlit-cloud safe
    """
    audio_file.seek(0)

    response = client.audio.transcriptions.create(
        file=(audio_file.name, audio_file.read()),
        model="whisper-large-v3"
    )

    text = response.text.strip()

    confidence = 0.9 if len(text.split()) > 5 else 0.6

    return {
        "text": text,
        "confidence": confidence,
        "needs_clarification": confidence < 0.7
    }
